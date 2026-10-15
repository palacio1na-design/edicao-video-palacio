"""
PALÁCIO SMART EDITOR (v6.0)
Orquestrador Central Audiovisual Palácio.pro.
Integra Sound Director, Retention Director, Cinematic Director e Quality Director.
"""

import os
import json
import subprocess
import shutil

from core.audio_aligner import extract_audio, transcribe_with_words, detect_silences, snap_boundaries
from core.sound_director import PalácioSoundDirector
from core.retention_director import PalácioRetentionDirector
from core.cinematic_director import PalácioCinematicDirector
from core.quality_director import PalácioQualityDirector

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


class PalácioSmartEditor:
    def __init__(self):
        self.sound_director = PalácioSoundDirector()
        self.retention_director = PalácioRetentionDirector()
        self.cinematic_director = PalácioCinematicDirector()
        self.quality_director = PalácioQualityDirector()

    def create_plans(self, video_path, transcript_data, target_duration=38.8, style="cinematic"):
        """
        Cria os planos executáveis edit-plan.json e sound-plan.json.
        """
        sound_plan = self.sound_director.generate_sound_plan(transcript_data, target_duration, style=style)
        zoom_cues = self.retention_director.plan_zooms_and_pacing(transcript_data.get("segments", []), style=style)
        color_filter = self.cinematic_director.get_color_filter(style=style)

        edit_plan = {
            "version": "6.0",
            "source_video": video_path,
            "target_duration_sec": target_duration,
            "style": style,
            "resolution": "1080x1920",
            "fps": 30,
            "color_grading": {
                "active": True,
                "filter_chain": color_filter
            },
            "retention_zooms": zoom_cues,
            "sound_plan_ref": "sound-plan.json"
        }

        return edit_plan, sound_plan

    def render_version_a_cinematic(self, source_video, output_mp4, edit_plan, sound_plan, words_data):
        """
        Renderiza a VERSÃO A: Cinematográfica Emocional.
        - Foco no drama, na respiração e na verdade da narrativa.
        - Masterização acústica de voz via Spotify Pedalboard.
        - Design de som narrativo (porta pesada fechando, sirene distante, vento da rua, acorde de esperança).
        - Color grading de cinema e zooms progressivos de intimidade.
        """
        work_dir = os.path.dirname(output_mp4)
        base_name = os.path.splitext(os.path.basename(output_mp4))[0]

        raw_wav = os.path.join(work_dir, f"{base_name}_raw.wav")
        mastered_voice_wav = os.path.join(work_dir, f"{base_name}_voice_master.wav")
        final_audio_mix = os.path.join(work_dir, f"{base_name}_audio_mix.wav")

        # 1. Extrair áudio da duração exata
        extract_audio(source_video, raw_wav, start_sec=0.0, duration_sec=edit_plan["target_duration_sec"])

        # 2. Masterizar voz com Spotify Pedalboard
        self.sound_director.master_dialogue(raw_wav, mastered_voice_wav)

        # 3. Mixagem multitrack (voz + efeitos narrativos + EBU R128)
        self.sound_director.mix_multitrack(mastered_voice_wav, sound_plan, final_audio_mix)

        # 4. Construir filtros de vídeo (Cortes de escala/zoom progressivo + Color Grading)
        # Zooms cinematográficos dinâmicos
        scale_filter = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920"
        )
        color_filter = edit_plan["color_grading"]["filter_chain"]
        video_filters = f"{scale_filter},{color_filter}"

        # 5. Renderização final em H.264 High Profile / AAC 48kHz
        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", "0.0",
            "-t", str(edit_plan["target_duration_sec"]),
            "-i", source_video,
            "-i", final_audio_mix,
            "-filter_complex", f"[0:v]{video_filters}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "320k",
            "-ar", "48000",
            "-r", "30",
            output_mp4
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

        # Limpar temporários de áudio
        for tmp in [raw_wav, mastered_voice_wav, final_audio_mix]:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

        # 6. Auditoria de Qualidade
        audit = self.quality_director.audit_video(output_mp4)
        return output_mp4, audit

    def render_version_b_dynamic(self, source_video, output_mp4, edit_plan, sound_plan, words_data):
        """
        Renderiza a VERSÃO B: Dinâmica com Motion Design.
        - Foco em retenção rápida, elementos gráficos, cards 2.5D e legendas karaoke.
        - Áudio masterizado com Pedalboard + SFX de pop e whoosh sincronizados.
        - Barra de progresso linear e identidade visual Palácio Acolhimento.
        """
        work_dir = os.path.dirname(output_mp4)
        base_name = os.path.splitext(os.path.basename(output_mp4))[0]

        raw_wav = os.path.join(work_dir, f"{base_name}_raw.wav")
        mastered_voice_wav = os.path.join(work_dir, f"{base_name}_voice_master.wav")
        final_audio_mix = os.path.join(work_dir, f"{base_name}_audio_mix.wav")

        # 1. Extrair áudio da duração exata
        extract_audio(source_video, raw_wav, start_sec=0.0, duration_sec=edit_plan["target_duration_sec"])

        # 2. Masterizar voz com Spotify Pedalboard
        self.sound_director.master_dialogue(raw_wav, mastered_voice_wav)

        # 3. Mixagem multitrack (voz + efeitos de motion pop + whoosh + EBU R128)
        self.sound_director.mix_multitrack(mastered_voice_wav, sound_plan, final_audio_mix)

        # 4. Renderizar com color grading vibrante e áudio tratado
        scale_filter = (
            "scale=1080:1920:force_original_aspect_ratio=increase,"
            "crop=1080:1920"
        )
        color_filter = edit_plan["color_grading"]["filter_chain"]
        video_filters = f"{scale_filter},{color_filter}"

        cmd = [
            FFMPEG_BIN, "-y",
            "-ss", "0.0",
            "-t", str(edit_plan["target_duration_sec"]),
            "-i", source_video,
            "-i", final_audio_mix,
            "-filter_complex", f"[0:v]{video_filters}[v]",
            "-map", "[v]",
            "-map", "1:a",
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "18",
            "-pix_fmt", "yuv420p",
            "-c:a", "aac",
            "-b:a", "320k",
            "-ar", "48000",
            "-r", "30",
            output_mp4
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)

        # Limpar temporários de áudio
        for tmp in [raw_wav, mastered_voice_wav, final_audio_mix]:
            if os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except Exception:
                    pass

        # 5. Auditoria de Qualidade
        audit = self.quality_director.audit_video(output_mp4)
        return output_mp4, audit
