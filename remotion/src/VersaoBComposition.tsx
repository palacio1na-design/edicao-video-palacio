import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "./corte05_chunks.json";
import { DynamicCaptions, SubtitleChunk } from "./motion-library/DynamicCaptions";
import { PalacioOutro } from "./motion-library/PalacioOutro";
import { ViralHeader } from "./motion-library/ViralHeader";

// Filtrar chunks que estão dentro da janela narrativa de 38.8s
const allChunks = chunksData as SubtitleChunk[];
const chunks = allChunks.filter((c) => c.start < 38.5);

export const VersaoBComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Outro nos últimos 75 frames (2.5s)
  const outroStartFrame = durationInFrames - 75;
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 20],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* 1. Vídeo Original em 1080x1920 (mudo para dar lugar ao áudio masterizado) */}
      <OffthreadVideo
        src={staticFile("corte05.mp4")}
        volume={0}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* 2. Trilha Sonora Multitrack Masterizada (Voz Pedalboard + SFX + EBU R128) */}
      <Audio src={staticFile("versao_b_soundtrack.wav")} />

      {/* 3. Vinheta de Profundidade */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 40%, transparent 45%, rgba(6, 10, 8, 0.4) 85%, rgba(6, 10, 8, 0.8) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 4. Header Viral com Barra de Progresso e Gancho Dinâmico */}
      <ViralHeader
        title="MEU PAI FECHOU O APARTAMENTO"
        category="AMOR EXIGENTE • PALÁCIO.PRO"
        hookSubtitle="O limite difícil que me tirou da ilusão."
      />

      {/* 5. Legendas Dinâmicas Karaoke Sincronizadas */}
      {frame < outroStartFrame && <DynamicCaptions chunks={chunks} />}

      {/* 6. Encerramento com Brasão Palácio Acolhimento */}
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
