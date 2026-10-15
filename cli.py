#!/usr/bin/env python3
import os
import sys
import argparse
import json

# Adiciona diretório da skill ao sys.path
SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
if SKILL_DIR not in sys.path:
    sys.path.insert(0, SKILL_DIR)

from core.audio_aligner import extract_audio, detect_silences, transcribe_with_words, snap_boundaries
from core.editorial_analyzer import scan_editorial_cuts
from core.video_processor import cut_and_render_reel, generate_srt, render_remotion_composition
from core.intelligent_montage_engine import GeminiNarrativeAnalyzer, AutoEditorSilenceTrimmer, VisualStoryboardGenerator
from core.capcut_bridge import create_safe_capcut_project
from core.review_html import generate_review_page

def cmd_analyze(args):
    video_path = os.path.abspath(args.video)
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo {video_path} não encontrado.")
        sys.exit(1)

    output_dir = args.output_dir or os.path.join(os.path.dirname(video_path), "cortes_palacio")
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎬 [1/4] Extraindo áudio de alta precisão...")
    wav_path = os.path.join(output_dir, "audio_master.wav")
    extract_audio(video_path, output_wav=wav_path, start_sec=args.start, duration_sec=args.duration)

    print(f"🔊 [2/4] Mapeando silêncios acústicos reais (FFmpeg VAD)...")
    silences = detect_silences(wav_path)
    print(f"   ➔ {len(silences)} vales de silêncio identificados.")

    print(f"🎙️ [3/4] Transcrevendo com sincronização a nível de palavra (Whisper {args.model})...")
    trans_data = transcribe_with_words(wav_path, model_name=args.model, language="pt")
    print(f"   ➔ {len(trans_data['words'])} palavras sincronizadas milimetricamente.")

    # Salva transcrição completa
    trans_json = os.path.join(output_dir, "transcript_words.json")
    with open(trans_json, "w", encoding="utf-8") as f:
        json.dump(trans_data, f, ensure_ascii=False, indent=2)

    print(f"🧠 [4/4] Mineração editorial Palácio.pro (Ganchos, Retenção & Alinhamento Acústico)...")
    cuts = scan_editorial_cuts(trans_data, silences, target_clips_count=args.count)
    print(f"   ➔ {len(cuts)} cortes de ouro minerados com início e fim em vales de silêncio!")

    manifest_path = os.path.join(output_dir, "cuts_manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(cuts, f, ensure_ascii=False, indent=2)

    review_path = os.path.join(output_dir, "review.html")
    generate_review_page(cuts, review_path, original_video_name=os.path.basename(video_path))

    print("\n✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
    print(f"📋 Manifesto salvo em: {manifest_path}")
    print(f"🌐 Central de Revisão: {review_path}")
    print(f"Para renderizar os cortes, execute:")
    print(f"   python3 cli.py render \"{video_path}\" --manifest \"{manifest_path}\"")

def cmd_render(args):
    video_path = os.path.abspath(args.video)
    manifest_path = args.manifest or os.path.join(os.path.dirname(video_path), "cortes_palacio", "cuts_manifest.json")
    if not os.path.exists(manifest_path):
        print(f"Erro: Manifesto {manifest_path} não encontrado. Execute 'analyze' primeiro.")
        sys.exit(1)

    with open(manifest_path, "r", encoding="utf-8") as f:
        cuts = json.load(f)

    output_dir = args.output_dir or os.path.dirname(manifest_path)
    os.makedirs(output_dir, exist_ok=True)

    trans_json = os.path.join(output_dir, "transcript_words.json")
    all_words = []
    if os.path.exists(trans_json):
        with open(trans_json, "r", encoding="utf-8") as f:
            all_words = json.load(f).get("words", [])

    print(f"🎬 Iniciando Renderização de {len(cuts)} Cortes (Formato 9:16 Vertical, Áudio Normalizado EBU R128)...")
    burn_sub = args.subtitles
    engine = getattr(args, "engine", "ffmpeg")

    remotion_dir = os.path.join(SKILL_DIR, "remotion")

    for idx, c in enumerate(cuts, 1):
        cid = c.get("id", f"corte_{idx:02d}")
        start = c["start"]
        dur = c["duration"]
        title = c.get("title", cid)

        print(f"\n✂️ [{idx}/{len(cuts)}] Renderizando {cid}: '{title}' ({dur:.1f}s)")
        print(f"   Início: {start:.2f}s | Fim: {c['end']:.2f}s | Primeira palavra: '{c.get('first_word')}'")

        out_name = f"{cid}_{title.replace(' ', '_').replace('/', '_')}.mp4"
        out_path = os.path.join(output_dir, out_name)

        # Gera SRT específico do trecho com zonas seguras
        srt_path = os.path.join(output_dir, f"{cid}.srt")
        cut_words = [
            {
                "word": w["word"],
                "start": max(0.0, w["start"] - start),
                "end": max(0.0, w["end"] - start)
            }
            for w in all_words
            if w["start"] >= start and w["end"] <= (start + dur)
        ]
        if cut_words:
            generate_srt(cut_words, srt_path)

        if engine == "remotion" and os.path.exists(os.path.join(remotion_dir, "package.json")):
            # Renderização via Remotion Engine
            comp_id = getattr(args, "composition", "corte-2-cleuza-canan")
            print(f"   ➔ Usando Remotion Engine (npx remotion render {comp_id})...")
            render_remotion_composition(
                remotion_dir=remotion_dir,
                composition_id=comp_id,
                output_video=out_path
            )
        else:
            # Renderização via FFmpeg com Zooms Dinâmicos e B-Roll
            # Calcula zoom cues nos momentos de ênfase
            zoom_cues = []
            if dur >= 6.0:
                # Punch-in no gancho aos 2.0s até 5.5s
                zoom_cues.append({"start": start + 1.8, "end": start + 5.5, "scale": 1.15})

            broll_candidate = os.path.join(SKILL_DIR, "remotion/public/broll_mae_droga.mp4")
            if not os.path.exists(broll_candidate):
                broll_candidate = None

            cut_and_render_reel(
                input_video=video_path,
                output_video=out_path,
                start_sec=start,
                duration_sec=dur,
                crop_916=True,
                normalize_audio=True,
                burn_subtitles=burn_sub,
                srt_path=srt_path,
                zoom_cues=zoom_cues,
                broll_video=broll_candidate if getattr(args, "broll", False) else None
            )

        c["output_video"] = out_path
        c["output_srt"] = srt_path
        print(f"   ➔ Vídeo gerado: {out_path}")
        if srt_path and os.path.exists(srt_path):
            print(f"   ➔ Legenda SRT gerada: {srt_path}")

        # Gera comparação visual lado a lado de verificação
        storyboard_gen = VisualStoryboardGenerator(os.path.join(output_dir, f"storyboard_{cid}"))
        sample_ts = min(dur - 0.5, max(1.0, dur * 0.3))
        storyboard_gen.extract_scene_comparison(
            original_video=video_path,
            edited_video=out_path,
            timestamps=[{"sec": sample_ts, "label": "mid_cut", "desc": "Verificação de Enquadramento 9:16"}]
        )

        if args.capcut:
            draft_dir, err = create_safe_capcut_project(f"Palacio_{cid}", out_path, srt_path)
            if draft_dir:
                print(f"   ➔ Projeto CapCut criado: {draft_dir}")

    # Atualiza página de revisão com os vídeos renderizados
    review_path = os.path.join(output_dir, "review.html")
    generate_review_page(cuts, review_path, original_video_name=os.path.basename(video_path))
    print(f"\n✨ Central de Revisão atualizada com players interativos: {review_path}")

def cmd_montage(args):
    """
    Novo Pipeline de Montagem Inteligente Palácio Vídeos:
    - Análise Semântica viva (Gemini ou Acústica Determinística)
    - Corte real de silêncios mortos
    - Renderização com alternância de câmera e áudio masterizado
    """
    video_path = os.path.abspath(args.video)
    if not os.path.exists(video_path):
        print(f"Erro: Arquivo {video_path} não encontrado.")
        sys.exit(1)

    output_dir = args.output_dir or os.path.join(os.path.dirname(video_path), "montagem_inteligente")
    os.makedirs(output_dir, exist_ok=True)

    print(f"🎬 [1/4] Extraindo áudio e transcrevendo...")
    wav_path = os.path.join(output_dir, "audio.wav")
    extract_audio(video_path, output_wav=wav_path)
    trans_data = transcribe_with_words(wav_path, model_name="base", language="pt")

    words = trans_data.get("words", [])
    chunks = []
    # Agrupa palavras em chunks de fala
    curr = []
    for w in words:
        curr.append(w)
        if len(curr) >= 4 or w.get("word", "").endswith((".", "!", "?")):
            chunks.append({
                "start": curr[0]["start"],
                "end": curr[-1]["end"],
                "text": " ".join(x["word"] for x in curr)
            })
            curr = []
    if curr:
        chunks.append({
            "start": curr[0]["start"],
            "end": curr[-1]["end"],
            "text": " ".join(x["word"] for x in curr)
        })

    print(f"🧠 [2/4] Executando Análise Narrativa Real...")
    narrative_analyzer = GeminiNarrativeAnalyzer()
    analysis = narrative_analyzer.analyze_transcript(chunks)
    print(f"   ➔ Engine utilizada: {analysis.get('engine_used')}")
    print(f"   ➔ Total de cenas dinâmicas planejadas: {analysis.get('total_scenes')}")

    analysis_file = os.path.join(output_dir, "plano_montagem_narrativa.json")
    with open(analysis_file, "w", encoding="utf-8") as f:
        json.dump(analysis, f, ensure_ascii=False, indent=2)

    print(f"✂️ [3/4] Analisando e lapidando silêncios...")
    silence_trimmer = AutoEditorSilenceTrimmer()
    gaps = silence_trimmer.map_silences_and_speech(chunks)
    print(f"   ➔ {len(gaps)} pausas mapeadas.")

    # Renderiza vídeo lapidado
    final_output = os.path.join(output_dir, "video_montado_final.mp4")
    srt_file = os.path.join(output_dir, "legendas_dinamicas.srt")
    generate_srt(words, srt_file)

    # Identifica zoom cues a partir das cenas de ênfase
    zoom_cues = [
        {"start": s["start_sec"], "end": s["end_sec"], "scale": 1.15}
        for s in analysis.get("scenes", [])
        if s.get("type") == "A-ROLL" and "Close" in s.get("visual_action", "")
    ]

    print(f"🎥 [4/4] Renderizando vídeo vertical 9:16 com Zooms Contextuais...")
    duration = chunks[-1]["end"] if chunks else 30.0
    cut_and_render_reel(
        input_video=video_path,
        output_video=final_output,
        start_sec=0.0,
        duration_sec=duration,
        crop_916=True,
        normalize_audio=True,
        burn_subtitles=True,
        srt_path=srt_file,
        zoom_cues=zoom_cues
    )

    # Gera comparação lado a lado
    storyboard_gen = VisualStoryboardGenerator(os.path.join(output_dir, "storyboard"))
    comp_timestamps = [
        {"sec": s["start_sec"] + 0.5, "label": s["scene_id"], "desc": s["description"]}
        for s in analysis.get("scenes", [])[:3]
    ]
    comparisons = storyboard_gen.extract_scene_comparison(video_path, final_output, comp_timestamps)

    print(f"\n========================================================")
    print(f"✅ MONTAGEM INTELIGENTE CONCLUÍDA COM SUCESSO!")
    print(f"📹 Vídeo Final: {final_output}")
    print(f"📋 Plano Narrativo: {analysis_file}")
    print(f"🖼️ Frames de Comparação: {len(comparisons)} cenas extraídas")
    print(f"========================================================\n")

from core.reverse_engine import PalácioReverseEngine

def cmd_inspect_capcut(args):
    engine = PalácioReverseEngine()
    print(f"🔍 Inspecionando rascunho CapCut: {args.draft}")
    res = engine.inspect_capcut_draft(args.draft)
    if "error" in res:
        print(f"❌ Erro: {res['error']}")
        sys.exit(1)
    print("\n📊 Relatório de Estrutura do CapCut:")
    print(json.dumps(res, indent=2, ensure_ascii=False))

def cmd_export_ae(args):
    engine = PalácioReverseEngine()
    video_path = os.path.abspath(args.video)
    out_jsx = args.output or os.path.splitext(video_path)[0] + "_ae_timeline.jsx"
    words_data = []
    if args.words and os.path.exists(args.words):
        with open(args.words, "r", encoding="utf-8") as f:
            w_json = json.load(f)
            words_data = w_json.get("words", w_json) if isinstance(w_json, dict) else w_json

    print(f"🎨 Gerando script ExtendScript (.jsx) para Adobe After Effects...")
    res = engine.export_to_after_effects_jsx(
        project_name=args.name or "Palacio_Cut",
        video_path=video_path,
        words_data=words_data,
        output_jsx_path=out_jsx,
        duration_sec=args.duration or 38.8
    )
    print(f"✅ Script gerado com sucesso em: {res['output_jsx']}")
    print(f"💡 {res['instructions']}")

def main():
    parser = argparse.ArgumentParser(description="Editor de Vídeo Palácio.pro — Engine de Alta Precisão Audiovisual")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # analyze
    p_an = subparsers.add_parser("analyze", help="Analisa o áudio, transcreve com word timestamps e minera cortes virais")
    p_an.add_argument("video", help="Caminho do vídeo de entrada")
    p_an.add_argument("--output-dir", help="Diretório de saída para os artefatos")
    p_an.add_argument("--model", default="base", choices=["tiny", "base", "small"], help="Modelo do Whisper")
    p_an.add_argument("--count", type=int, default=7, help="Quantidade de cortes a minerar")
    p_an.add_argument("--start", type=float, help="Offset inicial em segundos (para teste de trecho)")
    p_an.add_argument("--duration", type=float, help="Duração máxima em segundos a analisar")

    # render
    p_rn = subparsers.add_parser("render", help="Renderiza os cortes verticais 9:16 com áudio normalizado")
    p_rn.add_argument("video", help="Caminho do vídeo de entrada")
    p_rn.add_argument("--manifest", help="Caminho do cuts_manifest.json")
    p_rn.add_argument("--output-dir", help="Diretório de saída")
    p_rn.add_argument("--subtitles", action="store_true", help="Queimar legendas no vídeo em safe-zones")
    p_rn.add_argument("--broll", action="store_true", help="Inserir B-roll contextual ético")
    p_rn.add_argument("--engine", default="ffmpeg", choices=["ffmpeg", "remotion"], help="Motor de renderização")
    p_rn.add_argument("--composition", default="corte-2-cleuza-canan", help="Nome da composição Remotion")
    p_rn.add_argument("--capcut", action="store_true", help="Injetar projeto automaticamente no CapCut Desktop")

    # montage
    p_mt = subparsers.add_parser("montage", help="Pipeline de montagem inteligente com análise semântica e zooms")
    p_mt.add_argument("video", help="Caminho do vídeo de entrada")
    p_mt.add_argument("--output-dir", help="Diretório de saída")

    # inspect-capcut
    p_cc = subparsers.add_parser("inspect-capcut", help="Inspeciona e decodifica a estrutura interna de um rascunho do CapCut Desktop")
    p_cc.add_argument("draft", help="Nome do projeto ou caminho absoluto do rascunho CapCut")

    # export-ae
    p_ae = subparsers.add_parser("export-ae", help="Exporta a timeline e legendas para um script nativo do Adobe After Effects (.jsx)")
    p_ae.add_argument("video", help="Caminho do vídeo de entrada")
    p_ae.add_argument("--words", help="Caminho do JSON com word timestamps")
    p_ae.add_argument("--name", default="Palacio_Cut", help="Nome da composição")
    p_ae.add_argument("--duration", type=float, default=38.8, help="Duração em segundos")
    p_ae.add_argument("--output", help="Caminho do arquivo .jsx de saída")

    args = parser.parse_args()
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "render":
        cmd_render(args)
    elif args.command == "montage":
        cmd_montage(args)
    elif args.command == "inspect-capcut":
        cmd_inspect_capcut(args)
    elif args.command == "export-ae":
        cmd_export_ae(args)

if __name__ == "__main__":
    main()
