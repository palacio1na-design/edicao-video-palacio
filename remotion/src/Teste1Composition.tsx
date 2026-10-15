import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  Sequence,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "./corte05_chunks.json";
import { DynamicCaptions, SubtitleChunk } from "./motion-library/DynamicCaptions";
import { PalacioOutro } from "./motion-library/PalacioOutro";
import { ViralHeader } from "./motion-library/ViralHeader";

const chunks = chunksData as SubtitleChunk[];

export const Teste1Composition: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Transição de fade suave para o Outro nos últimos 75 frames (2.5s)
  const outroStartFrame = durationInFrames - 75;
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 25],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* 1. Vídeo Original Limpo de Alta Resolução */}
      <OffthreadVideo
        src={staticFile("corte05.mp4")}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* 2. Leve vinheta cinematográfica nas bordas para destacar o sujeito e as legendas */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 40%, transparent 45%, rgba(6, 10, 8, 0.45) 85%, rgba(6, 10, 8, 0.85) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 3. Header Viral, Marca Palácio Acolhimento e Barra de Progresso */}
      <ViralHeader
        title="MEU PAI FECHOU O APARTAMENTO"
        category="AMOR EXIGENTE • PALÁCIO.PRO"
        hookSubtitle="O limite difícil que me tirou da ilusão."
      />

      {/* 4. Legendas Dinâmicas Sincronizadas Palavra por Palavra */}
      {frame < outroStartFrame && <DynamicCaptions chunks={chunks} />}

      {/* 5. Fechamento Institucional / Outro com Brasão P nos últimos segundos */}
      {frame >= outroStartFrame && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: `rgba(6, 10, 8, ${outroOpacity * 0.95})`,
            backdropFilter: `blur(${outroOpacity * 12}px)`,
            WebkitBackdropFilter: `blur(${outroOpacity * 12}px)`,
            opacity: outroOpacity,
            zIndex: 60,
          }}
        >
          <PalacioOutro />
        </div>
      )}
    </AbsoluteFill>
  );
};
