---
name: edicao-video-palacio
description: >-
  Use esta skill sempre que Marcelo Palácio solicitar edição de vídeo, cortes virais para Instagram Reels,
  TikTok ou YouTube Shorts, análise de palestras/lives do canal Palácio Acolhimento, ou automação no CapCut Desktop.
---

# Edição Vídeo Palácio — Palácio Vídeos Pro 7.5 (Direção Criativa das 5 Skills)

Esta skill capacita o assistente a operar como **Engenheiro Audiovisual Principal e Diretor de Edição de Marcelo Palácio**, conectando os 5 motores de inteligência editorial com as **5 Skills de Direção Criativa** (inspiradas no Método de Inteligência Audiovisual / MIA), operando de forma 100% local no macOS Apple Silicon.

---

## 1. Identidade Visual Obrigatória (Inviolável)

> [!IMPORTANT]
> **REGRA DE OURO:** A marca pública oficial de todos os vídeos é **PALÁCIO ACOLHIMENTO**.
> - **Nome:** `Palácio Acolhimento`
> - **Instagram / Redes:** `@palacioacolhimento`
> - **Website:** `palacioacolhimento.com.br`
> - **Monograma:** "P" Dourado de Acolhimento Familiar.
> 
> É **terminantemente proibido** utilizar `Palácio.pro`, `@palacio.pro`, `Palácio Ponto Pro` ou `Palácio AI` em qualquer elemento visível ou audível do vídeo (títulos, legendas, rodapés, créditos ou marcas d'água). O sistema anti-regressão rejeita qualquer tentativa de publicação em desconformidade.

---

## 2. Princípios Fundamentais de Produção

1. **Zero Timestamps Imaginários:** Todo corte é derivado do áudio real mapeado acusticamente.
2. **Sincronia Palavra por Palavra:** Transcrição via Whisper com `word_timestamps=True` e sanitização de gírias/ritmo.
3. **Acoustic Silence Snapping (VAD):** Cortes cravados nos vales de silêncio reais pelo FFmpeg, preservando respiros e peso emocional.
4. **Respeito às Zonas Seguras das Redes Sociais:** Legendas e títulos nunca competem com a UI nativa de Reels, TikTok ou Shorts.
5. **Autenticidade Emocional:** Sem poluição de IA barata, sem marcas d'água de modelos generativos (ex: logotipo Veo). O foco é a verdade de Marcelo e o acolhimento à família.
6. **Ação Real na Linha do Tempo:** Decisões de estilo, ritmo, legendas, movimento e composição são convertidas em keyframes, camadas e áudios reais no Remotion.

---

## 3. As Cinco Skills de Direção Criativa

O sistema opera com 5 skills integradas (registradas em `~/.gemini/config/skills/`):

1. **`palacio-estilo`:** Direção de fotografia, Moody Cinema grade, vinheta perimetral, paleta Dourado/Esmeralda e identidade Palácio Acolhimento.
2. **`palacio-ritmo`:** Estruturação em 4 Atos (Gancho, Storytelling, Clímax e Resolução), pausas dramáticas preservadas e cortes semânticos.
3. **`palacio-legendas`:** Transcrição revisada palavra por palavra, karaoke cinético em Dourado Nobre (`#E5A93C`) e ancoragem em $Y = 1380\text{px}$ (`bottom: 540px`).
4. **`palacio-movimento`:** Câmera virtual anatômica (`transformOrigin: "50% 36%"`), punch-ins dramáticos aos ápices emocionais e física de mola (`spring()`).
5. **`palacio-composicao`:** Moldura 2.5D flutuante chanfrada, ambient blur ao fundo em 9:16, reflexo dourado e badges glassmorphism.

---

## 4. Arquitetura do Sistema e Motores Integrados

```
edicao-video-palacio/
├── SKILL.md                            # Diretrizes oficiais e fluxo operacional
├── PALACIO-PODCAST-30-CORTES.md        # Manual do Motor de 30 Cortes Virais para Podcasts
├── PALACIO-EVOLUCAO-AUTOBROLL.md       # Evolução AutoBroll: Montagem inteligente e corte narrativo
├── PALACIO-DIRECAO-CRIATIVA.md         # Relatório completo do método e comparativo de timeline
├── PALACIO-VIDEOS-INTEGRACAO-7.0.md    # Relatório executivo da integração dos motores
├── PALACIO-SOUND-DIRECTOR.md           # Manual de engenharia de áudio e Pedalboard
├── core/
│   ├── podcast_clipper.py             # MOTOR DE 30 CORTES (Ingestão, Whisper, Face Track, Dossiê)
│   ├── intelligent_montage_engine.py  # Motor de Montagem Inteligente (AutoBroll / Auto-Editor)
│   ├── creative_director.py           # MASTER CREATIVE DIRECTOR (Orquestrador das 5 Skills)
│   ├── pipeline.py                    # Master Pipeline Unificada
│   ├── brand_config.py                # Gestor de marca e detector anti-regressão
│   ├── social_safe_zones.py           # Calculador e validador de zonas seguras das redes
│   ├── smart_editor.py                # Motor 1: VAD acústico, alinhamento e cortes
│   ├── retention_director.py          # Motor 2: Pacing, ganchos e curvas de câmera virtual
│   ├── cinematic_director.py          # Motor 3: Color grading cinema e curadoria de B-roll
│   ├── sound_director.py              # Motor 4: Cadeia vocal Spotify Pedalboard e EBU R128 (-14 LUFS)
│   └── quality_director.py            # Motor 5: Auditoria determinística e inspeção de frames
└── remotion/                           # Motor de Renderização 1080x1920 (React 19 + Remotion)
    └── src/
        ├── creative-engine/
        │   ├── CleuzaCananComposition.tsx        # Estilo Consultório Humanizado (Sem molduras falsas)
        │   ├── IntelligentMontageComposition.tsx # Composição AutoBroll multicâmera A/B-Roll
        │   ├── CreativeFramedLayer.tsx           # Moldura 2.5D com ambient blur e reflexo dourado
        │   ├── CinematicAudioEngine.tsx          # Player determinístico de SFX frame a frame
        │   └── CreativeMasterComposition.tsx     # Composição Master com as 5 skills na timeline
        └── motion-library/
            ├── BrandConfig.ts                 # Contrato TypeScript Palácio Acolhimento
            ├── SocialSafeZones.ts             # Zonas seguras para componentes React
            ├── ViralHeader.tsx                # Cabeçalho compacto superior (top: 116px)
            ├── DynamicCaptions.tsx            # Legendas dinâmicas elevadas (bottom: 540px)
            ├── PalacioOutro.tsx               # Encerramento oficial com CTA e monograma
            └── ThreeDStepsScene.tsx           # Shaders e malhas 3D em Three.js
```

---

## 5. Fluxo de Execução e Renderização

### Renderizar a Composição Master Criativa
```bash
cd ~/.gemini/config/skills/edicao-video-palacio/remotion
npx remotion render corte-2-creative-master ~/Downloads/Corte_02_Vida_Serena_Palacio_Acolhimento_DIRECAO_CRIATIVA.mp4 --concurrency=7
```

### Finalização e Auditoria Acústica / Visual
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  /Users/palacio.pro/.gemini/antigravity/scratch/finalize_and_audit.py
```
Métricas de aprovação obrigatórias:
- Resolução Vertical 9:16 (1080x1920) @ 30fps.
- Áudio Masterizado: `-13.7` a `-14.1` LUFS, True Peak $\le -0.9\text{ dBFS}$, zero clipping.
- Marca 100% íntegra: Zero menções a `Palácio.pro`.
- Legendas e Títulos dentro da Zona Segura Universal.
