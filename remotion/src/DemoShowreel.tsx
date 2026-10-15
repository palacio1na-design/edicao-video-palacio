import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import { CinematicTitle } from "./motion-library/CinematicTitle";
import { KineticStepCard } from "./motion-library/KineticStepCard";
import { PalacioOutro } from "./motion-library/PalacioOutro";
import { ParallaxBackground } from "./motion-library/ParallaxBackground";
import { ThreeDStepsScene } from "./motion-library/ThreeDStepsScene";

export const DemoShowreel: React.FC = () => {
  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* Fundo Parallax Cinemático Contínuo nos 450 frames */}
      <ParallaxBackground intensity={1} />

      {/* CENA 1: ABERTURA CINEMATOGRÁFICA (Frames 0 a 120 / 4s) */}
      <Sequence from={0} durationInFrames={120}>
        <ThreeDStepsScene step={1} />
        <CinematicTitle
          categoryBadge="PALÁCIO.PRO • FILOSOFIA"
          title="PARAR DE USAR É SÓ O PRIMEIRO PASSO"
          highlightWord="PRIMEIRO"
          subtitle="O que muitos ainda não entendem sobre a verdadeira recuperação."
        />
      </Sequence>

      {/* CENA 2 - ETAPA 1: PARAR (Frames 120 a 180 / 2s) */}
      <Sequence from={120} durationInFrames={60}>
        <ThreeDStepsScene step={1} />
        <KineticStepCard
          stepNumber={1}
          stepName="DESINTOXICAÇÃO"
          headline="1. Parar de Usar"
          explanation="Estabilizar o corpo e quebrar o ciclo químico é essencial, mas é apenas a porta de entrada."
          quote="Sem tratar a causa, a sobriedade torna-se insustentável."
        />
      </Sequence>

      {/* CENA 2 - ETAPA 2: CUIDAR (Frames 180 a 240 / 2s) */}
      <Sequence from={180} durationInFrames={60}>
        <ThreeDStepsScene step={2} />
        <KineticStepCard
          stepNumber={2}
          stepName="TERAPIA & EMOÇÕES"
          headline="2. Cuidar da Raiz"
          explanation="Acolher os traumas, a ansiedade e os conflitos que alimentavam a necessidade de fuga."
          quote="A mente precisa encontrar alívio e clareza na sobriedade."
        />
      </Sequence>

      {/* CENA 2 - ETAPA 3: RECONSTRUIR (Frames 240 a 300 / 2s) */}
      <Sequence from={240} durationInFrames={60}>
        <ThreeDStepsScene step={3} />
        <KineticStepCard
          stepNumber={3}
          stepName="NOVA VIDA"
          headline="3. Reconstruir a Vida"
          explanation="Restaurar a confiança com a família, cultivar novos hábitos e viver com propósito digno."
          quote="A recuperação se consolida na rotina de quem vive bem."
        />
      </Sequence>

      {/* CENA 3: OUTRO & AUTORIDADE PALÁCIO ACOLHIMENTO (Frames 300 a 450 / 5s) */}
      <Sequence from={300} durationInFrames={150}>
        <PalacioOutro />
      </Sequence>
    </AbsoluteFill>
  );
};
