"""
PALÁCIO BRAND CONFIGURATION (v7.0)
Configuração Central Obrigatória da Identidade Audiovisual.

REGRA INEGOCIÁVEL:
A marca principal de todos os vídeos é PALÁCIO ACOLHIMENTO.
Palácio.pro identifica o ecossistema técnico/desenvolvimento,
mas é PROIBIDO utilizá-lo como assinatura, marca d'água ou badge visual nos vídeos.
"""

from typing import Dict, Any, List

BRAND_REGISTRY: Dict[str, Dict[str, Any]] = {
    "palacio-acolhimento": {
        "brand_id": "palacio-acolhimento",
        "brand_name": "Palácio Acolhimento",
        "brand_display": "PALÁCIO ACOLHIMENTO",
        "brand_mode": "default",
        "handle": "@palacioacolhimento",
        "website": "palacioacolhimento.com.br",
        "slogan": "A recuperação continua na forma de viver.",
        "subtext": "Acolhimento Familiar & Tratamento Humanizado",
        "monogram": "P",
        "colors": {
            "primary": "#074B32",      # Verde Esmeralda Institucional
            "primary_light": "#0D6B4A",
            "gold": "#D4AF37",         # Dourado Realce
            "gold_light": "#F3E5AB",
            "dark_bg": "#060A08",      # Preto Carvão Profundo
            "text_white": "#FFFFFF"
        },
        "forbidden_signatures": [
            "palácio.pro",
            "palacio.pro",
            "palácio ponto pro",
            "palacio ponto pro",
            "palácio ai",
            "palacio ai",
            "@palacio.pro",
            "@palacio_pro"
        ]
    },
    "mais-um-passo-saude": {
        "brand_id": "mais-um-passo-saude",
        "brand_name": "+1 Passo Saúde",
        "brand_display": "+1 PASSO SAÚDE",
        "brand_mode": "health",
        "handle": "@maisumpassosaude",
        "website": "maisumpassosaude.com.br",
        "slogan": "Cuidando de cada passo da sua saúde.",
        "subtext": "Saúde Integrativa & Prevenção",
        "monogram": "+1",
        "colors": {
            "primary": "#1E3A8A",
            "primary_light": "#3B82F6",
            "gold": "#10B981",
            "gold_light": "#6EE7B7",
            "dark_bg": "#050B14",
            "text_white": "#FFFFFF"
        },
        "forbidden_signatures": [
            "palácio.pro",
            "palacio.pro",
            "palácio ai",
            "@palacio.pro"
        ]
    }
}

DEFAULT_BRAND_ID = "palacio-acolhimento"

def get_brand_config(brand_id: str = DEFAULT_BRAND_ID) -> Dict[str, Any]:
    """Retorna o dicionário de configuração da marca selecionada."""
    if brand_id not in BRAND_REGISTRY:
        raise ValueError(f"Marca '{brand_id}' não reconhecida. Use uma das marcas registradas: {list(BRAND_REGISTRY.keys())}")
    return BRAND_REGISTRY[brand_id]

def validate_brand_integrity(text_or_props: Any, brand_id: str = DEFAULT_BRAND_ID) -> List[str]:
    """
    Verifica se alguma assinatura proibida (ex: Palácio.pro) foi inserida indevidamente
    em textos, badges, títulos ou propriedades visuais do vídeo.
    Retorna uma lista de violações encontradas. Se vazia, validação passou.
    """
    config = get_brand_config(brand_id)
    forbidden = config["forbidden_signatures"]
    violations = []

    def scan_string(val: str, path: str = ""):
        val_lower = val.lower()
        for forbidden_term in forbidden:
            if forbidden_term in val_lower:
                violations.append(f"Violação de marca em '{path}': termo proibido '{forbidden_term}' encontrado no texto '{val}'")

    def walk(obj: Any, path: str = "root"):
        if isinstance(obj, str):
            scan_string(obj, path)
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k in ("forbidden_signatures", "forbiddenSignatures"):
                    continue
                walk(v, f"{path}.{k}")
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                walk(item, f"{path}[{i}]")

    walk(text_or_props)
    return violations
