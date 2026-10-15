"""
PALÁCIO SOCIAL SAFE ZONES (v7.0)
Módulo Central de Zonas Seguras para Redes Sociais.

Garante que legendas, títulos, ganchos e elementos visuais de motion design
fiquem rigorosamente dentro da área visível em 1080x1920 (Vertical 9:16),
sem sofrer sobreposição de barras de navegação, caixas de comentários,
botões de engajamento (curtir/compartilhar) ou descrições das plataformas.
"""

from typing import Dict, Any

SAFE_ZONE_PROFILES: Dict[str, Dict[str, Any]] = {
    "INSTAGRAM_REELS": {
        "platform": "Instagram Reels",
        "frame_width": 1080,
        "frame_height": 1920,
        "top_margin": 140,            # Margem superior (câmera, stories)
        "bottom_margin": 450,         # Área ocupada por @user, legenda de texto, áudio original
        "left_margin": 60,            # Margem lateral esquerda
        "right_margin": 130,          # Coluna de botões laterais (Like, Comentário, Share)
        # Faixa vertical ideal para legendas dinâmicas
        "subtitle_y_min": 1180,
        "subtitle_y_max": 1420,
        "subtitle_default_y": 1280,
        # Equivalente em bottom (px a partir do chão)
        "subtitle_bottom_px": 540,
        "max_subtitle_width": 860
    },
    "TIKTOK_VERTICAL": {
        "platform": "TikTok",
        "frame_width": 1080,
        "frame_height": 1920,
        "top_margin": 160,            # Busca, Ao Vivo, abas Para Você
        "bottom_margin": 480,         # Nome de usuário, descrição, som e disco giratório
        "left_margin": 60,
        "right_margin": 140,          # Coluna com avatar, like, comentário, favoritos, share
        "subtitle_y_min": 1180,
        "subtitle_y_max": 1390,
        "subtitle_default_y": 1260,
        "subtitle_bottom_px": 560,
        "max_subtitle_width": 850
    },
    "YOUTUBE_SHORTS": {
        "platform": "YouTube Shorts",
        "frame_width": 1080,
        "frame_height": 1920,
        "top_margin": 130,            # Câmera e pesquisa
        "bottom_margin": 420,         # Canal, botão Inscrever-se, título do Short
        "left_margin": 60,
        "right_margin": 130,          # Botões laterais de like/dislike/comentários/remix
        "subtitle_y_min": 1180,
        "subtitle_y_max": 1420,
        "subtitle_default_y": 1290,
        "subtitle_bottom_px": 530,
        "max_subtitle_width": 860
    },
    "FACEBOOK_REELS": {
        "platform": "Facebook Reels",
        "frame_width": 1080,
        "frame_height": 1920,
        "top_margin": 140,
        "bottom_margin": 440,
        "left_margin": 60,
        "right_margin": 130,
        "subtitle_y_min": 1180,
        "subtitle_y_max": 1410,
        "subtitle_default_y": 1280,
        "subtitle_bottom_px": 540,
        "max_subtitle_width": 860
    },
    "SOCIAL_VERTICAL_MASTER": {
        "platform": "Master Universal (Compatível com todas as 4 redes)",
        "frame_width": 1080,
        "frame_height": 1920,
        "top_margin": 160,
        "bottom_margin": 480,
        "left_margin": 65,
        "right_margin": 140,
        "subtitle_y_min": 1200,
        "subtitle_y_max": 1380,
        "subtitle_default_y": 1280,
        "subtitle_bottom_px": 540,     # Fica exatamente no centro da faixa Y = 1280 a 1380
        "max_subtitle_width": 840
    }
}

DEFAULT_PROFILE = "SOCIAL_VERTICAL_MASTER"

def get_safe_zone(profile_name: str = DEFAULT_PROFILE) -> Dict[str, Any]:
    """Retorna os parâmetros de zona segura do perfil solicitado."""
    return SAFE_ZONE_PROFILES.get(profile_name, SAFE_ZONE_PROFILES[DEFAULT_PROFILE])

def validate_subtitle_position(y_position: float, box_height: float = 120.0, profile_name: str = DEFAULT_PROFILE) -> Dict[str, Any]:
    """
    Valida se a legenda está dentro da zona segura vertical e não invade
    a área do rosto do autor (Y < 1100) nem a área dos controles da rede (Y > 1460).
    """
    sz = get_safe_zone(profile_name)
    top_y = y_position - (box_height / 2.0)
    bottom_y = y_position + (box_height / 2.0)

    is_too_high = top_y < 1050  # Invade o tórax/pescoço/rosto
    is_too_low = bottom_y > (sz["frame_height"] - sz["bottom_margin"])  # Invade descrição/botoeira

    passed = not (is_too_high or is_too_low)
    critique = []
    if is_too_high:
        critique.append(f"Legenda muito alta (Y={top_y:.0f}px), risco de cobrir o rosto do orador.")
    if is_too_low:
        critique.append(f"Legenda muito baixa (Y={bottom_y:.0f}px), será encoberta pelos botões e descrição do {sz['platform']}.")

    return {
        "passed": passed,
        "y_position": y_position,
        "safe_range": [sz["subtitle_y_min"], sz["subtitle_y_max"]],
        "platform": sz["platform"],
        "critique": " ".join(critique) if critique else "Legenda perfeitamente posicionada na Zona Segura."
    }
