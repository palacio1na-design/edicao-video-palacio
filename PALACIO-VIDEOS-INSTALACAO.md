# PALÁCIO VÍDEOS 2.0 — GUIA DE INSTALAÇÃO E ARQUITETURA
**Sistema Audiovisual Profissional com Remotion, Motion Design 3D e Inteligência Gemini**
*Marca Oficial: Palácio.pro | Palácio Acolhimento*

---

## 1. Visão Geral da Arquitetura 2.0

O **PALÁCIO VÍDEOS 2.0** unifica o motor de inteligência editorial pré-existente (análise semântica, alinhamento palavra por palavra com Faster-Whisper/FFmpeg e integração CapCut) a um motor gráfico profissional de **Motion Design Programático e 3D**, construído sobre **Remotion**, **React Three Fiber (R3F)** e **Three.js**.

```
edicao-video-palacio/
├── core/                        # Motor Python de IA & Audiovisual
│   ├── audio_aligner.py         # Transcrição Whisper com alinhamento por palavra
│   ├── video_processor.py       # Extração, cortes precisos e renderização FFmpeg
│   ├── editorial_analyzer.py    # Ganchos virais e storytelling humanizado
│   └── capcut_bridge.py         # Integração com CapCut Desktop
├── remotion/                    # Motor de Motion Design 2.0 (React + Three.js)
│   ├── package.json             # Remotion 4.0.535, @remotion/three, three 0.178
│   ├── src/
│   │   ├── motion-library/      # Palácio Motion Library (componentes reutilizáveis)
│   │   │   ├── PalacioTheme.ts           # Paleta oficial (#074B32, #D4AF37, #060A08)
│   │   │   ├── ParallaxBackground.tsx    # Fundo orgânico esmeralda/dourado
│   │   │   ├── CinematicTitle.tsx        # Tipografia cinética com spring physics
│   │   │   ├── ThreeDStepsScene.tsx      # Cena 3D determinística com R3F
│   │   │   ├── KineticStepCard.tsx       # Cards 2.5D com glassmorphism e steppers
│   │   │   └── PalacioOutro.tsx          # Encerramento com brasão P e assinatura
│   │   ├── DemoShowreel.tsx     # Composição vertical 9:16 (1080x1920) de 15s
│   │   └── Root.tsx             # Registro oficial de composições Remotion
└── docs/                        # Documentações técnicas e bibliotecas
```

---

## 2. Dependências e Tecnologias Instaladas

### Remotion & Ecossistema 3D (macOS Apple Silicon nativo)
- **Remotion**: `4.0.535`
- **@remotion/cli**: `4.0.535`
- **@remotion/three**: `4.0.535`
- **@react-three/fiber**: `9.2.0`
- **three**: `0.178.0`
- **react / react-dom**: `19.2.3`
- **chrome-headless-shell**: ARM64 nativo instalado em cache de sistema

### Licença Comercial Remotion
- Remotion utiliza a **Remotion Free License (Company License)**:
  - Uso gratuito para pessoas físicas e empresas com **até 3 pessoas**.
  - O uso na marca **Palácio.pro / Palácio Acolhimento** está 100% em conformidade com os termos comerciais oficiais.

### Skills Oficiais do Remotion Instaladas
Instaladas no ecossistema global Antigravity (`~/.gemini/config/skills/`):
- `remotion-best-practices`: Regras arquiteturais, renderização determinística e hooks
- `remotion-create`: Scaffold e criação rápida de novas composições
- `remotion-render`: Comandos de linha para exportação MP4, ProRes e H.264
- `remotion-captions`: Tratamento e sincronização de legendas por palavra
- `remotion-markup`: Ingestão e animação de SVGs e vetores
- `remotion-multimedia`: Tratamento de áudio, crossfades e vídeos
- `remotion-studio`: Gerenciamento do preview em tempo real via localhost

---

## 3. Comandos de Uso

### 3.1 Abrir o Remotion Studio (Preview Visual em Tempo Real)
```bash
cd ~/.gemini/config/skills/edicao-video-palacio/remotion
npm_config_cache=/tmp/npm-cache npm run dev
# Ou diretamente:
npx remotion preview
```
Abre a interface interativa no navegador para ajuste fino de keyframes, textos e 3D.

### 3.2 Renderizar Vídeo MP4 (Linha de Comando)
```bash
cd ~/.gemini/config/skills/edicao-video-palacio/remotion
npx remotion render DemoShowreel ~/Downloads/MeuVideo_9x16.mp4
```

### 3.3 Renderizar com Resolução ou Concorrência Customizada
```bash
# Renderizar com 7 threads paralelas (otimizado para Apple Silicon M-series):
npx remotion render DemoShowreel ~/Downloads/Video_High.mp4 --concurrency=7 --codec=h264
```

---

## 4. Validação Técnica do Primeiro Vídeo Produzido

- **Arquivo**: `/Users/palacio.pro/Downloads/Palacio_Videos_Demo_15s_3D.mp4`
- **Formato**: MP4 H.264 / AAC
- **Resolução**: 1080 x 1920 (9:16 Vertical)
- **Duração**: Exatos 15,00 segundos (450 frames a 30 fps)
- **Tempo de renderização**: 7,52 segundos (velocidade ~60 fps de render!)
- **Composições validadas**:
  1. Tipografia cinética com stagger word-by-word e spring physics
  2. Cena 3D com 3 tokens representativos (Torus Knot, Icosaedro e Octaedro)
  3. Cards 2.5D de glassmorphism com controle de etapas de recuperação
  4. Encerramento institucional Palácio Acolhimento
