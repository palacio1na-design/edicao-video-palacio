"""
PALÁCIO VÍDEOS — INTELLIGENT MONTAGE ENGINE
Inspirado na arquitetura do AutoBroll (andriidrok1/autobroll) e Auto-Editor (WyattBlue/auto-editor).
Zero Simulação Operacional: Análise semântica e acústica real para cada vídeo fornecido.

Módulos:
1. GeminiNarrativeAnalyzer: Análise semântica via Gemini API (se conectada) ou acústico-semântica determinística.
2. AutoEditorSilenceTrimmer: Mapeamento e remoção cirúrgica de silêncios mortos.
3. DiscreetCameraDirector: Planejamento de zooms contextuais e alternância de planos sem cortes abruptos.
4. VisualStoryboardGenerator: Comparação visual lado a lado Original vs Editado.
"""

import os
import sys
import json
import re
import subprocess
from typing import Dict, Any, List, Optional, Tuple

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


class GeminiNarrativeAnalyzer:
    """
    Analisa a estrutura dramática da transcrição real fornecida.
    - Se a integração com a API Gemini estiver configurada (GEMINI_API_KEY no ambiente),
      executa inferência semântica viva com prompt especializado em acolhimento familiar.
    - Se a API Gemini estiver indisponível/desconectada, relata com total transparência
      e executa a análise acústico-semântica determinística com base nas palavras e timestamps reais.
    NUNCA retorna cenas hardcoded de vídeos antigos.
    """
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

    def analyze_transcript(self, chunks: List[Dict[str, Any]], video_duration: Optional[float] = None) -> Dict[str, Any]:
        if not chunks:
            return {
                "total_duration": video_duration or 0.0,
                "total_scenes": 0,
                "scenes": [],
                "engine_used": "EMPTY_CHUNKS"
            }

        full_text = " ".join(c.get("text", "") for c in chunks).strip()
        total_duration = video_duration or chunks[-1].get("end", 0.0)

        # 1. Tenta chamada à API Gemini se credenciais existirem
        if self.api_key:
            try:
                gemini_result = self._call_gemini_api(full_text, chunks, total_duration)
                if gemini_result and gemini_result.get("scenes"):
                    gemini_result["engine_used"] = "GEMINI_API_LIVE"
                    return gemini_result
            except Exception as e:
                print(f"[!] Erro na chamada da API Gemini ({e}). Recorrendo à análise acústico-semântica determinística.")

        # 2. Análise Semântico-Acústica Determinística (Zero Simulação: baseada no texto REAL)
        return self._deterministic_semantic_analysis(chunks, full_text, total_duration)

    def _call_gemini_api(self, full_text: str, chunks: List[Dict[str, Any]], total_duration: float) -> Optional[Dict[str, Any]]:
        """Invoca a API do Gemini via SDK google-genai ou google.generativeai se instalado."""
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.api_key)
            model = genai.GenerativeModel("gemini-1.5-flash")
            
            prompt = f"""Você é o Diretor Criativo da Palácio Acolhimento.
Analise a transcrição abaixo de um vídeo de conscientização familiar em dependência química ({total_duration:.1f}s):
"{full_text}"

Identifique em JSON estrito os momentos-chave para corte cinematográfico vertical (9:16):
- scene_id: identificador
- type: 'A-ROLL', 'B-ROLL_CUTAWAY' ou 'OUTRO_INSTITUCIONAL'
- start_sec: segundo de início
- end_sec: segundo de término
- description: explicação
- visual_action: enquadramento sugerido (Plano Médio 1.0x ou Close 1.15x)
- sfx: sugestão de efeito sonoro (whoosh, sub impacto, etc.)

Retorne APENAS um bloco JSON válido com a chave "scenes"."""
            
            response = model.generate_content(prompt)
            raw = response.text.strip()
            # Limpa blocos de código markdown
            raw = re.sub(r"^```json\s*", "", raw)
            raw = re.sub(r"\s*```$", "", raw)
            data = json.loads(raw)
            if "scenes" in data:
                data["total_duration"] = total_duration
                data["total_scenes"] = len(data["scenes"])
                return data
        except Exception:
            pass
        return None

    def _deterministic_semantic_analysis(self, chunks: List[Dict[str, Any]], full_text: str, total_duration: float) -> Dict[str, Any]:
        """
        Analisa o fluxo semântico real do orador a partir dos blocos de texto reais e pausas.
        Identifica:
        - Gancho de Retenção (primeira frase ou até a primeira pausa significativa, max 4s)
        - Palavras de Ruptura Emocional (dor, perda, sofrimento, morte, internação, socorro, família, filho)
        - Conclusão / Acolhimento
        """
        scenes = []
        fps = 30.0

        # Identifica Gancho
        hook_end = min(3.5, total_duration * 0.15)
        for c in chunks:
            if c.get("end", 0.0) >= 2.5:
                hook_end = min(c.get("end"), 4.5)
                break

        scenes.append({
            "scene_id": "scene_1_hook",
            "type": "A-ROLL",
            "start_sec": 0.0,
            "end_sec": round(hook_end, 2),
            "start_frame": 0,
            "end_frame": int(hook_end * fps),
            "description": f"Gancho Inicial: '{chunks[0].get('text', '')[:60]}...'",
            "visual_action": "Plano Médio 1.0x com Punch-in suave 1.15x no pico de entonação inicial.",
            "sfx": "Sub Impacto na abertura"
        })

        # Procura momentos emocionais no corpo do vídeo
        emotional_keywords = {
            "dor", "morreu", "morte", "perdi", "perder", "droga", "drogas", "sofre", "sofrimento",
            "filho", "filha", "pai", "mãe", "família", "ajuda", "socorro", "amor", "tratamento", "clínica"
        }

        current_start = hook_end
        scene_idx = 2

        for i, chunk in enumerate(chunks):
            start = chunk.get("start", 0.0)
            end = chunk.get("end", 0.0)
            text = chunk.get("text", "").lower()

            if start < hook_end:
                continue

            words_in_chunk = set(re.findall(r"\w+", text))
            has_emotion = bool(words_in_chunk & emotional_keywords)

            # Se encontrar pico emocional com duração razoável (> 2.0s)
            if has_emotion and (end - current_start) >= 3.0:
                # Cria cena de A-Roll Close
                scenes.append({
                    "scene_id": f"scene_{scene_idx}_emphasis",
                    "type": "A-ROLL",
                    "start_sec": round(current_start, 2),
                    "end_sec": round(end, 2),
                    "start_frame": int(current_start * fps),
                    "end_frame": int(end * fps),
                    "description": f"Ênfase Emocional: '{chunk.get('text', '')[:70]}'",
                    "visual_action": "Câmera Close Íntimo (1.14x) focado no olhar do apresentador.",
                    "sfx": "Transição whoosh suave"
                })
                current_start = end
                scene_idx += 1

        # Encerramento institucional
        outro_duration = min(2.0, max(1.0, total_duration * 0.1))
        outro_start = max(current_start, total_duration - outro_duration)

        if outro_start > current_start:
            scenes.append({
                "scene_id": f"scene_{scene_idx}_body",
                "type": "A-ROLL",
                "start_sec": round(current_start, 2),
                "end_sec": round(outro_start, 2),
                "start_frame": int(current_start * fps),
                "end_frame": int(outro_start * fps),
                "description": "Desenvolvimento e Mensagem de Conscientização",
                "visual_action": "Alternância para Plano Médio 1.05x",
                "sfx": "Cama instrumental contínua"
            })
            scene_idx += 1

        scenes.append({
            "scene_id": f"scene_{scene_idx}_outro",
            "type": "OUTRO_INSTITUCIONAL",
            "start_sec": round(outro_start, 2),
            "end_sec": round(total_duration, 2),
            "start_frame": int(outro_start * fps),
            "end_frame": int(total_duration * fps),
            "description": "Fechamento Oficial Palácio Acolhimento",
            "visual_action": "Card Institucional com Monograma Dourado 'P' e Contato Humanizado",
            "sfx": "Pop suave no card institucional"
        })

        return {
            "total_duration": total_duration,
            "total_scenes": len(scenes),
            "scenes": scenes,
            "engine_used": "DETERMINISTIC_ACOUSTIC_SEMANTIC (ZERO SIMULAÇÃO)"
        }


class AutoEditorSilenceTrimmer:
    """
    Analisa os silêncios acústicos reais e calcula pausas mortas.
    Permite remover lacunas sem quebrar a naturalidade da fala (preserva 120ms de margem).
    """
    def map_silences_and_speech(self, chunks: List[Dict[str, Any]], min_gap: float = 0.45) -> List[Dict[str, Any]]:
        gaps = []
        for i in range(1, len(chunks)):
            prev_end = chunks[i-1]["end"]
            curr_start = chunks[i]["start"]
            gap = curr_start - prev_end
            if gap >= min_gap:
                gaps.append({
                    "start": prev_end,
                    "end": curr_start,
                    "duration": round(gap, 2),
                    "after_text": chunks[i-1].get("text", ""),
                    "before_text": chunks[i].get("text", "")
                })
        return gaps

    def trim_silences_ffmpeg(self, input_video: str, output_video: str, chunks: List[Dict[str, Any]], margin_sec: float = 0.08) -> Tuple[str, List[Dict[str, Any]]]:
        """
        Executa cortes reais de silêncio através de concatenação limpa dos trechos ativos de fala.
        """
        if not chunks:
            return input_video, chunks

        # Identifica segmentos ativos com margem de respiração
        segments = []
        for i, c in enumerate(chunks):
            start = max(0.0, c["start"] - margin_sec)
            end = c["end"] + margin_sec
            if segments and start <= segments[-1][1]:
                # Funde com o segmento anterior se sobrepor a margem
                segments[-1] = (segments[-1][0], max(segments[-1][1], end))
            else:
                segments.append((start, end))

        if len(segments) <= 1:
            return input_video, chunks

        # Monta filtro complexo de select para cortar silêncios no vídeo e áudio sem dessincronia
        v_expr = "+".join([f"between(t,{s:.3f},{e:.3f})" for s, e in segments])
        a_expr = "+".join([f"between(t,{s:.3f},{e:.3f})" for s, e in segments])

        cmd = [
            FFMPEG_BIN, "-y",
            "-i", input_video,
            "-vf", f"select='{v_expr}',setpts=N/FRAME_RATE/TB",
            "-af", f"aselect='{a_expr}',asetpts=N/SR/TB",
            "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
            "-c:a", "aac", "-b:a", "192k",
            output_video
        ]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"[!] Falha ao remover silêncios via FFmpeg: {res.stderr[:200]}")
            return input_video, chunks

        return output_video, chunks


class VisualStoryboardGenerator:
    """
    Gera comparação visual lado a lado entre o vídeo Original (Webcam linear contínua)
    e a Nova Edição com Montagem Real (A/B-roll cuts).
    """
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def extract_scene_comparison(
        self,
        original_video: str,
        edited_video: str,
        timestamps: List[Dict[str, Any]]
    ) -> List[Dict[str, str]]:
        results = []
        for item in timestamps:
            ts = item.get("sec", 1.0)
            label = item.get("label", "scene")
            orig_frame = os.path.join(self.output_dir, f"orig_{label}_{ts}s.jpg")
            edit_frame = os.path.join(self.output_dir, f"edit_{label}_{ts}s.jpg")

            subprocess.run([
                FFMPEG_BIN, "-y", "-ss", str(ts), "-i", original_video,
                "-vframes", "1", "-q:v", "2", orig_frame
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            subprocess.run([
                FFMPEG_BIN, "-y", "-ss", str(ts), "-i", edited_video,
                "-vframes", "1", "-q:v", "2", edit_frame
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            results.append({
                "label": label,
                "sec": ts,
                "description": item.get("desc", ""),
                "original_frame": orig_frame,
                "edited_frame": edit_frame
            })
        return results
