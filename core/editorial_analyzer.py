import os
import sys
import json
import re

THEMATIC_PATTERNS = [
    {
        "id": "fundo_de_poco",
        "category": "Depoimento / Fundo de Poço",
        "keywords": ["última vez", "55 kg", "cheguei na clínica", "não aguentava mais", "overdose", "perdi tudo", "hospital", "morrer", "fundo do poço", "droga", "álcool", "internação"],
        "min_dur": 30,
        "max_dur": 85
    },
    {
        "id": "acolhimento_familiar",
        "category": "Família & Codependência",
        "keywords": ["mãe", "pai", "família", "esposa", "filho", "codependência", "desespero", "adoece junto", "ajudar", "acolhimento", "noite em claro"],
        "min_dur": 30,
        "max_dur": 80
    },
    {
        "id": "quebra_de_tabu",
        "category": "Quebra de Tabu & Tratamento",
        "keywords": ["internar", "clínica", "manicômio", "castigo", "preconceito", "tratamento humanizado", "vida serena", "amor", "dignidade"],
        "min_dur": 30,
        "max_dur": 75
    },
    {
        "id": "superacao_recuperacao",
        "category": "Superação & Nova Vida",
        "keywords": ["recuperação", "viver limpo", "sobriedade", "esperança", "transformação", "vida serena", "propósito", "deus", "espiritualidade"],
        "min_dur": 30,
        "max_dur": 75
    }
]

def scan_editorial_cuts(transcription_data, silences, target_clips_count=7):
    """
    Minera os momentos de ouro da fala do Marcelo Palácio com base em picos temáticos,
    storytelling completo (gancho, dor, reflexão) e alinhamento acústico.
    """
    words = transcription_data.get("words", [])
    segments = transcription_data.get("segments", [])
    if not words:
        return []

    from core.audio_aligner import snap_boundaries

    found_cuts = []

    # Procurar passagens marcantes nos segmentos
    total_segments = len(segments)
    for i in range(total_segments):
        seg = segments[i]
        text_lower = seg["text"].lower()

        for pat in THEMATIC_PATTERNS:
            matched_kws = [k for k in pat["keywords"] if k in text_lower]
            if matched_kws:
                # Início potencial do corte
                start_seg_idx = i
                # Expandir até atingir uma duração coerente (30 a 75 segundos) com desfecho natural
                accumulated_text = []
                end_seg_idx = i
                current_duration = 0

                for j in range(i, min(i + 25, total_segments)):
                    s = segments[j]
                    accumulated_text.append(s["text"].strip())
                    current_duration = s["end"] - segments[start_seg_idx]["start"]
                    # Verifica se encerra em pontuação forte após atingir a duração mínima
                    if current_duration >= pat["min_dur"]:
                        if s["text"].strip().endswith((".", "!", "?")) or current_duration >= pat["max_dur"]:
                            end_seg_idx = j
                            break

                candidate_start = segments[start_seg_idx]["start"]
                candidate_end = segments[end_seg_idx]["end"]

                # Verificar se não sobrepõe excessivamente com cortes já encontrados
                overlap = False
                for existing in found_cuts:
                    if not (candidate_end < existing["raw_start"] or candidate_start > existing["raw_end"]):
                        overlap = True
                        break

                if not overlap and (candidate_end - candidate_start) >= 25:
                    # Ajuste acústico cirúrgico no silêncio
                    snapped = snap_boundaries(candidate_start, candidate_end, words, silences)
                    
                    full_text = " ".join(accumulated_text)
                    first_phrase = accumulated_text[0] if accumulated_text else ""
                    
                    # Título e gancho inspirados no estilo viral do Marcelo
                    hook = first_phrase.strip()
                    title = f"Corte Viral — {matched_kws[0].capitalize()}"
                    
                    found_cuts.append({
                        "id": f"corte_{len(found_cuts)+1:02d}",
                        "title": title,
                        "category": pat["category"],
                        "matched_keyword": matched_kws[0],
                        "hook": hook,
                        "raw_start": candidate_start,
                        "raw_end": candidate_end,
                        "start": snapped["start"],
                        "end": snapped["end"],
                        "duration": snapped["duration"],
                        "first_word": snapped["first_word"],
                        "last_word": snapped["last_word"],
                        "full_transcript": full_text,
                        "seo_caption": generate_seo_copy(title, hook, full_text)
                    })

                if len(found_cuts) >= target_clips_count:
                    break
        if len(found_cuts) >= target_clips_count:
            break

    return found_cuts

def generate_seo_copy(title, hook, text):
    """
    Gera legenda SEO pronta para postar no Instagram Reels, TikTok e Shorts.
    """
    lines = [
        f"🚨 {hook}",
        "",
        "Se essa mensagem faz sentido para você ou para a sua família, assista até o final.",
        "",
        "A dependência química adoece não apenas quem consome, mas toda a estrutura familiar. O acolhimento e o tratamento humanizado salvam vidas.",
        "",
        "💬 Deixe sua opinião nos comentários: você já passou por isso ou conhece alguém que precisa ouvir isso hoje?",
        "",
        "📲 Compartilhe com quem precisa desse acolhimento.",
        "",
        "#MarceloPalacio #PalacioAcolhimento #ClinicaVidaSerena #DependenciaQuimica #Codependencia #AcolhimentoFamiliar #Sobriedade #Recuperacao #TratamentoHumanizado"
    ]
    return "\n".join(lines)
