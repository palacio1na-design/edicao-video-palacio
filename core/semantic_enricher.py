#!/usr/bin/env python3
"""
PALÁCIO VÍDEOS 3.0 — SEMANTIC ENRICHER & SCENE PLANNER
Módulos: Fases 2, 3, 4 e 5 da Arquitetura Intelligent Motion Editor.

1. Transcrição com alinhamento temporal de palavras (Whisper).
2. Enriquecimento semântico e interpretação narrativa (Gemini 2.5 / Heurística Profunda).
3. Análise multimodal de frames (Detecção de face, olhar e espaços livres na tela).
4. Planejador de Cenas (Scene Planner): Mapeamento milimétrico de animações com justificativa.
"""

import os
import sys
import json
import subprocess
import shutil
from typing import Dict, Any, List, Optional, Tuple

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


class SemanticSpeechEnricher:
    """
    Motor inteligente de transcrição, enriquecimento semântico e planejamento de cenas.
    """

    def __init__(self, work_dir: str = "/Users/palacio.pro/.gemini/antigravity/scratch/motion_editor"):
        self.work_dir = work_dir
        self.frames_dir = os.path.join(work_dir, "extracted_frames")
        os.makedirs(self.work_dir, exist_ok=True)
        os.makedirs(self.frames_dir, exist_ok=True)

    # =========================================================================
    # FASE 2: TRANSCRIÇÃO INTELIGENTE & ALINHAMENTO TEMPORAL
    # =========================================================================

    def transcribe_video_with_words(self, video_path: str, model_name: str = "base") -> Dict[str, Any]:
        """
        Extrai áudio e executa Whisper para obter transcrição completa com timestamps de cada palavra.
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Vídeo não encontrado: {video_path}")

        audio_wav = os.path.join(self.work_dir, "extracted_audio.wav")
        print(f"[Fase 2] Extraindo áudio 16kHz mono de {os.path.basename(video_path)}...")
        cmd_audio = [
            FFMPEG_BIN, "-y", "-i", video_path,
            "-vn", "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1",
            audio_wav
        ]
        subprocess.run(cmd_audio, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)

        print(f"[Fase 2] Executando Whisper ({model_name}) com word_timestamps=True...")
        import whisper
        model = whisper.load_model(model_name, device="cpu")
        result = model.transcribe(audio_wav, language="pt", word_timestamps=True)

        segments = result.get("segments", [])
        all_words = []
        for seg in segments:
            for w in seg.get("words", []):
                all_words.append({
                    "word": w["word"].strip(),
                    "start": round(float(w["start"]), 3),
                    "end": round(float(w["end"]), 3),
                    "confidence": round(float(w.get("probability", 1.0)), 2)
                })

        transcript_data = {
            "video_path": video_path,
            "full_text": result.get("text", "").strip(),
            "segments": segments,
            "words": all_words
        }

        output_json = os.path.join(self.work_dir, "transcript_aligned.json")
        with open(output_json, "w", encoding="utf-8") as f:
            json.dump(transcript_data, f, ensure_ascii=False, indent=2)

        print(f"[Fase 2] Transcrição concluída: {len(all_words)} palavras sincronizadas.")
        return transcript_data

    # =========================================================================
    # FASE 4: ANÁLISE MULTIMODAL DOS FRAMES (ROSTO, OLHAR E ESPAÇO LIVRE)
    # =========================================================================

    def analyze_visual_frames(self, video_path: str, timestamps: List[float]) -> List[Dict[str, Any]]:
        """
        Extrai frames nos timestamps indicados e analisa enquadramento, presença de face e espaço livre.
        """
        import cv2

        results = []
        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        for sec in timestamps:
            frame_filename = f"frame_{sec:.2f}s.jpg"
            frame_path = os.path.join(self.frames_dir, frame_filename)

            # Extrair frame via FFmpeg
            cmd = [
                FFMPEG_BIN, "-y", "-ss", str(sec), "-i", video_path,
                "-vframes", "1", "-q:v", "2",
                frame_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

            if not os.path.exists(frame_path):
                continue

            img = cv2.imread(frame_path)
            if img is None:
                continue

            height, width, _ = img.shape
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(60, 60))

            face_detected = len(faces) > 0
            face_box = None
            free_zone = "center_right"  # Padrão
            is_close_up = False

            if face_detected:
                # Pegar a maior face detectada
                largest_face = max(faces, key=lambda b: b[2] * b[3])
                fx, fy, fw, fh = largest_face
                face_box = {
                    "x": int(fx), "y": int(fy),
                    "width": int(fw), "height": int(fh),
                    "relative_area": round((fw * fh) / (width * height), 3)
                }

                # Close-up se a face ocupar mais de 10% da área total vertical
                is_close_up = face_box["relative_area"] > 0.09

                # Calcular onde está o espaço livre na tela (negativo)
                face_center_x = fx + fw / 2.0
                if face_center_x < width * 0.45:
                    free_zone = "right_half"  # Rosto à esquerda, espaço livre à direita
                elif face_center_x > width * 0.55:
                    free_zone = "left_half"   # Rosto à direita, espaço livre à esquerda
                else:
                    free_zone = "upper_lower" # Rosto centralizado, espaço acima ou abaixo

            results.append({
                "timestamp_sec": sec,
                "frame_path": frame_path,
                "face_detected": face_detected,
                "face_box": face_box,
                "is_close_up": is_close_up,
                "free_zone": free_zone,
                "recommendation": "preserve_face" if is_close_up else "allow_motion_overlay"
            })

        return results

    # =========================================================================
    # FASE 3 & 5: ENRIQUECIMENTO SEMÂNTICO E PLANEJAMENTO DE CENAS
    # =========================================================================

    def generate_semantic_scene_plan(
        self,
        transcript_data: Dict[str, Any],
        video_path: str,
        fps: int = 30
    ) -> Dict[str, Any]:
        """
        Executa a interpretação semântica narrativa e planeja as cenas com motion graphics sincronizados.
        """
        segments = transcript_data.get("segments", [])
        words = transcript_data.get("words", [])

        # Extrair timestamps médios para análise visual de frames
        sample_times = [round(seg["start"] + (seg["end"] - seg["start"]) / 2.0, 2) for seg in segments[:8]]
        if not sample_times and words:
            sample_times = [2.0, 8.0, 15.0, 22.0]

        print("[Fase 4] Analisando multimodalmente os frames do vídeo original...")
        frame_analyses = self.analyze_visual_frames(video_path, sample_times)
        frame_map = {round(fa["timestamp_sec"], 1): fa for fa in frame_analyses}

        scenes = []
        scene_idx = 1

        for seg in segments:
            text = seg["text"].strip()
            start_sec = round(float(seg["start"]), 2)
            end_sec = round(float(seg["end"]), 2)
            duration_sec = round(end_sec - start_sec, 2)

            if duration_sec < 1.2:
                continue

            # Buscar palavras dentro desse segmento
            seg_words = [
                w for w in words
                if w["start"] >= start_sec - 0.2 and w["end"] <= end_sec + 0.2
            ]

            # Encontrar análise visual mais próxima
            matching_fa = None
            for ts, fa in frame_map.items():
                if abs(ts - (start_sec + duration_sec / 2.0)) < 4.0:
                    matching_fa = fa
                    break

            is_close_up = matching_fa.get("is_close_up", False) if matching_fa else False
            free_zone = matching_fa.get("free_zone", "center_right") if matching_fa else "center_right"

            # Interpretação Semântica e Decisão de Motion Graphics
            semantic_info = self._interpret_semantics(text, duration_sec, is_close_up, free_zone)

            start_frame = int(round(start_sec * fps))
            end_frame = int(round(end_sec * fps))

            scene = {
                "scene_id": f"cena_{scene_idx:02d}",
                "start_sec": start_sec,
                "end_sec": end_sec,
                "start_frame": start_frame,
                "end_frame": end_frame,
                "duration_frames": end_frame - start_frame,
                "speech_text": text,
                "words": seg_words,
                "meaning": semantic_info["meaning"],
                "emotion": semantic_info["emotion"],
                "visual_objective": semantic_info["visual_objective"],
                "motion_type": semantic_info["motion_type"],
                "motion_params": semantic_info["motion_params"],
                "layout_position": semantic_info["layout_position"],
                "keep_face_visible": semantic_info["keep_face_visible"],
                "transition": semantic_info["transition"],
                "priority": semantic_info["priority"],
                "justification": semantic_info["justification"],
                "approval_status": "pending"  # PENDENTE DE APROVAÇÃO HUMANA (Fase 6)
            }
            scenes.append(scene)
            scene_idx += 1

        scene_plan = {
            "version": "3.0.0",
            "video_path": video_path,
            "total_scenes": len(scenes),
            "fps": fps,
            "scenes": scenes,
            "brand": "palacio-acolhimento",
            "metadata": {
                "format": "9:16",
                "resolution": "1080x1920",
                "human_gate_required": True,
                "is_approved": False
            }
        }

        plan_file = os.path.join(self.work_dir, "storyboard_plan.json")
        with open(plan_file, "w", encoding="utf-8") as f:
            json.dump(scene_plan, f, ensure_ascii=False, indent=2)

        print(f"[Fase 5] Plano de cenas gerado com {len(scenes)} cenas estruturadas.")
        print(f"[Fase 5] Salvo em: {plan_file}")
        return scene_plan

    def _interpret_semantics(self, text: str, duration: float, is_close_up: bool, free_zone: str) -> Dict[str, Any]:
        """
        Mapeia a fala para conceitos semânticos, determinando o motion graphics correspondente.
        """
        lower = text.lower()

        # 1. Caso de Clímax Emocional / Foco nos Olhos (Preservar a Face!)
        if any(w in lower for w in ["não quero que seja você", "não quero perder você", "esperando você", "morreu"]):
            return {
                "meaning": "Momento de choque e gravidade máxima. Alerta urgente à vida.",
                "emotion": "dor e apelo íntimo",
                "visual_objective": "Preservar a expressão facial e o olhar de Marcelo Palácio sem distrações visuais.",
                "motion_type": "close_up_face",
                "motion_params": {
                    "zoom": 1.16,
                    "focus": "eyes",
                    "sub_impact": True
                },
                "layout_position": {"anchor": "full_screen", "y_offset": 0},
                "keep_face_visible": True,
                "transition": "punch_in_spring",
                "priority": 5,
                "justification": "A dor e o olho no olho conectam mais do que qualquer gráfico. O rosto de Marcelo é o elemento principal."
            }

        # 2. Conceito de Linha do Tempo / Passagem dos Anos
        if any(w in lower for w in ["ano", "anos", "tempo", "passou", "antigamente", "hoje", "ontem"]):
            return {
                "meaning": "Passagem de tempo e perdas acumuladas ao longo da trajetória da dependência.",
                "emotion": "nostalgia e reflexão sóbria",
                "visual_objective": "Ilustrar a passagem dos anos com uma linha do tempo vetorial suave.",
                "motion_type": "animated_timeline",
                "motion_params": {
                    "points": ["Passado", "Alerta", "Presente"],
                    "highlightIndex": 1,
                    "accentColor": "#E5A93C"
                },
                "layout_position": {"anchor": free_zone, "top": 280, "width": 800},
                "keep_face_visible": True,
                "transition": "fade_in_spring",
                "priority": 4,
                "justification": "Linha temporal minimalista reforça o conceito de que o tempo não para, sem cobrir o locutor."
            }

        # 3. Conceito de Etapas / Processo / Degraus
        if any(w in lower for w in ["etapa", "etapas", "passo", "primeiro", "segundo", "três", "processo", "regra"]):
            return {
                "meaning": "Estruturação metódica de raciocínio clínico para a família.",
                "emotion": "clareza e autoridade",
                "visual_objective": "Exibir os passos numerados sincronizados com a pronúncia dos numerais.",
                "motion_type": "animated_process",
                "motion_params": {
                    "steps": ["Reconhecer", "Estabelecer Limites", "Buscar Ajuda"],
                    "activeStep": 1,
                    "accentColor": "#074B32"
                },
                "layout_position": {"anchor": free_zone, "top": 320, "width": 780},
                "keep_face_visible": True,
                "transition": "slide_up_spring",
                "priority": 4,
                "justification": "Ajuda a mente da família a memorizar a ordem das ações essenciais."
            }

        # 4. Conceito de Vínculos / Afastamento / Rompimento
        if any(w in lower for w in ["amigo", "amigos", "família", "mãe", "pai", "afastando", "perdi", "sozinho"]):
            return {
                "meaning": "A dor do isolamento e o enfraquecimento dos laços afetivos.",
                "emotion": "solidão e quebra de vínculos",
                "visual_objective": "Diagrama de conexões que se afastam sutilmente, ilustrando o isolamento social.",
                "motion_type": "animated_connection",
                "motion_params": {
                    "nodes": ["Você", "Família", "Amigos"],
                    "mode": "separate",
                    "accentColor": "#E5A93C"
                },
                "layout_position": {"anchor": free_zone, "top": 300, "width": 750},
                "keep_face_visible": True,
                "transition": "fade_in_smooth",
                "priority": 3,
                "justification": "Ilustra o afastamento progressivo provocado pela droga sem cair em caricatura."
            }

        # 5. Padrão: Palavras-Chave de Destaque Sóbrias
        words_in_text = [w for w in text.split() if len(w) > 4]
        key_word = words_in_text[0].upper() if words_in_text else "ACOLHIMENTO"
        return {
            "meaning": "Reforço conceitual da mensagem falada.",
            "emotion": "sobriedade",
            "visual_objective": "Destaque cinético elegante da palavra-chave na área livre.",
            "motion_type": "animated_keywords",
            "motion_params": {
                "keyword": key_word,
                "subtitle": "PALÁCIO ACOLHIMENTO",
                "accentColor": "#E5A93C"
            },
            "layout_position": {"anchor": "top_center", "top": 260, "width": 840},
            "keep_face_visible": True,
            "transition": "fade_in_spring",
            "priority": 2,
            "justification": "Garante retenção visual sem sobrecarregar a mensagem falada."
        }
