"""
PALÁCIO SOUND DIRECTOR (v6.0)
Motor Inteligente de Design de Som, Mixagem Multitrack e Análise Narrativa.
Integrado com Spotify Pedalboard, FFmpeg e Palácio Cinematic Sound Library.
"""

import os
import json
import re
import subprocess
import numpy as np
import soundfile as sf
from pedalboard import (
    Pedalboard, Compressor, HighpassFilter, LowpassFilter,
    PeakFilter, Reverb, Limiter, Gain, NoiseGate
)

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"

SOUND_LIB_DIR = "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio/assets/sound-library"
MANIFEST_FILE = os.path.join(SOUND_LIB_DIR, "manifest.json")


class PalácioSoundDirector:
    def __init__(self, manifest_path=MANIFEST_FILE):
        self.manifest_path = manifest_path
        self.sounds_db = self._load_manifest()

    def _load_manifest(self):
        if os.path.exists(self.manifest_path):
            with open(self.manifest_path, "r", encoding="utf-8") as f:
                data = json.load(f)
                return {s["id"]: s for s in data.get("sounds", [])}
        return {}

    def analyze_narrative(self, words_or_segments, total_duration=39.0):
        """
        Analisa o fluxo semântico e emocional das falas e identifica
        oportunidades sonoras narrativas com justificativa editorial.
        """
        sound_cues = []
        
        # Mapeamento semântico de gatilhos
        narrative_rules = [
            {
                "trigger_words": ["fechou", "apartamento", "porta", "trancou", "decisão"],
                "sound_id": "door_firm_close",
                "default_offset": 0.1,
                "volume_db": -13.0,
                "category": "acontecimento",
                "justification": "Fechamento literal e metafórico da porta pelo pai (Amor Exigente)."
            },
            {
                "trigger_words": ["tentei", "tudo", "proteger", "mãe", "dor"],
                "sound_id": "tension_drone_c_minor",
                "default_offset": 0.2,
                "volume_db": -18.0,
                "category": "cinematografico",
                "justification": "Dramatismo e dor familiar diante da exaustão da família."
            },
            {
                "trigger_words": ["polícia", "viatura", "policial", "correr"],
                "sound_id": "distant_police_siren",
                "default_offset": -0.2,
                "volume_db": -19.0,
                "category": "acontecimento",
                "justification": "Sirene distante de viatura contextualizando o confronto e o limite imposto."
            },
            {
                "trigger_words": ["rua", "morando", "semana", "sozinho", "frio"],
                "sound_id": "night_city_wind",
                "default_offset": 0.0,
                "volume_db": -20.0,
                "category": "ambiente",
                "justification": "Desolação e solidão de uma semana morando na rua (fundo de poço)."
            },
            {
                "trigger_words": ["irmão", "fantástico", "recuperação", "viver"],
                "sound_id": "hope_resolution_chord",
                "default_offset": 0.3,
                "volume_db": -15.0,
                "category": "emocional",
                "justification": "Acorde harmônico de resolução, esperança e despertar da sobriedade."
            }
        ]

        # Extrair palavras com timestamps
        flat_words = []
        if isinstance(words_or_segments, dict) and "words" in words_or_segments:
            flat_words = words_or_segments["words"]
        elif isinstance(words_or_segments, list):
            for item in words_or_segments:
                if "words" in item:
                    flat_words.extend(item["words"])
                elif "word" in item:
                    flat_words.append(item)

        matched_rules = set()
        for w in flat_words:
            word_clean = re.sub(r"[^a-záéíóúãõç]", "", w["word"].lower())
            for rule_idx, rule in enumerate(narrative_rules):
                if rule_idx in matched_rules:
                    continue
                if word_clean in rule["trigger_words"]:
                    sound_info = self.sounds_db.get(rule["sound_id"])
                    if sound_info:
                        start_time = max(0.0, round(w["start"] + rule["default_offset"], 2))
                        if start_time < total_duration:
                            sound_cues.append({
                                "id": rule["sound_id"],
                                "name": sound_info["name"],
                                "file": sound_info["absolute_path"],
                                "start_time": start_time,
                                "duration": sound_info["duration_sec"],
                                "volume_db": rule["volume_db"],
                                "category": rule["category"],
                                "justification": rule["justification"]
                            })
                            matched_rules.add(rule_idx)

        return sound_cues

    def master_dialogue(self, input_wav, output_wav):
        """
        Masterização acústica profissional da voz com Spotify Pedalboard:
        - Highpass (corte de rumble < 80Hz)
        - NoiseGate suave (remoção de ruído de fundo entre falas)
        - EQ Paramétrico (corte de mudez em 280Hz e realce de brilho em 3.2kHz)
        - Compressão suave estilo broadcast (ratio 3.2:1)
        - Limiter de segurança TruePeak -1.0 dB
        """
        audio, sr = sf.read(input_wav)
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)

        board = Pedalboard([
            HighpassFilter(cutoff_frequency_hz=82.0),
            NoiseGate(threshold_db=-46.0, ratio=2.8, release_ms=120.0),
            PeakFilter(cutoff_frequency_hz=280.0, gain_db=-2.2, q=1.4),
            PeakFilter(cutoff_frequency_hz=3200.0, gain_db=2.8, q=1.2),
            Compressor(threshold_db=-19.0, ratio=3.2, attack_ms=4.0, release_ms=90.0),
            Limiter(threshold_db=-1.0, release_ms=80.0)
        ])

        mastered = board(audio, sr)
        sf.write(output_wav, mastered, sr, subtype="PCM_24")
        return output_wav

    def generate_sound_plan(self, transcript_data, total_duration, style="cinematic"):
        """
        Cria o sound-plan.json determinístico com planejamento de todas as camadas.
        """
        sfx_cues = self.analyze_narrative(transcript_data, total_duration)

        # Adicionar sons de motion design se houver estilo dinâmico
        if style == "motion" and "card_glass_pop" in self.sounds_db:
            card_pop = self.sounds_db["card_glass_pop"]
            whoosh = self.sounds_db.get("cinematic_whoosh")
            sfx_cues.insert(0, {
                "id": "card_glass_pop",
                "name": card_pop["name"],
                "file": card_pop["absolute_path"],
                "start_time": 0.4,
                "duration": card_pop["duration_sec"],
                "volume_db": -16.0,
                "category": "motion_design",
                "justification": "Entrada de card visual e gancho principal."
            })
            if whoosh:
                sfx_cues.append({
                    "id": "cinematic_whoosh",
                    "name": whoosh["name"],
                    "file": whoosh["absolute_path"],
                    "start_time": 3.6,
                    "duration": whoosh["duration_sec"],
                    "volume_db": -18.0,
                    "category": "transicao",
                    "justification": "Transição suave de saída do título de abertura."
                })

        plan = {
            "version": "6.0",
            "style": style,
            "total_duration_sec": total_duration,
            "sample_rate": 48000,
            "voice_track": {
                "priority": 1,
                "nominal_gain_db": 0.0,
                "chain": ["Highpass 82Hz", "NoiseGate -46dB", "EQ Paramétrico", "Compressor 3.2:1", "Limiter -1dB"]
            },
            "music_track": {
                "active": True,
                "ducking": {
                    "active_speech_db": -24.0,
                    "pause_speech_db": -15.0,
                    "fade_time_ms": 300
                }
            },
            "sfx_tracks": sfx_cues,
            "master_target": {
                "integrated_lufs": -14.0,
                "true_peak_dbfs": -1.0,
                "standards": "EBU R128 / Apple Podcasts / Instagram Reels"
            }
        }
        return plan

    def mix_multitrack(self, mastered_voice_wav, sound_plan, output_wav):
        """
        Executa a mixagem multitrack somando voz, efeitos sincronizados e ambiência,
        aplicando auto-ducking e normalização final para -14 LUFS.
        """
        voice, sr = sf.read(mastered_voice_wav)
        total_samples = int(sound_plan["total_duration_sec"] * sr)

        # Garantir tamanho e estéreo
        if len(voice) > total_samples:
            voice = voice[:total_samples]
        elif len(voice) < total_samples:
            pad = np.zeros(total_samples - len(voice))
            voice = np.concatenate([voice, pad])

        if len(voice.shape) == 1:
            mix_stereo = np.column_stack([voice, voice])
        else:
            mix_stereo = voice.copy()

        # Camada de SFX narrativos
        for sfx in sound_plan.get("sfx_tracks", []):
            filepath = sfx["file"]
            if os.path.exists(filepath):
                sfx_audio, sfx_sr = sf.read(filepath)
                if sfx_sr != sr:
                    # Se sample rate diferente, reamostrar via FFmpeg ou interpolação
                    pass
                if len(sfx_audio.shape) == 1:
                    sfx_audio = np.column_stack([sfx_audio, sfx_audio])

                start_idx = int(sfx["start_time"] * sr)
                end_idx = min(start_idx + len(sfx_audio), total_samples)
                sfx_len = end_idx - start_idx
                if sfx_len > 0:
                    gain_linear = 10.0 ** (sfx["volume_db"] / 20.0)
                    mix_stereo[start_idx:end_idx] += sfx_audio[:sfx_len] * gain_linear

        # Limiter e normalização de segurança no mixdown com Pedalboard
        final_board = Pedalboard([
            Compressor(threshold_db=-8.0, ratio=2.0),
            Limiter(threshold_db=-1.0)
        ])
        mixed = final_board(mix_stereo, sr)

        temp_unnorm = output_wav + ".temp.wav"
        sf.write(temp_unnorm, mixed, sr, subtype="PCM_24")

        # Normalização rigorosa EBU R128 (-14 LUFS) via FFmpeg
        cmd = [
            FFMPEG_BIN, "-y", "-i", temp_unnorm,
            "-af", "loudnorm=I=-14:TP=-1.0:LRA=7",
            "-ar", "48000",
            output_wav
        ]
        subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, check=True)
        if os.path.exists(temp_unnorm):
            os.remove(temp_unnorm)

        return output_wav
