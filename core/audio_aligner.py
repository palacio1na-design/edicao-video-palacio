import os
import sys
import re
import subprocess
import json

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"

def extract_audio(video_path, output_wav=None, start_sec=None, duration_sec=None):
    """
    Extrai áudio mono 16kHz PCM WAV do vídeo para análise rápida e precisa.
    """
    if not output_wav:
        base, _ = os.path.splitext(video_path)
        output_wav = base + "_audio.wav"

    cmd = [FFMPEG_BIN, "-y"]
    if start_sec is not None:
        cmd.extend(["-ss", str(start_sec)])
    cmd.extend(["-i", video_path])
    if duration_sec is not None:
        cmd.extend(["-t", str(duration_sec)])
    cmd.extend(["-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_wav])

    subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
    return output_wav

def detect_silences(wav_path, noise_threshold="-30dB", min_duration=0.18):
    """
    Mapeia todos os silêncios acústicos reais usando o filtro silencedetect do FFmpeg.
    Retorna lista de dicionários: [{'start': float, 'end': float, 'duration': float}]
    """
    cmd = [
        FFMPEG_BIN, "-i", wav_path,
        "-af", f"silencedetect=noise={noise_threshold}:d={min_duration}",
        "-f", "null", "-"
    ]
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    stderr = res.stderr

    silences = []
    current_start = None
    for line in stderr.splitlines():
        if "silence_start:" in line:
            m = re.search(r"silence_start:\s*([0-9.]+)", line)
            if m:
                current_start = float(m.group(1))
        elif "silence_end:" in line:
            m_end = re.search(r"silence_end:\s*([0-9.]+)", line)
            m_dur = re.search(r"silence_duration:\s*([0-9.]+)", line)
            if m_end:
                end_val = float(m_end.group(1))
                dur_val = float(m_dur.group(1)) if m_dur else (end_val - (current_start or 0.0))
                start_val = current_start if current_start is not None else max(0.0, end_val - dur_val)
                silences.append({
                    "start": start_val,
                    "end": end_val,
                    "duration": dur_val
                })
                current_start = None

    return silences

def transcribe_with_words(wav_path, model_name="base", language="pt"):
    """
    Transcreve áudio com Whisper retornando alinhamento a nível de palavra.
    """
    import whisper
    bin_dir = os.path.dirname(FFMPEG_BIN)
    if bin_dir and bin_dir not in os.environ.get("PATH", ""):
        os.environ["PATH"] = f"{bin_dir}:{os.environ.get('PATH', '')}"

    model = whisper.load_model(model_name)
    result = model.transcribe(wav_path, language=language, word_timestamps=True)

    segments = []
    all_words = []

    for seg in result.get("segments", []):
        seg_words = []
        for w in seg.get("words", []):
            item = {
                "word": w["word"].strip(),
                "start": round(float(w["start"]), 3),
                "end": round(float(w["end"]), 3),
                "probability": round(float(w.get("probability", 1.0)), 3)
            }
            seg_words.append(item)
            all_words.append(item)

        segments.append({
            "id": seg["id"],
            "start": round(float(seg["start"]), 3),
            "end": round(float(seg["end"]), 3),
            "text": seg["text"].strip(),
            "words": seg_words
        })

    return {
        "text": result.get("text", "").strip(),
        "segments": segments,
        "words": all_words
    }

def snap_boundaries(requested_start, requested_end, words, silences, pad_before=0.08, pad_after=0.20):
    """
    Encaixa os limites do corte cirurgicamente nos vales de silêncio acústico reais.
    Garante que:
    1. A primeira palavra comece logo após o início do corte.
    2. A última palavra termine antes do fim do corte.
    3. Nenhuma sílaba ou consoante inicial/final seja decepada.
    4. O respiro natural seja preservado.
    """
    in_range_words = [w for w in words if w["end"] >= requested_start and w["start"] <= requested_end]
    if not in_range_words:
        return {
            "start": round(float(requested_start), 3),
            "end": round(float(requested_end), 3),
            "duration": round(float(requested_end - requested_start), 3),
            "first_word": None,
            "last_word": None,
            "snapped": False
        }

    first_word = in_range_words[0]
    last_word = in_range_words[-1]

    w_start = float(first_word["start"])
    w_end = float(last_word["end"])

    # 1. Ajuste do Início: procurar silêncio imediatamente anterior a w_start
    best_start = max(0.0, w_start - pad_before)
    candidate_silences_before = [s for s in silences if s["start"] <= w_start and (w_start - s["end"]) < 2.5]
    if candidate_silences_before:
        s = max(candidate_silences_before, key=lambda x: x["end"])
        if s["end"] <= w_start:
            # Ponto ideal: final do silêncio menos pad_before
            best_start = max(s["start"], s["end"] - pad_before)
        else:
            best_start = max(0.0, s["start"] + 0.05)

    # 2. Ajuste do Fim: procurar silêncio imediatamente posterior a w_end
    best_end = w_end + pad_after
    candidate_silences_after = [s for s in silences if s["end"] >= w_end and (s["start"] - w_end) < 2.0]
    if candidate_silences_after:
        s = min(candidate_silences_after, key=lambda x: x["start"])
        silence_dur = s["duration"]
        extra = min(pad_after, silence_dur * 0.4)
        best_end = s["start"] + extra

    return {
        "start": round(best_start, 3),
        "end": round(best_end, 3),
        "duration": round(best_end - best_start, 3),
        "first_word": first_word["word"],
        "last_word": last_word["word"],
        "first_word_time": w_start,
        "last_word_time": w_end,
        "snapped": True
    }
