---
name: palacio-videos
description: >-
  Sistema profissional de criação, automação e motion design audiovisual Palácio.pro (v2.0).
  Utilize sempre que Marcelo Palácio solicitar edição de vídeo, motion design 3D, cortes virais para Instagram Reels,
  TikTok ou YouTube Shorts, animações gráficas com Remotion/Three.js, ou renderização de alta precisão.
---

# Palácio Vídeos 2.0 — Sistema Audiovisual Profissional

O **PALÁCIO VÍDEOS 2.0** é o ecossistema audiovisual e motor de motion design programático oficial da marca **Palácio.pro** e **Palácio Acolhimento**.

Ele combina inteligência editorial de ponta, alinhamento acústico palavra por palavra, motor 3D/Motion Design com Remotion e Three.js, e integração para acabamento no CapCut.

---

## 1. Princípios Inegociáveis da Marca

1. **Zero Timestamps Imaginários:** Nenhum corte é realizado por estimativa. Todo timestamp deriva da análise acústica real com Faster-Whisper e FFmpeg (`silencedetect`).
2. **Design Editorial Palácio.pro:** Estética cinematográfica, sóbria, elegante e acolhedora.
   - Verde Esmeralda (`#074B32` / `#0D6B4A`)
   - Dourado Realce (`#D4AF37` / `#F3E5AB`)
   - Preto Carvão Profundo (`#060A08`)
   - Tipografia limpa, bold e legível
3. **Respeito à Dor e à Mensagem Humana:** A temática de dependência química e acolhimento familiar exige seriedade e esperança. É proibido sensacionalismo barato, B-rolls descontextualizados ou poluição visual agressiva.
4. **Física Determinística com Spring:** Toda animação gráfica utiliza física de mola (`spring()`) do Remotion, garantindo movimentos naturais e sincronizados com a taxa de quadros (30 fps).

---

## 2. Estrutura do Ecossistema

O repositório está localizado em:
`~/.gemini/config/skills/edicao-video-palacio/`

### A. Motor de Motion Design (Remotion + Three.js)
Localizado em `edicao-video-palacio/remotion/`:
- **Framework:** Remotion `4.0.535` com `@remotion/three` e Three.js `0.178.0`
- **Componentes Centrais (`src/motion-library/`):**
  - `PalacioTheme.ts`: Design tokens, paleta e molas cinematográficas.
  - `ParallaxBackground.tsx`: Fundo dinâmico com orbes orgânicos esmeralda/dourado e grid de perspectiva.
  - `CinematicTitle.tsx`: Tipografia cinética escalonada com destaque em dourado.
  - `ThreeDStepsScene.tsx`: Cena 3D com ThreeCanvas e tokens geométricos rotativos (Torus Knot, Icosaedro e Octaedro).
  - `KineticStepCard.tsx`: Cards 2.5D com glassmorphism, indicador de etapas e safe zone vertical.
  - `PalacioOutro.tsx`: Encerramento com brasão P em relevo dourado, lema da recuperação e CTA Palácio Acolhimento.
  - `DemoShowreel.tsx`: Composição de 15s (1080x1920) demonstrando o fluxo completo.

### B. Motor Python de IA & Transcrição
Localizado em `edicao-video-palacio/core/`:
- `audio_aligner.py`: Extração WAV, Whisper word-timestamps e corte exato em vales de silêncio (VAD).
- `editorial_analyzer.py`: Identificação de ganchos virais, storytelling e geração de metadados SEO.
- `video_processor.py`: Recorte 9:16 (1080x1920), normalização EBU R128 (-14 LUFS) e render via FFmpeg.
- `capcut_bridge.py`: Exportação para projetos compatíveis com CapCut Desktop no macOS.

### C. Skills Oficiais do Remotion Integradas
Disponíveis globalmente em `~/.gemini/config/skills/`:
- `remotion-best-practices`: Boas práticas de arquitetura e performance.
- `remotion-create`: Geração de novas composições.
- `remotion-render`: Exportação via linha de comando (`npx remotion render`).
- `remotion-captions`: Tratamento e animação de legendas por palavra.
- `remotion-multimedia`: Áudio, crossfades e transições.
- `remotion-studio`: Interface gráfica interativa para pré-visualização.

---

## 3. Guia Operacional: Como Produzir Vídeos

### Fluxo 1: Criar Vídeo de Motion Design / 3D Programático
1. Abra o diretório do Remotion:
   ```bash
   cd ~/.gemini/config/skills/edicao-video-palacio/remotion
   ```
2. Para editar e testar com preview visual ao vivo:
   ```bash
   npm_config_cache=/tmp/npm-cache npm run dev
   # Ou: npx remotion preview
   ```
3. Para renderizar a composição em formato 9:16 (1080x1920):
   ```bash
   npx remotion render DemoShowreel ~/Downloads/NomeDoVideo.mp4 --concurrency=7
   ```

### Fluxo 2: Analisar Vídeo Longo e Cortar Melhores Momentos
1. Execute a mineração acústica real com a CLI:
   ```bash
   /Users/palacio.pro/.gemini/antigravity/scratch/.venv/bin/python \
     ~/.gemini/config/skills/edicao-video-palacio/cli.py analyze \
     "/caminho/do/video.mp4" --count 10
   ```
2. Revise os cortes no relatório gerado `review.html`.
3. Renderize os cortes selecionados ou importe para o CapCut Desktop via `capcut_bridge.py`.

### Fluxo 3: Combinar Corte Real com Overlays de Motion Design 3D
1. Use os componentes da `Palacio Motion Library` (`src/motion-library/`) sobrepostos ao vídeo do palestrante/corte.
2. Posicione títulos no terço superior e cards de reflexão (`KineticStepCard`) no terço inferior, preservando a área central para a expressão do interlocutor.

---

## 4. Checklist de Qualidade Obrigatório
- [ ] Duração exata e sincronia de quadros (30 fps).
- [ ] Resolução vertical 1080x1920 com safe zone para Reels/Shorts (150px de margem superior e inferior).
- [ ] Contraste tipográfico acessível com drop shadow e cores `#074B32`, `#D4AF37` e `#F0F6FC`.
- [ ] Encerramento com a assinatura institucional Palácio Acolhimento.
