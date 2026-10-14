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
from core.video_processor import cut_and_render_reel, generate_srt
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

    for idx, c in enumerate(cuts, 1):
        cid = c.get("id", f"corte_{idx:02d}")
        start = c["start"]
        dur = c["duration"]
        title = c.get("title", cid)

        print(f"\n✂️ [{idx}/{len(cuts)}] Renderizando {cid}: '{title}' ({dur:.1f}s)")
        print(f"   Início: {start:.2f}s | Fim: {c['end']:.2f}s | Primeira palavra: '{c.get('first_word')}'")

        out_name = f"{cid}_{title.replace(' ', '_').replace('/', '_')}.mp4"
        out_path = os.path.join(output_dir, out_name)

        # Gera SRT específico do trecho
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

        cut_and_render_reel(
            input_video=video_path,
            output_video=out_path,
            start_sec=start,
            duration_sec=dur,
            crop_916=True,
            normalize_audio=True,
            burn_subtitles=burn_sub,
            srt_path=srt_path
        )
        c["output_video"] = out_path
        c["output_srt"] = srt_path
        print(f"   ➔ Vídeo gerado: {out_path}")
        if srt_path and os.path.exists(srt_path):
            print(f"   ➔ Legenda SRT gerada: {srt_path}")

        if args.capcut:
            draft_dir, err = create_safe_capcut_project(f"Palacio_{cid}", out_path, srt_path)
            if draft_dir:
                print(f"   ➔ Projeto CapCut criado: {draft_dir}")

    # Atualiza página de revisão com os vídeos renderizados
    review_path = os.path.join(output_dir, "review.html")
    generate_review_page(cuts, review_path, original_video_name=os.path.basename(video_path))
    print(f"\n✨ Central de Revisão atualizada com players interativos: {review_path}")

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
    p_rn.add_argument("--subtitles", action="store_true", help="Queimar legendas no vídeo (padrão: clipe limpo sem legenda)")
    p_rn.add_argument("--capcut", action="store_true", help="Injetar projeto automaticamente no CapCut Desktop")

    args = parser.parse_args()
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "render":
        cmd_render(args)

if __name__ == "__main__":
    main()
