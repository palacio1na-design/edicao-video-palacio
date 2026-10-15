---
name: edicao-video-palacio
description: >-
  Use esta skill sempre que Marcelo Palácio solicitar edição de vídeo, cortes virais para Instagram Reels,
  TikTok ou YouTube Shorts, análise de palestras/lives do canal Palácio Acolhimento, ou automação no CapCut Desktop.
---

# Edição Vídeo Palácio.pro — Diretor Audiovisual & Editor Sênior de Alta Precisão

Esta skill capacita o assistente a operar como Engenheiro Audiovisual Sênior e Diretor de Edição de Marcelo Palácio, integrando soluções modernas dos ecossistemas **AutoBroll**, **SynthCut** e **AI Video Editor**, com processamento 100% local no macOS Apple Silicon.

## Princípios Fundamentais (Invioláveis)
1. **Zero Timestamps Imaginários:** Nenhum corte é realizado por estimativa ou intuição da IA. Todo timestamp deriva da análise do áudio real.
2. **Alinhamento a Nível de Palavra:** Transcrição acústica sincronizada palavra por palavra via Whisper com `word_timestamps=True`.
3. **Acoustic Silence Snapping (VAD):** O início e o fim de cada corte são cravados cirurgicamente nos vales de silêncio detectados pelo FFmpeg (`silencedetect`), garantindo que nenhuma sílaba seja decepada e que as pausas emocionais e o respiro natural sejam preservados.
4. **Verdade e Autenticidade:** Edições sem poluição visual, sem sensacionalismo vazio e sem B-rolls que desvirtuem a seriedade da recuperação e do acolhimento familiar.

---

## Arquitetura do Sistema (v6.0 — Superpoderes de Edição e Design de Som)

```
edicao-video-palacio/
├── SKILL.md                         # Diretrizes, arquétipos e documentação
├── PALACIO-SOUND-DIRECTOR.md        # Manual oficial de design de som e engenharia de áudio
├── edit-plan.json                   # Plano executável de cortes, escalas e cor
├── sound-plan.json                  # Plano executável de trilha, SFX e ducking
├── assets/sound-library/            # Palácio Cinematic Sound Library (48kHz/24-bit)
├── core/
│   ├── smart_editor.py             # PALÁCIO SMART EDITOR (Orquestrador Central)
│   ├── sound_director.py           # PALÁCIO SOUND DIRECTOR (Pedalboard, SFX e EBU R128)
│   ├── retention_director.py       # PALÁCIO RETENTION DIRECTOR (Pacing e punch-ins)
│   ├── cinematic_director.py       # PALÁCIO CINEMATIC DIRECTOR (Color grading e vinheta)
│   ├── quality_director.py         # PALÁCIO QUALITY DIRECTOR (Autocrítica e auditoria)
│   ├── audio_aligner.py            # Extração WAV, Whisper word-timestamps, VAD silence snapping
│   ├── editorial_analyzer.py       # Mineração dos momentos de ouro, ganchos e SEO
│   └── capcut_bridge.py            # Integração segura com CapCut Desktop
└── remotion/                        # Motor de Motion Design 2.0 (React + Three.js)
```

---

## Inteligência Editorial Palácio.pro

O editor é especializado nos pilares de Marcelo Palácio:
1. **Dependência Química & Fundo de Poço:** Histórias viscerais de dor, peso corporal (ex: "quando cheguei na clínica com 55 kg"), internação involuntária e renascimento.
2. **Acolhimento Familiar & Codependência:** O sofrimento de mães, pais e esposas; a família que adoece junto; como amar sem ser conivente.
3. **Tratamento Humanizado & Clínica Vida Serena:** Quebra do estigma de manicômio; internação como ato de amor, respeito e suporte médico.
4. **Superação & Nova Vida:** A sobriedade como conquista diária e transformação de vidas.

### Estrutura de um Corte Viral Perfeito
- **Gancho (0 a 3 segundos):** Frase de impacto direto que interrompe o feed e seleciona o público qualificado.
- **Desenvolvimento (15 a 45 segundos):** Narrativa autêntica, ritmo envolvente, pausas dramáticas preservadas.
- **Fechamento (5 a 10 segundos):** Reflexão profunda ou virada de chave que gera identificação e compartilhamentos.

---

## Fluxo Operacional Definitivo

### 1. Mineração e Análise do Áudio Real
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  ~/.gemini/config/skills/edicao-video-palacio/cli.py analyze \
  "/caminho/do/video.mp4" --count 7
```
- Extrai áudio mono 16kHz PCM WAV.
- Mapeia todos os silêncios acústicos com FFmpeg VAD.
- Transcreve palavras com Whisper `base` em `pt-BR`.
- Minera os 7 melhores cortes com início/fim em silêncios reais.
- Gera `cuts_manifest.json` e `review.html`.

### 2. Renderização em Formato Reels/Shorts/TikTok
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  ~/.gemini/config/skills/edicao-video-palacio/cli.py render \
  "/caminho/do/video.mp4"
```
- Recorte 9:16 vertical (1080x1920) com Marcelo perfeitamente centralizado.
- Normalização de áudio profissional EBU R128 (`-14 LUFS`, True Peak `-1.0 dB`).
- Renderização ultra-rápida via Apple VideoToolbox (`h264_videotoolbox`).
- Gera arquivos `.mp4` limpos e arquivos `.srt` sincronizados palavra por palavra.
- Opção `--subtitles` para queimar legendas dinâmicas se desejado.
- Opção `--capcut` para criar os rascunhos no CapCut Desktop.

### 3. Revisão e Publicação
- Abra o arquivo `review.html` no Safari ou Chrome para assistir aos cortes, conferir a métrica de validação acústica e copiar a legenda SEO com 1 clique.
