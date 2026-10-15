import os
import sys
import subprocess
import json
from typing import Optional, List, Dict, Any

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"

def generate_srt(words, output_srt_path, words_per_line=3):
    """
    Gera um arquivo .srt com legendas dinâmicas (2 a 3 palavras por tela)
    perfeitamente sincronizadas com os timestamps reais.
    """
    if not words:
        return None

    lines = []
    chunk = []
    for w in words:
        chunk.append(w)
        if len(chunk) >= words_per_line or w.get("word", "").endswith((".", "!", "?", ",")):
            lines.append(list(chunk))
            chunk = []
    if chunk:
        lines.append(chunk)

    def format_time(sec):
        millis = int((sec - int(sec)) * 1000)
        s = int(sec) % 60
        m = (int(sec) // 60) % 60
        h = int(sec) // 3600
        return f"{h:02d}:{m:02d}:{s:02d},{millis:03d}"

    with open(output_srt_path, "w", encoding="utf-8") as f:
        for idx, cl in enumerate(lines, 1):
            s_time = format_time(cl[0]["start"])
            e_time = format_time(cl[-1]["end"])
            text = " ".join([x["word"] for x in cl])
            f.write(f"{idx}\n{s_time} --> {e_time}\n{text}\n\n")

    return output_srt_path

def cut_and_render_reel(
    input_video,
    output_video,
    start_sec,
    duration_sec,
    crop_916=True,
    normalize_audio=True,
    burn_subtitles=False,
    srt_path=None,
    broll_video=None,
    broll_start_in_cut=5.0,
    broll_duration=5.0,
    broll_seek=2.0,
    zoom_cues: Optional[List[Dict[str, Any]]] = None
):
    """
    Renderiza o corte em formato 9:16 vertical (1080x1920) com áudio EBU R128 (-14 LUFS).
    Suporta Zooms dinâmicos (punch-in nos momentos emocionais), B-roll contextual e legendas em safe-zone.
    Usa aceleração por hardware da Apple (h264_videotoolbox) com fallback automático para libx264.
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)

    has_broll = broll_video and os.path.exists(broll_video) and duration_sec > (broll_start_in_cut + 2.0)

    # 1. Base do vídeo 9:16 com ou sem punch-in dinâmico
    base_crop = "crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos"
    
    # Se houver zoom cues especificados, aplica punch-in no momento exato
    if zoom_cues:
        # Ex: zoom_cues = [{"start": 2.0, "end": 6.0, "scale": 1.15}]
        # Aplica zoom dinâmico suave sem tremer
        cue = zoom_cues[0]
        c_st = max(0.0, cue.get("start", 0.0) - start_sec)
        c_end = max(c_st + 0.5, cue.get("end", 0.0) - start_sec)
        c_scale = cue.get("scale", 1.15)
        # Corta ligeiramente mais fechado no intervalo do cue
        base_v_filter = (
            f"crop=w='if(between(t,{c_st:.2f},{c_end:.2f}),(ih*9/16)/{c_scale:.2f},ih*9/16)':"
            f"h='if(between(t,{c_st:.2f},{c_end:.2f}),ih/{c_scale:.2f},ih)':"
            f"x='(iw-ow)/2':y='(ih-oh)/2',"
            f"scale=1080:1920:flags=lanczos"
        )
    else:
        base_v_filter = base_crop

    filter_complex = []
    
    if has_broll:
        b_st = float(broll_start_in_cut)
        b_dur = float(broll_duration)
        fade_dur = 0.35
        fade_out_st = max(0.1, b_dur - fade_dur)

        filter_complex.extend([
            f"[0:v]{base_v_filter}[main]",
            f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuva420p,fade=t=in:st=0:d={fade_dur}:alpha=1,fade=t=out:st={fade_out_st}:d={fade_dur}:alpha=1[broll]",
            f"[main][broll]overlay=0:0:enable='between(t,{b_st},{b_st+b_dur})'[v_mixed]"
        ])
        final_v = "[v_mixed]"
    else:
        filter_complex.append(f"[0:v]{base_v_filter}[main]")
        final_v = "[main]"

    # Legendas com respeito estrito à ZONA SEGURA DAS REDES SOCIAIS (MarginV=260)
    if burn_subtitles and srt_path and os.path.exists(srt_path):
        escaped_srt = srt_path.replace(":", "\\:").replace("'", "\\'")
        # MarginV=260 evita sobreposição pela barra inferior do Reels/TikTok/Shorts
        style = (
            "FontName=HelveticaNeue-Bold,FontSize=22,"
            "PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,"
            "BorderStyle=1,Outline=2.5,Shadow=1.5,Alignment=2,MarginV=260"
        )
        filter_complex.append(f"{final_v}subtitles='{escaped_srt}':force_style='{style}'[v_sub]")
        final_v = "[v_sub]"

    # Verifica se o arquivo tem áudio embutido ou arquivo de áudio adjacente
    audio_source = input_video
    base_no_ext = os.path.splitext(input_video)[0]
    candidate_wav = base_no_ext.replace("_video", "_audio") + ".wav"
    candidate_wav2 = base_no_ext + ".wav"
    has_separate_audio = False

    # Procura probe de áudio
    probe_cmd = [FFMPEG_BIN, "-i", input_video]
    probe_res = subprocess.run(probe_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    has_audio_stream = "Audio:" in probe_res.stderr

    if not has_audio_stream:
        if os.path.exists(candidate_wav):
            audio_source = candidate_wav
            has_separate_audio = True
        elif os.path.exists(candidate_wav2):
            audio_source = candidate_wav2
            has_separate_audio = True

    if has_audio_stream or has_separate_audio:
        af_idx = "1:a" if has_separate_audio else "0:a"
        af_filter = "loudnorm=I=-14:LRA=7:TP=-1.0" if normalize_audio else "anull"
        filter_complex.append(f"[{af_idx}]{af_filter}[a]")
        has_audio_out = True
    else:
        has_audio_out = False

    cmd = [
        FFMPEG_BIN, "-y",
        "-ss", str(start_sec), "-i", input_video
    ]
    if has_separate_audio:
        cmd.extend(["-ss", str(start_sec), "-i", audio_source])
    if has_broll:
        cmd.extend(["-ss", str(broll_seek), "-i", broll_video])

    cmd.extend([
        "-filter_complex", "; ".join(filter_complex),
        "-map", final_v
    ])
    if has_audio_out:
        cmd.extend([
            "-map", "[a]",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000"
        ])
    cmd.extend([
        "-t", str(duration_sec),
        "-c:v", "h264_videotoolbox",
        "-b:v", "6500k",
        "-movflags", "+faststart",
        output_video
    ])

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        # Fallback para encoder de software libx264
        if "-c:v" in cmd:
            cmd[cmd.index("-c:v") + 1] = "libx264"
        if "-b:v" in cmd:
            cmd[cmd.index("-b:v")] = "-preset"
            cmd[cmd.index("-preset") + 1] = "veryfast"
        res_fb = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res_fb.returncode != 0:
            raise RuntimeError(f"FFmpeg render error: {res_fb.stderr}")

    return output_video

def render_remotion_composition(
    remotion_dir: str,
    composition_id: str,
    output_video: str,
    props: Optional[Dict[str, Any]] = None
) -> str:
    """
    Renderiza uma composição Remotion diretamente via CLI (npx remotion render).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)
    cmd = [
        "npx", "remotion", "render",
        composition_id,
        output_video,
        "--gl=angle"
    ]
    if props:
        props_json = json.dumps(props)
        cmd.extend(["--props", props_json])

    print(f"🎬 Disparando renderizador Remotion: {composition_id} -> {output_video}")
    res = subprocess.run(cmd, cwd=remotion_dir, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Remotion render error: {res.stderr}")
    return output_video
