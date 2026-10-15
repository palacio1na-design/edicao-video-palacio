"""
PALÁCIO CINEMATIC DIRECTOR (v6.0)
Color Grading, Textura Cinematográfica, Vinheta e Profundidade Visual.
"""

class PalácioCinematicDirector:
    def __init__(self):
        pass

    def get_color_filter(self, style="cinematic"):
        """
        Retorna a cadeia de filtros FFmpeg para color grading cinematográfico autoral.
        """
        if style == "cinematic":
            # Estilo Cinematográfico Emocional:
            # - Contraste elegante e sombras levemente esmeralda/teal
            # - Pele quente e natural protegida
            # - Vinheta sutil para profundidade e intimismo
            filters = [
                "eq=contrast=1.12:brightness=-0.01:saturation=0.94",
                "colorbalance=rs=-0.02:gs=0.04:bs=0.01:rm=0.03:gm=0.02:bm=-0.02:rh=0.02:gh=0.01:bh=-0.01",
                "vignette=angle=PI/4"
            ]
            return ",".join(filters)
        else:
            # Estilo Dinâmico / Motion Design:
            # - Contraste vivo, cores acentuadas, realce em tons dourados
            filters = [
                "eq=contrast=1.15:brightness=0.01:saturation=1.08",
                "colorbalance=rm=0.02:gm=0.01:bm=-0.02:rh=0.03:gh=0.02:bh=-0.02",
                "vignette=angle=PI/5"
            ]
            return ",".join(filters)
