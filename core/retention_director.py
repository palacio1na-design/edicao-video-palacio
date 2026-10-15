"""
PALÁCIO RETENTION DIRECTOR (v7.0)
Direção de Ritmo, Enquadramento Dinâmico, Punch-in e Curva de Retenção.

Analisa a transcrição palavra por palavra, a densidade de fala, pausas e termos
emocionais para calcular os momentos ideais de punch-in, reset de câmera e ênfase visual.
"""

from typing import List, Dict, Any

class PalácioRetentionDirector:
    def __init__(self):
        pass

    def analyze_retention_curve(self, words: List[Dict[str, Any]], total_duration: float, style: str = "cinematic") -> List[Dict[str, Any]]:
        """
        Calcula movimentos de câmera e punch-ins baseados na intensidade dramática
        e nos marcos narrativos da fala.
        """
        if not words:
            return [{"start_sec": 0.0, "end_sec": total_duration, "scale": 1.05, "type": "default"}]

        cues = []
        
        # 1. Gancho Inicial (0s até término da primeira frase forte ~3.0s a 4.0s)
        first_pause = next((w["end"] for w in words if w["end"] >= 2.5 and any(w["word"].endswith(p) for p in [".", ",", "!"])), 3.5)
        hook_end = min(round(first_pause, 2), 4.2)

        cues.append({
            "start_sec": 0.0,
            "end_sec": hook_end,
            "scale": 1.05,
            "focus": "center",
            "type": "hook_establishing",
            "justification": "Fixação de gancho inicial limpo sem distrações visuais excessivas."
        })

        # Termos de alta dor/impacto emocional que justificam punch-in de intimidade
        tension_keywords = {"morreu", "perdi", "droga", "doença", "perder", "sozinho", "chorando", "dor", "rua"}
        
        # 2. Rastrear momentos de tensão
        current_time = hook_end
        while current_time < total_duration - 3.5:
            # Procurar palavra de tensão nos próximos 6 segundos
            window_words = [w for w in words if current_time <= w["start"] < current_time + 6.0]
            tension_found = any(any(k in w["word"].lower() for k in tension_keywords) for w in window_words)

            if tension_found and style == "cinematic":
                next_seg_dur = min(6.5, (total_duration - 3.0) - current_time)
                cues.append({
                    "start_sec": current_time,
                    "end_sec": round(current_time + next_seg_dur, 2),
                    "scale": 1.15,
                    "focus": "upper_third",
                    "type": "punch_in_drama",
                    "justification": "Aproximação de intimidade e confronto emocional durante confissão de dor."
                })
                current_time += next_seg_dur
            else:
                next_seg_dur = min(5.0, (total_duration - 3.0) - current_time)
                scale = 1.08 if style == "cinematic" else 1.14
                cues.append({
                    "start_sec": current_time,
                    "end_sec": round(current_time + next_seg_dur, 2),
                    "scale": scale,
                    "focus": "center",
                    "type": "medium_engagement",
                    "justification": "Manutenção de ritmo visual orgânico."
                })
                current_time += next_seg_dur

        # 3. Fechamento Reflexivo / Outro
        if current_time < total_duration:
            cues.append({
                "start_sec": current_time,
                "end_sec": total_duration,
                "scale": 1.03,
                "focus": "center",
                "type": "resolution_pull_out",
                "justification": "Recuo sutil de câmera para transição de encerramento institucional."
            })

        return cues
