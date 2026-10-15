"""
PALÁCIO CINEMATIC DIRECTOR (v7.0)
Color Grading, Textura Cinematográfica, Transições e Curadoria Contextual de B-Roll.

Seleciona B-roll contextual baseado na narrativa semântica, assegurando que
o orador seja mantido em primeiro plano em falas centrais, aplicando inserções
apenas nos momentos em que a imagem ilustrativa aprofunda o impacto emocional.
"""

import os
from typing import List, Dict, Any

class PalácioCinematicDirector:
    def __init__(self, downloads_dir: str = "/Users/palacio.pro/Downloads"):
        self.downloads_dir = downloads_dir
        self.broll_catalog = self._scan_broll_catalog()

    def _scan_broll_catalog(self) -> Dict[str, str]:
        """Catálogo de B-Rolls locais verificados no disco."""
        known_files = {
            "mae_familia_droga": "Woman_discusses_sons_drug_use_3850e9bf96.mp4",
            "solidao_abandono": "Woman_leaves_man_in_silence_ba37e79a08.mp4",
            "familia_telefone": "Woman_arriving_and_placing_phone_202608081956.mp4",
            "reflexao_noite": "gemini_generated_video_80718F6A.MP4",
            "reflexao_chuva": "gemini_generated_video_9E611192.MP4",
            "clinica_recomeco": "Conheça a Clínica Vida Serena | Um lugar para recomeçar.mp4"
        }
        catalog = {}
        for key, fname in known_files.items():
            full_path = os.path.join(self.downloads_dir, fname)
            if os.path.exists(full_path):
                catalog[key] = full_path
        return catalog

    def get_color_filter(self, style: str = "cinematic") -> str:
        """Retorna cadeia de filtros FFmpeg para color grading cinematográfico."""
        if style == "cinematic":
            filters = [
                "eq=contrast=1.12:brightness=-0.01:saturation=1.02",
                "colorbalance=rm=0.02:gm=0.01:bm=-0.01"
            ]
            return ",".join(filters)
        else:
            filters = [
                "eq=contrast=1.15:brightness=0.01:saturation=1.08",
                "colorbalance=rm=0.03:gm=0.01:bm=-0.02"
            ]
            return ",".join(filters)

    def plan_broll_cues(self, words: List[Dict[str, Any]], total_duration: float) -> List[Dict[str, Any]]:
        """
        Analisa a transcrição e identifica se há trecho emocional onde B-roll enriquece a cena.
        Regra de Ouro: Nunca inserir B-roll nos primeiros 3.5s (gancho) nem no encerramento (últimos 3s).
        """
        broll_cues = []
        if not self.broll_catalog:
            return broll_cues

        # Gatilho de Família/Mãe Sofrendo
        family_keywords = {"mãe", "familia", "família", "chorando", "filho"}
        for w in words:
            word_clean = w["word"].lower().strip(".,!?:")
            if word_clean in family_keywords:
                w_start = float(w["start"])
                # Verificar se está na janela adequada (entre 12s e duration - 4s)
                if 12.0 <= w_start <= (total_duration - 4.5):
                    broll_file = self.broll_catalog.get("mae_familia_droga")
                    if broll_file:
                        broll_cues.append({
                            "type": "broll_cutaway",
                            "name": "Mãe Sofrendo / Impacto Familiar",
                            "file": broll_file,
                            "start_sec": max(14.0, round(w_start - 0.5, 2)),
                            "duration_sec": 3.8,
                            "opacity": 0.88,
                            "blend_mode": "crossfade",
                            "justification": f"Ilustração contextual da dor da família ao mencionar '{word_clean}'."
                        })
                        break  # No máximo 1 B-roll pontual em vídeos curtos (< 35s) para não fragmentar a atenção

        return broll_cues
