import os
import sys
import subprocess
import json

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
        if len(chunk) >= words_per_line or w["word"].endswith((".", "!", "?", ",")):
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
    broll_seek=2.0
):
    """
    Renderiza o corte em formato 9:16 vertical (1080x1920) com áudio EBU R128 (-14 LUFS).
    Suporta B-roll overlay contextual com transições suaves em crossfade.
    Usa aceleração por hardware da Apple (h264_videotoolbox).
    """
    os.makedirs(os.path.dirname(os.path.abspath(output_video)), exist_ok=True)

    has_broll = broll_video and os.path.exists(broll_video) and duration_sec > (broll_start_in_cut + 2.0)

    if has_broll:
        # Pipeline com B-Roll
        b_st = float(broll_start_in_cut)
        b_dur = float(broll_duration)
        fade_dur = 0.35
        fade_out_st = max(0.1, b_dur - fade_dur)

        filter_complex = [
            # 1. Vídeo principal 9:16
            "[0:v]crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos[main]",
            # 2. B-Roll ajustado em 9:16 com fade in e out
            f"[1:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,format=yuva420p,fade=t=in:st=0:d={fade_dur}:alpha=1,fade=t=out:st={fade_out_st}:d={fade_dur}:alpha=1[broll]",
            # 3. Overlay do B-roll no momento exato
            f"[main][broll]overlay=0:0:enable='between(t,{b_st},{b_st+b_dur})'[v_mixed]"
        ]

        final_v = "[v_mixed]"
        if burn_subtitles and srt_path and os.path.exists(srt_path):
            escaped_srt = srt_path.replace(":", "\\:").replace("'", "\\'")
            style = "FontName=HelveticaNeue-Bold,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=120"
            filter_complex.append(f"{final_v}subtitles='{escaped_srt}':force_style='{style}'[v_sub]")
            final_v = "[v_sub]"

        af_filter = "loudnorm=I=-14:LRA=7:TP=-1.0" if normalize_audio else "anull"
        filter_complex.append(f"[0:a]{af_filter}[a]")

        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(start_sec), "-i", input_video,
            "-ss", str(broll_seek), "-i", broll_video,
            "-filter_complex", "; ".join(filter_complex),
            "-map", final_v,
            "-map", "[a]",
            "-t", str(duration_sec),
            "-c:v", "h264_videotoolbox",
            "-b:v", "6500k",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-movflags", "+faststart",
            output_video
        ]
    else:
        # Pipeline limpo sem B-Roll
        vf_filters = []
        if crop_916:
            vf_filters.append("crop=ih*9/16:ih:(iw-ih*9/16)/2:0,scale=1080:1920:flags=lanczos")

        if burn_subtitles and srt_path and os.path.exists(srt_path):
            escaped_srt = srt_path.replace(":", "\\:").replace("'", "\\'")
            style = "FontName=HelveticaNeue-Bold,FontSize=20,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=2,Shadow=1,Alignment=2,MarginV=120"
            vf_filters.append(f"subtitles='{escaped_srt}':force_style='{style}'")

        vf_arg = ",".join(vf_filters) if vf_filters else "null"
        af_arg = "loudnorm=I=-14:LRA=7:TP=-1.0" if normalize_audio else "anull"

        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", str(start_sec), "-i", input_video,
            "-vf", vf_arg,
            "-af", af_arg,
            "-t", str(duration_sec),
            "-c:v", "h264_videotoolbox",
            "-b:v", "6500k",
            "-c:a", "aac",
            "-b:a", "192k",
            "-ar", "48000",
            "-movflags", "+faststart",
            output_video
        ]

    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    if res.returncode != 0:
        # Fallback para software encoder libx264
        cmd[cmd.index("-c:v") + 1] = "libx264"
        cmd[cmd.index("-b:v")] = "-preset"
        cmd[cmd.index("-preset") + 1] = "veryfast"
        res_fb = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res_fb.returncode != 0:
            raise RuntimeError(f"FFmpeg render error: {res_fb.stderr}")

    return output_video
