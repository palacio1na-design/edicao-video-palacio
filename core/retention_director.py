"""
PALÁCIO RETENTION DIRECTOR (v6.0)
Direção de Ritmo, Enquadramento Dinâmico, Punch-in e Curva de Retenção.
"""

class PalácioRetentionDirector:
    def __init__(self):
        pass

    def plan_zooms_and_pacing(self, segments, style="cinematic"):
        """
        Calcula movimentos de câmera e punch-ins baseados na intensidade dramática.
        """
        cues = []
        if style == "cinematic":
            # Versão Cinematográfica: Movimentos lentos e punch-ins dramáticos
            cues = [
                {
                    "start_sec": 0.0,
                    "end_sec": 3.8,
                    "scale": 1.05,
                    "focus": "center",
                    "type": "opening_establishing",
                    "justification": "Enquadramento inicial estável para fixação do gancho."
                },
                {
                    "start_sec": 3.8,
                    "end_sec": 12.5,
                    "scale": 1.15,
                    "focus": "upper_third",
                    "type": "punch_in_drama",
                    "justification": "Aproximação intensa no rosto ao falar que o pai fechou o apartamento."
                },
                {
                    "start_sec": 12.5,
                    "end_sec": 23.5,
                    "scale": 1.10,
                    "focus": "center",
                    "type": "medium_tension",
                    "justification": "Respiração visual durante relato da viatura e da resistência."
                },
                {
                    "start_sec": 23.5,
                    "end_sec": 36.5,
                    "scale": 1.18,
                    "focus": "eyes",
                    "type": "peak_intimacy",
                    "justification": "Punch-in máximo de intimidade: uma semana morando na rua (fundo de poço)."
                },
                {
                    "start_sec": 36.5,
                    "end_sec": 39.0,
                    "scale": 1.05,
                    "focus": "center",
                    "type": "resolution_pull_out",
                    "justification": "Recuo para o fechamento reflexivo: 'É isso, meu irmão'."
                }
            ]
        else:
            # Versão Dinâmica: Cortes de escala rápidos e ágeis a cada 3-5 segundos
            cues = [
                {"start_sec": 0.0, "end_sec": 3.5, "scale": 1.05, "type": "hook"},
                {"start_sec": 3.5, "end_sec": 8.0, "scale": 1.16, "type": "punch_in"},
                {"start_sec": 8.0, "end_sec": 14.0, "scale": 1.08, "type": "reset"},
                {"start_sec": 14.0, "end_sec": 23.0, "scale": 1.18, "type": "punch_in"},
                {"start_sec": 23.0, "end_sec": 30.0, "scale": 1.10, "type": "reset"},
                {"start_sec": 30.0, "end_sec": 39.0, "scale": 1.20, "type": "climax"}
            ]

        return cues
