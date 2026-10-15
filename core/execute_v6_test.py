"""
SCRIPT DE EXECUÇÃO PALÁCIO VÍDEOS 6.0
Gera os planos edit-plan.json e sound-plan.json,
e renderiza a VERSÃO A (Cinematográfica Emocional) e VERSÃO B (Dinâmica Motion).
"""

import os
import sys
import json

sys.path.insert(0, "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio")

from core.smart_editor import PalácioSmartEditor

SOURCE_VIDEO = "/Users/palacio.pro/Downloads/Corte_04_Amor_Firme_Meu_Pai_Fechou_o_Apartamento_SEM_LEGENDA.mp4"
WORDS_FILE = "/Users/palacio.pro/.gemini/antigravity/scratch/corte05_words.json"
BASE_DIR = "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio"
DOWNLOADS_DIR = "/Users/palacio.pro/Downloads"

TARGET_DURATION = 38.80 # Exata conclusão narrativa: "É isso, não é meu irmão? É isso."

def main():
    print("=" * 60)
    print("INICIANDO PIPELINE PALÁCIO VÍDEOS 6.0")
    print("=" * 60)

    with open(WORDS_FILE, "r", encoding="utf-8") as f:
        transcript_data = json.load(f)

    smart_editor = PalácioSmartEditor()

    # 1. Planejamento Editorial e de Som
    print("\n[1/4] Gerando planos editoriais e de sound design...")
    edit_plan_a, sound_plan_a = smart_editor.create_plans(
        SOURCE_VIDEO, transcript_data, target_duration=TARGET_DURATION, style="cinematic"
    )
    edit_plan_b, sound_plan_b = smart_editor.create_plans(
        SOURCE_VIDEO, transcript_data, target_duration=TARGET_DURATION, style="motion"
    )

    edit_plan_path = os.path.join(BASE_DIR, "edit-plan.json")
    sound_plan_path = os.path.join(BASE_DIR, "sound-plan.json")

    with open(edit_plan_path, "w", encoding="utf-8") as f:
        json.dump({
            "versao_a_cinematica": edit_plan_a,
            "versao_b_dinamica": edit_plan_b
        }, f, ensure_ascii=False, indent=2)

    with open(sound_plan_path, "w", encoding="utf-8") as f:
        json.dump({
            "versao_a_soundtrack_and_sfx": sound_plan_a,
            "versao_b_soundtrack_and_sfx": sound_plan_b
        }, f, ensure_ascii=False, indent=2)

    print(f"Planos salvos em:\n - {edit_plan_path}\n - {sound_plan_path}")

    # 2. Renderização VERSÃO A: Cinematográfica Emocional
    print("\n[2/4] Renderizando VERSÃO A (Cinematográfica Emocional)...")
    out_a = os.path.join(DOWNLOADS_DIR, "Palacio_Videos_Versao_A_Cinematografica_39s.mp4")
    file_a, audit_a = smart_editor.render_version_a_cinematic(
        SOURCE_VIDEO, out_a, edit_plan_a, sound_plan_a, transcript_data
    )
    print(f"Versão A gerada: {file_a}")
    print("Auditoria Versão A:")
    print(json.dumps(audit_a, indent=2, ensure_ascii=False))

    # 3. Renderização VERSÃO B: Dinâmica com Motion Design
    print("\n[3/4] Renderizando VERSÃO B (Dinâmica com Motion Design)...")
    out_b = os.path.join(DOWNLOADS_DIR, "Palacio_Videos_Versao_B_Dinamica_Motion_39s.mp4")
    file_b, audit_b = smart_editor.render_version_b_dynamic(
        SOURCE_VIDEO, out_b, edit_plan_b, sound_plan_b, transcript_data
    )
    print(f"Versão B gerada: {file_b}")
    print("Auditoria Versão B:")
    print(json.dumps(audit_b, indent=2, ensure_ascii=False))

    # 4. Resumo e Conclusão
    print("\n" + "=" * 60)
    print("PIPELINE PALÁCIO VÍDEOS 6.0 CONCLUÍDO COM SUCESSO!")
    print(f"Versão A: {out_a} ({audit_a['size_mb']} MB, LUFS: {audit_a['audio_metrics']['integrated_lufs']})")
    print(f"Versão B: {out_b} ({audit_b['size_mb']} MB, LUFS: {audit_b['audio_metrics']['integrated_lufs']})")
    print("=" * 60)

if __name__ == "__main__":
    main()
