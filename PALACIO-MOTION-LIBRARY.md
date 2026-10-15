# PALÁCIO MOTION LIBRARY
**Biblioteca de Componentes Visuais, Motion Design e Elementos 3D**
*Design System Oficial para Vídeos Palácio.pro & Palácio Acolhimento*

---

## 1. Identidade Visual & Design Tokens (`PalacioTheme.ts`)

A biblioteca obedece rigorosamente às cores da marca, pensadas para transmitir **sobriedade, autoridade, esperança e elegância cinematográfica**:

| Token | Hex / Valor | Significado Audiovisual |
| :--- | :--- | :--- |
| `deepGreen` | `#074B32` | Verde esmeralda profundo, base de estabilidade e acolhimento |
| `emeraldLight` | `#0D6B4A` | Verde esmeralda vivo para realces de luz e progressão |
| `gold` | `#D4AF37` | Dourado nobre oficial para destaques, palavras-chave e brasões |
| `goldLight` | `#F3E5AB` | Dourado suave para títulos secundários e reflexos 3D |
| `darkBg` | `#060A08` | Preto carvão com matiz esmeralda, contraste premium |
| `cardBg` | `rgba(13, 22, 18, 0.75)` | Fundo com glassmorphism fosco 2.5D |
| `borderGlass` | `rgba(212, 175, 55, 0.25)` | Borda translúcida dourada para profundidade |

### Física de Animação (Springs)
- **`snappy`** (`damping: 15, mass: 0.8, stiffness: 120`): Entradas rápidas de badges e títulos dinâmicos.
- **`gentle`** (`damping: 20, mass: 1.2, stiffness: 80`): Transição orgânica de cards e objetos 3D.
- **`cinematic`** (`damping: 28, mass: 2.0, stiffness: 60`): Câmera lenta, revelações monumentais e encerramento.

---

## 2. Componentes da Biblioteca

### 2.1 `ParallaxBackground.tsx`
Fundo dinâmico com orbes de luz esmeralda e dourada que se movem de forma orgânica e sutil, complementados por uma malha quadriculada de perspectiva de cinema.
- **Props**: `intensity?: number` (controla a velocidade e amplitude do movimento).

### 2.2 `CinematicTitle.tsx`
Tipografia cinética de alto impacto com revelação palavra a palavra escalonada (stagger de 3 frames), rotação tridimensional e suporte a palavra em destaque dourado com drop shadow luminoso.
- **Props**:
  - `title: string` (ex: `"PARAR DE USAR É SÓ O PRIMEIRO PASSO"`)
  - `highlightWord?: string` (ex: `"PRIMEIRO"`)
  - `subtitle?: string` (frase de apoio reflexiva)
  - `categoryBadge?: string` (ex: `"PALÁCIO.PRO • FILOSOFIA"`)

### 2.3 `ThreeDStepsScene.tsx`
Cena 3D com ThreeCanvas, iluminação de estúdio multi-ponto e tokens geométricos tridimensionais rotativos:
- **`step === 1`**: Nó Toroidal Dourado (`torusKnotGeometry`) com anel esmeralda — representa a quebra do ciclo e a interrupção do uso.
- **`step === 2`**: Icosaedro Esmeralda com Wireframe Dourado (`icosahedronGeometry`) — representa o cuidado com a mente e as múltiplas facetas emocionais.
- **`step === 3`**: Octaedro Diamante com anéis orbitais cruzados (`octahedronGeometry`) — representa a solidez da vida reconstruída.
- **Props**: `step: 1 | 2 | 3`

### 2.4 `KineticStepCard.tsx`
Card flutuante 2.5D em glassmorphism posicionado estrategicamente na base do vídeo vertical (safe zone de Reels/TikTok), com stepper visual de progresso (pontos 1, 2, 3), badge superior, headline, corpo de texto e citação em itálico com barra dourada.
- **Props**:
  - `stepNumber: 1 | 2 | 3`
  - `stepName: string`
  - `headline: string`
  - `explanation: string`
  - `quote?: string`

### 2.5 `PalacioOutro.tsx`
Encerramento com o brasão monograma "P" dourado com gradiente metálico, lema central da recuperação (*"A recuperação continua na forma de viver"*), marca institucional **PALÁCIO ACOLHIMENTO** e pill de contato (`palacioacolhimento.com.br • @palacio.pro`).

---

## 3. Como Montar Novos Vídeos no Remotion

Exemplo de orquestração no Remotion:

```tsx
import { AbsoluteFill, Sequence } from "remotion";
import { ParallaxBackground } from "./motion-library/ParallaxBackground";
import { CinematicTitle } from "./motion-library/CinematicTitle";
import { ThreeDStepsScene } from "./motion-library/ThreeDStepsScene";
import { KineticStepCard } from "./motion-library/KineticStepCard";
import { PalacioOutro } from "./motion-library/PalacioOutro";

export const MeuCorteViral: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      <ParallaxBackground />
      
      {/* 0 a 3s: Gancho Forte */}
      <Sequence from={0} durationInFrames={90}>
        <ThreeDStepsScene step={1} />
        <CinematicTitle
          title="A FAMÍLIA TAMBÉM PRECISA DE TRATAMENTO"
          highlightWord="FAMÍLIA"
          subtitle="O que a codependência faz com quem ama."
        />
      </Sequence>

      {/* 3s a 8s: Explicação com Card e Objeto 3D */}
      <Sequence from={90} durationInFrames={150}>
        <ThreeDStepsScene step={2} />
        <KineticStepCard
          stepNumber={2}
          stepName="ACOLHIMENTO"
          headline="Cuidar de Si para Ajudar o Outro"
          explanation="Quando a família muda de postura, todo o ambiente de recuperação se transforma."
        />
      </Sequence>

      {/* 8s a 12s: Encerramento Oficial */}
      <Sequence from={240} durationInFrames={120}>
        <PalacioOutro />
      </Sequence>
    </AbsoluteFill>
  );
};
```
