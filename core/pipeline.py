"""
PALÁCIO VÍDEOS PRO 7.0 — MASTER PIPELINE
Orquestrador Central e Linha de Produção Audiovisual Unificada.

Conecta todos os motores:
1. SMART EDITOR: Análise acústica, alinhamento palavra por palavra, VAD e transcrição.
2. RETENTION DIRECTOR: Curva de retenção, ganchos e punch-ins dramáticos.
3. CINEMATIC DIRECTOR: Color grading cinematográfico, B-roll contextual e transições.
4. SOUND DIRECTOR: Masterização vocal via Spotify Pedalboard, SFX e EBU R128 (-14.0 LUFS).
5. RENDER ENGINE: Renderização programática via Remotion (1080x1920 vertical 9:16).
6. QUALITY DIRECTOR: Validação estrita de marca (Palácio Acolhimento), zonas seguras e inspeção de frames.
"""

import os
import sys
import json
import argparse
import subprocess
from typing import Dict, Any, Optional

BASE_DIR = "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio"
sys.path.insert(0, BASE_DIR)

from core.brand_config import get_brand_config, validate_brand_integrity, DEFAULT_BRAND_ID
from core.social_safe_zones import get_safe_zone, validate_subtitle_position, DEFAULT_PROFILE
from core.smart_editor import PalácioSmartEditor
from core.retention_director import PalácioRetentionDirector
from core.cinematic_director import PalácioCinematicDirector
from core.sound_director import PalácioSoundDirector
from core.quality_director import PalácioQualityDirector

REMOTION_DIR = os.path.join(BASE_DIR, "remotion")
DOWNLOADS_DIR = "/Users/palacio.pro/Downloads"


class PalácioVideosPipeline:
    def __init__(self, brand_id: str = DEFAULT_BRAND_ID, profile_name: str = DEFAULT_PROFILE):
        self.brand_id = brand_id
        self.brand_config = get_brand_config(brand_id)
        self.profile_name = profile_name
        self.safe_zone = get_safe_zone(profile_name)

        # Inicialização dos 5 Motores
        self.smart_editor = PalácioSmartEditor()
        self.retention_director = PalácioRetentionDirector()
        self.cinematic_director = PalácioCinematicDirector(downloads_dir=DOWNLOADS_DIR)
        self.sound_director = PalácioSoundDirector()
        self.quality_director = PalácioQualityDirector(brand_id=self.brand_id, platform_profile=self.profile_name)

    def create_project_plan(
        self,
        video_path: str,
        title: str,
        category: str,
        start_sec: float,
        duration_sec: float,
        words_data: list,
        style: str = "cinematic",
        hook_subtitle: str = ""
    ) -> Dict[str, Any]:
        """
        Gera o plano editorial estruturado compartilhado entre todos os motores.
        """
        # 1. Retention Director: Câmera e Enquadramento
        retention_cues = self.retention_director.analyze_retention_curve(words_data, duration_sec, style=style)

        # 2. Cinematic Director: Color Grading e B-Roll
        color_filter = self.cinematic_director.get_color_filter(style=style)
        broll_cues = self.cinematic_director.plan_broll_cues(words_data, duration_sec) if style == "cinematic" else []

        # 3. Sound Director: Sound Plan com SFX Narrativos
        sound_plan = self.sound_director.generate_sound_plan({"words": words_data}, duration_sec, style=style)

        # 4. Social Safe Zones: Configuração de Legendas
        subtitle_config = {
            "bottom_px": self.safe_zone["subtitle_bottom_px"],
            "max_width": self.safe_zone["max_subtitle_width"],
            "target_y": self.safe_zone["subtitle_default_y"],
            "safe_range": [self.safe_zone["subtitle_y_min"], self.safe_zone["subtitle_y_max"]]
        }

        # 5. Validação de Marca Pre-flight
        props_to_validate = {
            "title": title,
            "category": category,
            "hook_subtitle": hook_subtitle,
            "brand": self.brand_config
        }
        violations = validate_brand_integrity(props_to_validate, self.brand_id)
        if violations:
            raise ValueError(f"FALHA PRE-FLIGHT DE MARCA: {violations}")

        project_plan = {
            "pipeline_version": "7.0",
            "brand": self.brand_config,
            "platform_profile": self.profile_name,
            "video_source": video_path,
            "title": title,
            "category": category,
            "hook_subtitle": hook_subtitle,
            "timing": {
                "start_sec": start_sec,
                "duration_sec": duration_sec,
                "fps": 30,
                "resolution": "1080x1920"
            },
            "retention": {
                "cues": retention_cues
            },
            "cinematic": {
                "color_filter": color_filter,
                "broll": broll_cues
            },
            "sound": sound_plan,
            "subtitles": subtitle_config
        }

        return project_plan

    def render_remotion_composition(self, composition_id: str, output_path: str, concurrency: int = 7) -> Dict[str, Any]:
        """
        Renderiza a composição Remotion com medição de performance e captura de logs.
        """
        print(f"\n[RENDER] Renderizando composição '{composition_id}' -> '{output_path}' (concorrência: {concurrency})...")
        cmd = [
            "npx", "remotion", "render",
            composition_id,
            output_path,
            f"--concurrency={concurrency}"
        ]
        res = subprocess.run(cmd, cwd=REMOTION_DIR, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Erro no Remotion:\n{res.stderr}")
            raise RuntimeError(f"Falha ao renderizar Remotion ({composition_id}): {res.stderr}")

        print(f"[RENDER OK] Composição renderizada com sucesso: {output_path}")

        # Executar Auditoria de Qualidade com Quality Director
        audit = self.quality_director.audit_video(output_path, composition_props={"brand": self.brand_config})
        return audit


def run_cli():
    parser = argparse.ArgumentParser(description="Palácio Vídeos Pro 7.0 CLI")
    parser.add_argument("--composition", type=str, required=True, help="ID da composição Remotion")
    parser.add_argument("--output", type=str, required=True, help="Caminho do arquivo MP4 final")
    parser.add_argument("--brand", type=str, default=DEFAULT_BRAND_ID, help="ID da marca")
    parser.add_argument("--profile", type=str, default=DEFAULT_PROFILE, help="Perfil de rede social")
    args = parser.parse_args()

    pipeline = PalácioVideosPipeline(brand_id=args.brand, profile_name=args.profile)
    audit = pipeline.render_remotion_composition(args.composition, args.output)
    print("\n--- AUDITORIA FINAL DO QUALITY DIRECTOR ---")
    print(json.dumps(audit, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_cli()
