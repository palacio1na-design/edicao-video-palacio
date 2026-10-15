# PALÁCIO PODCAST CLIPPER 8.0 — O MOTOR DE 30 CORTES VIRAIS
## Sistema Industrial de Repurposing Audiovisual, Face Tracking e Mineração de Destaques
**Palácio Acolhimento | Palácio.pro — Tecnologia e Humanização Audiovisual**

---

## 1. VISÃO GERAL DA ARQUITETURA

O **Palácio Podcast Clipper** foi concebido para atender à demanda de transformar podcasts, palestras ou lives longas (de 1h a 3h) em um lote de **até 30 cortes curtos verticais (9:16)** de altíssimo impacto emocional e retenção, prontos para publicação no Instagram Reels, TikTok e YouTube Shorts.

O motor incorpora o **Estilo Humanizado da Dra. Cleuza Canan**, eliminando o excesso de molduras gráficas e efeitos artificiais em prol da **sobriedade clínica, autoridade acolhedora e conexão olho no olho com a família**.

```
[ Vídeo Longo 1h - 3h ] (MP4 Local ou Link YouTube via yt-dlp)
           │
           ▼
[ Whisper Acoustic Transcriber ] ──> Transcrição integral com timestamps palavra por palavra
           │
           ▼
[ Gemini Viral Highlight Miner ] ──> Mineração dos 30 melhores blocos (30s a 60s)
           │                          com ganchos familiares, dor, limites e superação
           ▼
[ MediaPipe Face Tracker ]       ──> Auto-crop inteligente 16:9 -> 9:16 mantendo o orador no centro
           │
           ▼
[ Remotion CleuzaCanan Engine ]  ──> Renderização 1080x1920:
           │                          • Headline no Topo (Zona Segura Superior)
           │                          • Legendas dinâmicas em Dourado Nobre
           │                          • Alternância de Câmeras (Plano A -> Close B nos olhos)
           │                          • Cama musical de piano a -24 dB abaixo da voz
           │                          • Monograma "P" Dourado de Encerramento
           ▼
[ Masterização EBU R128 ]        ──> -14.0 LUFS cravado, True Peak <= -0.9 dBFS (Spotify Pedalboard)
           │
           ▼
[ Pasta de Exportação ]          ──> 30 Vídeos MP4 + Dossiê Markdown + Catálogo CSV com Copies
```

---

## 2. FERRAMENTAS E BIBLIOTECAS INCORPORADAS DO GITHUB

Todas as ferramentas foram instaladas e configuradas nativamente no ambiente Apple Silicon:

1. **`yt-dlp`:** Baixa automaticamente qualquer live ou podcast do YouTube pelo link em máxima resolução (`1080p`).
2. **`OpenAI Whisper`:** Extração acústica e transcrição no milissegundo de cada palavra (`word_timestamps=True`).
3. **`MediaPipe & OpenCV` (`opencv-contrib-python`):** Rastreamento de pontos nodais faciais em tempo real e cálculo de centroide amortecido para cortes 9:16 sem solavancos.
4. **`Auto-Editor`:** Motor nativo em binário arm64 para remoção cirúrgica de silêncios mantendo margens de respiro natural (`0.15s` a `0.25s`).
5. **`Spotify Pedalboard & FFmpeg loudnorm`:** Equalizador de presença vocal, controle de dinâmica e masterização EBU R128 (-14.0 LUFS, True Peak $\le -0.9\text{ dBFS}$).
6. **`Remotion v4 + React 19`:** Renderização determinística de alta fidelidade em 1080x1920 a 30fps.

---

## 3. O ESTILO EDITORIAL CLEUZA CANAN (PALÁCIO ACOLHIMENTO)

A nova composição [`CleuzaCananComposition.tsx`](file:///Users/palacio.pro/.gemini/config/skills/edicao-video-palacio/remotion/src/creative-engine/CleuzaCananComposition.tsx) adota 5 regras estéticas fundamentais:

* **Zero Poluição Visual:** O vídeo de Marcelo ocupa a tela inteira em 9:16 nativo (1080x1920), eliminando molduras flutuantes 2.5D ou fundos desfocados falsos.
* **Headline de Gancho no Topo:** Barra superior ancorada na Zona Segura (`top: 130px`) com pergunta cortante para as famílias (ex: *"POR QUE VOCÊ NÃO CONSEGUE DIZER NÃO?"*).
* **Legenda Dinâmica Sóbria:** Posicionada a `540px` da base (Universal Safe Zone), com tipografia limpa, cor branca e iluminação em dourado nobre (`#E5A93C`) apenas na palavra falada.
* **Alternância de Câmeras Invisível:** Transição suave entre Plano Médio (1.0x) e Plano Fechado / Close nos Olhos (1.16x) cravado exatamente nos ápices emocionais da fala.
* **Cama Sonora de Piano Emotivo:** Trilha de piano acústico suave mixada a `-24 dB` abaixo da voz com voice-ducking automático (o piano nunca compete com a fala).

---

## 4. COMO EXECUTAR O PROCESSAMENTO DE UM PODCAST COMPLETO

### Processar um arquivo local de palestra/podcast:
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  /Users/palacio.pro/.gemini/config/skills/edicao-video-palacio/core/podcast_clipper.py \
  "/Users/palacio.pro/Downloads/Tematica Vida serena.mp4" \
  --max-cuts 30
```

### Processar diretamente de uma URL do YouTube:
```bash
/Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
  /Users/palacio.pro/.gemini/config/skills/edicao-video-palacio/core/podcast_clipper.py \
  "https://www.youtube.com/watch?v=SEU_PODCAST" \
  --max-cuts 30
```

---

## 5. RESULTADO DA EXPORTAÇÃO

Ao final do processamento de um podcast longo, o sistema gera na pasta:
`/Users/palacio.pro/Downloads/Palacio_30_Cortes_Podcast/`

1. **30 Vídeos Verticais em MP4 Masterizados:**
   * `Corte_01_Nota95_O_Erro_Que_Toda_Familia_Comete.mp4`
   * `Corte_02_Nota92_Por_Que_Voce_Nao_Consegue_Dizer_Nao.mp4`
   * ...
   * `Corte_30_...mp4`
2. **`DOSSIE_30_CORTES_PODCAST.md`:** Relatório com minutagem de início/fim, transcrição completa da fala e copy persuasiva pronta para copiar e colar no Instagram.
3. **`catalogo_30_cortes.csv`:** Planilha estruturada para agendamento em ferramentas como Meta Business Suite, mLabs ou Notion.
