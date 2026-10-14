# 🎬 Edição Vídeo Palácio.pro — Diretor Audiovisual & Editor Sênior com IA

> **Agente de Edição Audiovisual de Alta Precisão para Conteúdos Virais (Reels, TikTok e YouTube Shorts), com Sincronização Acústica por Palavra e B-Roll Contextual.**

Construído para o ecossistema de **Marcelo Palácio** ([Palácio Acolhimento](https://palacioacolhimento.com.br) & [Clínica Vida Serena](https://clinicavidaserena.com.br)), combinando o que há de mais avançado nas arquiteturas **AutoBroll**, **SynthCut** e **AI Video Editor**, operando de forma 100% local no macOS Apple Silicon.

---

## ✨ Principais Funcionalidades

* 🎙️ **Alinhamento a Nível de Palavra (Word-Level Timestamps):** Transcrição acústica precisa via Whisper em Português do Brasil.
* ✂️ **Acoustic Silence Snapping (Zero Cortes Decepados):** Análise em tempo real de silêncio acústico via FFmpeg (`silencedetect`). Os cortes são cravados cirurgicamente nos vales de silêncio antes do gancho e após a conclusão da fala. Nenhuma palavra é cortada ao meio e o respiro natural é preservado.
* 📱 **Reenquadramento Vertical 9:16 (1080x1920):** Enquadramento otimizado para Reels, Shorts e TikTok com aceleração por hardware da Apple (`h264_videotoolbox`).
* 🎞️ **B-Roll Contextual em Crossfade:** Inserção automática de imagens de apoio (instalações da clínica, depoimentos familiares, cenas reflexivas) com transições suaves em *dissolve*, sem interromper o fluxo da voz do apresentador.
* 🔊 **Normalização de Áudio EBU R128 (-14 LUFS):** Padrão profissional de sonoridade com True Peak a `-1.0 dB` para clareza e impacto máximo nas plataformas de vídeo curto.
* 🖥️ **Integração com CapCut Desktop:** Criação segura de projetos de rascunho em `com.lveditor.draft`, prontos para acabamento criativo.
* 🌐 **Central de Revisão HTML Interativa:** Página web com players lado a lado, transcrições e botão de cópia de legenda SEO em 1 clique.

---

## 🏗️ Estrutura do Projeto

```
edicao-video-palacio/
├── SKILL.md                         # Prompt mestre e instruções para Google Antigravity
├── README.md                        # Documentação do projeto
├── cli.py                           # Interface de Linha de Comando (CLI)
├── core/
│   ├── audio_aligner.py            # Extração WAV, Whisper word-timestamps e VAD Snapping
│   ├── editorial_analyzer.py       # Mineração de ganchos virais e storytelling
│   ├── video_processor.py          # Render 9:16, normalização EBU R128 e overlay de B-roll
│   ├── capcut_bridge.py            # Integração e exportação para o CapCut Desktop
│   └── review_html.py              # Gerador da Central de Revisão HTML
└── scripts/
    ├── cut_and_export_916.swift    # Utilitário Swift AVFoundation
    └── create_capcut_project.py    # Utilitário legado CapCut
```

---

## 🚀 Como Utilizar

### Pré-requisitos
* macOS (otimizado para Apple Silicon M1/M2/M3/M4)
* Python 3.9+
* FFmpeg 6.0+

### Instalação
```bash
git clone https://github.com/palacio1na-design/edicao-video-palacio.git
cd edicao-video-palacio
python3 -m venv .venv
source .venv/bin/activate
pip install openai-whisper
```

### 1. Minerar Cortes Virais do Vídeo Completo
```bash
python3 cli.py analyze "/caminho/do/video.mp4" --count 10
```

### 2. Renderizar os Cortes em 9:16 com Áudio Normalizado
```bash
python3 cli.py render "/caminho/do/video.mp4"
```

---

## 🎯 Pilares Editoriais Palácio.pro

1. **Fundo de Poço & Superação:** Histórias reais de dor e recomeço, sem romantização da doença.
2. **Acolhimento Familiar & Codependência:** O sofrimento de mães, pais e esposas que adoecem junto, e o amor firme que salva vidas.
3. **Quebra de Tabu sobre Internação:** Desmistificar o preconceito de "manicômio" e apresentar o tratamento humanizado com amor e ciência.
4. **Regra de Ouro da Sobriedade:** *"A única coisa que você não pode fazer é usar droga."*

---

## 📄 Licença
Distribuído sob licença MIT. Criado por Marcelo Palácio / Palácio.pro.
