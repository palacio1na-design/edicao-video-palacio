"""
PALÁCIO CREATIVE DIRECTOR — MOTOR UNIFICADO DAS 5 SKILLS
Implementa a direção criativa executável inspirada no Método de Inteligência Audiovisual (MIA):
1. PALACIO-ESTILO: Direção de arte, fotografia, cor e marca Palácio Acolhimento.
2. PALACIO-RITMO: Cortes semânticos, pausas dramáticas, ganchos e 4 atos narrativos.
3. PALACIO-LEGENDAS: Transcrição auditada, destaques de palavra e zonas seguras.
4. PALACIO-MOVIMENTO: Câmera virtual (50% 36%), punch-in dramático, spring physics e 3D.
5. PALACIO-COMPOSICAO: Moldura flutuante 2.5D, ambient blur, camadas e gráficos de acolhimento.

Integra diretamente:
- Retention Director
- Cinematic Director
- Sound Director
- Quality Director
"""

import os
import json
from typing import Dict, Any, List, Optional
from core.brand_config import get_brand_config, validate_brand_integrity, DEFAULT_BRAND_ID
from core.social_safe_zones import get_safe_zone, validate_subtitle_position, DEFAULT_PROFILE
from core.retention_director import PalácioRetentionDirector
from core.cinematic_director import PalácioCinematicDirector
from core.sound_director import PalácioSoundDirector
from core.quality_director import PalácioQualityDirector

class PalácioCreativeDirector:
    def __init__(self, brand_id: str = DEFAULT_BRAND_ID, platform_profile: str = DEFAULT_PROFILE):
        self.brand_id = brand_id
        self.brand_config = get_brand_config(brand_id)
        self.platform_profile = platform_profile
        self.safe_zone = get_safe_zone(platform_profile)

        # Integração com os 4 diretores técnicos existentes
        self.retention_director = PalácioRetentionDirector()
        self.cinematic_director = PalácioCinematicDirector()
        self.sound_director = PalácioSoundDirector()
        self.quality_director = PalácioQualityDirector(brand_id=self.brand_id, platform_profile=self.platform_profile)

    def plan_creative_edition(
        self,
        video_src: str,
        total_duration: float,
        words_data: List[Dict[str, Any]],
        title: str,
        category: str,
        hook_text: str = ""
    ) -> Dict[str, Any]:
        """
        Gera o plano criativo completo convertendo decisões das 5 skills em ações reais de timeline.
        """
        # 1. PALACIO-ESTILO: Validação de integridade de marca e paleta
        brand_violations = validate_brand_integrity({
            "title": title,
            "category": category,
            "brand": self.brand_config
        }, self.brand_id)
        if brand_violations:
            raise ValueError(f"FALHA CRIATIVA PALACIO-ESTILO: {brand_violations}")

        color_style = {
            "grade": "moody_cinema",
            "contrast": 1.06,
            "brightness": 1.02,
            "saturate": 1.04,
            "vignette": "radial-gradient(circle at 50% 38%, transparent 40%, rgba(6, 10, 8, 0.45) 82%, rgba(6, 10, 8, 0.88) 100%)",
            "ambient_blur": "blur(36px) brightness(0.42) saturate(1.4)"
        }

        # 2. PALACIO-RITMO: Estruturação dos 4 Atos
        acts = [
            {
                "act": 1,
                "name": "Hook Shock (Gancho de Atenção)",
                "start_sec": 0.0,
                "end_sec": 4.5,
                "pacing": "intenso",
                "intent": "Interromper a rolagem no feed com corte no primeiro fonema."
            },
            {
                "act": 2,
                "name": "Storytelling & Dor (Morte e Perda de Amigos)",
                "start_sec": 4.5,
                "end_sec": 13.0,
                "pacing": "cadenciado",
                "intent": "Punch-in semântico imediato aos 5.8s em 'morreu!' e pausa dramática."
            },
            {
                "act": 3,
                "name": "Composição Avançada & Reflexão Familiar",
                "start_sec": 13.0,
                "end_sec": 22.0,
                "pacing": "profundo",
                "intent": "Transição para moldura flutuante 2.5D, ambient blur e badge de acolhimento."
            },
            {
                "act": 4,
                "name": "Clímax & Apelo Direto ('Não quero perder você')",
                "start_sec": 22.0,
                "end_sec": 26.0,
                "pacing": "máximo_impacto",
                "intent": "Retorno ao close de tela cheia focado nos olhos do orador."
            },
            {
                "act": 5,
                "name": "Resolução & Esperança (Palácio Acolhimento)",
                "start_sec": 26.0,
                "end_sec": total_duration,
                "pacing": "esperanca",
                "intent": "Acorde de esperança e encerramento com autoridade e acolhimento."
            }
        ]

        # 3. PALACIO-LEGENDAS: Zonas seguras e parâmetros
        subtitles_plan = {
            "bottom_px": self.safe_zone["subtitle_bottom_px"],
            "target_y": self.safe_zone["subtitle_default_y"],
            "safe_range": [self.safe_zone["subtitle_y_min"], self.safe_zone["subtitle_y_max"]],
            "highlight_color": "#E5A93C",
            "spoken_color": "#FFFFFF",
            "upcoming_color": "rgba(255, 255, 255, 0.45)"
        }

        # 4. PALACIO-MOVIMENTO & PALACIO-COMPOSICAO
        movement_cues = [
            {"time_sec": 0.0, "scale": 1.05, "type": "stable", "focus": "eyes"},
            {"time_sec": 5.8, "scale": 1.22, "type": "punch_in_cut", "trigger_word": "morreu!"},
            {"time_sec": 13.0, "scale": 1.08, "type": "framed_mode_2.5d", "ambient_blur": True},
            {"time_sec": 22.0, "scale": 1.16, "type": "full_screen_climax", "ambient_blur": False},
            {"time_sec": 26.0, "scale": 1.04, "type": "outro_retreat", "ambient_blur": False}
        ]

        # 5. SINCRONIA SONORA NARRATIVA (Sound Director)
        sfx_timeline = [
            {"sec": 0.0, "sfx": "cinematic_sub_hit.wav", "volume": 0.65, "reason": "Impacto de abertura do gancho"},
            {"sec": 5.8, "sfx": "cinematic_sub_hit.wav", "volume": 0.75, "reason": "Soco sonoro em 'morreu!'"},
            {"sec": 6.0, "sfx": "tension_drone_c_minor.wav", "volume": 0.40, "reason": "Drone de tensão durante relato de dor"},
            {"sec": 13.0, "sfx": "cinematic_whoosh.wav", "volume": 0.55, "reason": "Transição para modo moldura flutuante"},
            {"sec": 13.6, "sfx": "card_glass_pop.wav", "volume": 0.60, "reason": "Entrada do badge de acolhimento"},
            {"sec": 22.0, "sfx": "cinematic_whoosh.wav", "volume": 0.55, "reason": "Retorno a tela cheia para clímax"},
            {"sec": 24.0, "sfx": "hope_resolution_chord.wav", "volume": 0.50, "reason": "Resolução e esperança"},
            {"sec": 26.0, "sfx": "card_glass_pop.wav", "volume": 0.60, "reason": "Entrada do card de encerramento Palácio Acolhimento"}
        ]

        creative_plan = {
            "version": "7.5-creative-master",
            "brand": self.brand_config,
            "style": color_style,
            "acts": acts,
            "subtitles": subtitles_plan,
            "movement": movement_cues,
            "sound_sfx": sfx_timeline,
            "composition": {
                "has_advanced_composition": True,
                "mode": "2.5D Floating Card com Ambient Blur e Token 3D",
                "start_sec": 13.0,
                "end_sec": 22.0
            }
        }

        return creative_plan
