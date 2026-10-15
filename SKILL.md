---
name: edicao-video-palacio
description: >-
  Use esta skill sempre que Marcelo Palácio solicitar edição de vídeo, cortes virais para Instagram Reels,
  TikTok ou YouTube Shorts, análise de palestras/lives do canal Palácio Acolhimento, ou automação no CapCut Desktop.
---

# Edição Vídeo Palácio — Palácio Vídeos Pro 7.0 (Integração Definitiva dos Motores)

Esta skill capacita o assistente a operar como **Engenheiro Audiovisual Principal e Diretor de Edição de Marcelo Palácio**, conectando os 5 motores de inteligência editorial, cinema, retenção, som e qualidade com processamento 100% local no macOS Apple Silicon.

---

## 1. Identidade Visual Obrigatória (Inviolável)

> [!IMPORTANT]
> **REGRA DE OURO:** A marca pública oficial de todos os vídeos é **PALÁCIO ACOLHIMENTO**.
> - **Nome:** `Palácio Acolhimento`
> - **Instagram / Redes:** `@palacioacolhimento`
> - **Website:** `palacioacolhimento.com.br`
> - **Monograma:** "P" Dourado de Acolhimento Familiar.
> 
> É **terminantemente proibido** utilizar `Palácio.pro`, `@palacio.pro`, `Palácio Ponto Pro` ou `Palácio AI` em qualquer elemento visível ou audível do vídeo (títulos, legendas, rodapés, créditos ou marcas d'água). `Palácio.pro` identifica apenas o ecossistema técnico do repositório/workspace.

---

## 2. Princípios Fundamentais de Produção

1. **Zero Timestamps Imaginários:** Todo corte é derivado do áudio real mapeado acusticamente.
2. **Sincronia Palavra por Palavra:** Transcrição via Whisper com `word_timestamps=True` e sanitização de gírias/ritmo.
3. **Acoustic Silence Snapping (VAD):** Cortes cravados nos vales de silêncio reais pelo FFmpeg, preservando respiros e peso emocional.
4. **Respeito às Zonas Seguras das Redes Sociais:** Legendas e títulos nunca competem com a UI nativa de Reels, TikTok ou Shorts.
5. **Autenticidade Emocional:** Sem poluição de IA barata, sem marcas d'água de modelos generativos (ex: logotipo Veo). O foco é a verdade de Marcelo e o acolhimento à família.

---

## 3. Arquitetura dos 5 Motores Integrados (`core/pipeline.py`)

```
edicao-video-palacio/
├── SKILL.md                            # Diretrizes oficiais e fluxo operacional
├── PALACIO-VIDEOS-INTEGRACAO-7.0.md    # Relatório executivo da integração dos motores
├── PALACIO-SOUND-DIRECTOR.md           # Manual de engenharia de áudio e Pedalboard
├── core/
│   ├── pipeline.py                    # MASTER PIPELINE (Orquestrador Central dos 5 Motores)
│   ├── brand_config.py                # Gestor de marca e detector anti-regressão
│   ├── social_safe_zones.py           # Calculador e validador de zonas seguras das redes
│   ├── smart_editor.py                # Motor 1: VAD acústico, alinhamento e cortes
│   ├── retention_director.py          # Motor 2: Pacing, ganchos e curvas de câmera virtual
│   ├── cinematic_director.py          # Motor 3: Color grading cinema e curadoria de B-roll
│   ├── sound_director.py              # Motor 4: Cadeia vocal Spotify Pedalboard e EBU R128 (-14 LUFS)
│   ├── quality_director.py            # Motor 5: Auditoria determinística e inspeção de frames
│   ├── audio_aligner.py               # Extração de áudio 16kHz e Whisper word-timestamps
│   ├── editorial_analyzer.py          # Mineração semântica e ganchos de alta retenção
│   └── capcut_bridge.py               # Integração com rascunhos do CapCut Desktop
└── remotion/                           # Motor de Renderização 1080x1920 (React 19 + Remotion)
    └── src/
        ├── motion-library/
        │   ├── BrandConfig.ts         # Contrato TypeScript de marca Palácio Acolhimento
        │   ├── SocialSafeZones.ts     # Zonas seguras e offsets para componentes React
        │   ├── ViralHeader.tsx        # Cabeçalho compacto superior (top: 116px)
        │   ├── DynamicCaptions.tsx    # Legendas dinâmicas elevadas (bottom: 540px)
        │   └── PalacioOutro.tsx       # Encerramento oficial com CTA e monograma
        ├── Corte2CorrigidoComposition.tsx
        └── Corte2CinematicoComposition.tsx
```

---

## 4. Engenharia de Zonas Seguras (Social Safe Zones)

Os elementos visuais respeitam rigorosamente a área útil das interfaces de Instagram Reels, TikTok, YouTube Shorts e Facebook Reels:

- **Cabeçalho de Título (`ViralHeader`):**
  - Posicionado em `top: 116px`.
  - Altura compacta (`72px`) no terço superior vazio.
  - Nunca encobre a testa ou a linha dos olhos de Marcelo.
  - Exibe o handle oficial `@palacioacolhimento`.
- **Legendas Dinâmicas (`DynamicCaptions`):**
  - Elevadas para `bottom: 540px` (linha vertical $Y \approx 1300\text{--}1380\text{px}$).
  - Livres de obstrução do botão de áudio, legenda nativa do feed e botões laterais de interação.
  - Efeito karaoke com destaque dourado (`#E5A93C`) na palavra falada.

---

## 5. Fluxo de Trabalho e Execução

### Execução via Master Pipeline 7.0 (Recomendado)
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  -m core.pipeline \
  --composition "corte-2-cinematico" \
  --output "/Users/palacio.pro/Downloads/Corte_Cinematico.mp4" \
  --brand "palacio-acolhimento" \
  --profile "SOCIAL_VERTICAL_MASTER"
```

### Renderização Direta via Remotion CLI
```bash
cd ~/.gemini/config/skills/edicao-video-palacio/remotion
npx remotion render corte-2-cinematico ~/Downloads/Corte_Cinematico.mp4 --concurrency=7
```

### Auditoria e Validação de Qualidade
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  /Users/palacio.pro/.gemini/antigravity/scratch/test_palacio_videos_7.py
```
Critérios de aprovação obrigatórios:
- Formato Vertical 9:16 (1080x1920) @ 30fps.
- Áudio Masterizado: Loudness integrado entre `-14.5` e `-13.5` LUFS, True Peak $\le -0.9\text{ dBFS}$, zero clipping.
- Marca 100% íntegra: Rejeição imediata se contiver `Palácio.pro` ou `@palacio.pro`.
- Legendas e Títulos dentro dos limites do validador de Zonas Seguras.
