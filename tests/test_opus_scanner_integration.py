#!/usr/bin/env python3
"""
TESTE DE INTEGRAÇÃO: PALÁCIO SCANNER -> PALÁCIO EDITOR
Verifica se as ferramentas de engenharia reversa do Opus Clip estão 100% integradas.
"""

import os
import sys
import json

sys.path.insert(0, "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio")
from core.opus_scanner_bridge import OpusViralityScorer, OpusCurator, execute_scanner_editor_integration

def test_integration():
    print("Iniciando bateria de testes do Acoplamento Scanner -> Editor...")
    
    # 1. Testar Scorer com 4 Pesos
    scorer = OpusViralityScorer()
    sample_text = "Ontem na palestra um rapaz levantou a mão e falou: Marcelo, meu amigo morreu! E eu perdi amigos pra droga... E eu não quero que seja você. Não quero perder você pra droga. Tem uma família chorando por trás esperando você. Vem pro acolhimento!"
    score_res = scorer.calculate_score(sample_text, 0.0, 28.4)
    
    assert score_res["weights"]["hook"] == 0.35, "Peso do Hook incorreto"
    assert score_res["weights"]["autonomy"] == 0.30, "Peso da Autonomia incorreto"
    assert score_res["weights"]["value"] == 0.20, "Peso do Valor incorreto"
    assert score_res["weights"]["pacing"] == 0.15, "Peso do Ritmo incorreto"
    assert 0 <= score_res["virality_score"] <= 99, "Score fora da escala 0-99"
    print(f"✓ Teste 1 (Fórmula dos 4 Pesos): PASSOU (Score={score_res['virality_score']}/99)")

    # 2. Testar Curadoria na Transcrição Longa
    res = execute_scanner_editor_integration(
        transcript_path="/Users/palacio.pro/.gemini/antigravity/scratch/transcript.json",
        min_threshold=75,
        max_clips=5
    )
    assert res["success"] is True, "Falha na execução da integração"
    assert res["cuts_mined"] > 0, "Nenhum corte minerado"
    assert len(res["queue"]) > 0, "Fila de renderização vazia"
    print(f"✓ Teste 2 (Mineração e Fila de Renderização): PASSOU ({res['cuts_mined']} cortes minerados)")

    print("\nTODOS OS TESTES DE INTEGRAÇÃO PASSARAM COM SUCESSO!")

if __name__ == "__main__":
    test_integration()
