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
import chunksData from "./corte2_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "./motion-library/DynamicCaptions";
import { PalacioOutro } from "./motion-library/PalacioOutro";
import { ViralHeader } from "./motion-library/ViralHeader";
import { PALACIO_ACOLHIMENTO_BRAND } from "./motion-library/BrandConfig";

const chunks = chunksData as SubtitleChunk[];

export const Corte2CorrigidoComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // Outro nos últimos 68 frames (~2.26s)
  const outroStartFrame = durationInFrames - 68;
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 18],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* 1. Vídeo Original Tratado em 1080x1920 (9:16 vertical) */}
      <OffthreadVideo
        src={staticFile("corte2_video.mp4")}
        volume={0}
        style={{
          width: "100%",
          height: "100%",
          objectFit: "cover",
        }}
      />

      {/* 2. Trilha Sonora Masterizada (Pedalboard + SFX Narrativos + EBU R128) */}
      <Audio src={staticFile("corte2_audio.wav")} />

      {/* 3. Vinheta de Profundidade Cinematográfica Suave */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 40%, transparent 48%, rgba(6, 10, 8, 0.35) 85%, rgba(6, 10, 8, 0.75) 100%)",
          pointerEvents: "none",
        }}
      />

      {/* 4. Header Viral com Barra de Progresso, Marca PALÁCIO ACOLHIMENTO e Gancho Compacto */}
      <ViralHeader
        brand={PALACIO_ACOLHIMENTO_BRAND}
        title="NÃO QUERO PERDER VOCÊ"
        category="ALERTA SOBRE A VIDA • PALÁCIO ACOLHIMENTO"
        hookSubtitle="A dor de quem já perdeu amigos pra droga."
      />

      {/* 5. Legendas Dinâmicas Karaoke na ZONA SEGURA (bottom: 540px = Y central ~1300px) */}
      {frame < outroStartFrame && (
        <DynamicCaptions chunks={chunks} bottomPx={540} maxBoxWidth={860} />
      )}

      {/* 6. Encerramento Institucional Oficial PALÁCIO ACOLHIMENTO */}
      {frame >= outroStartFrame && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: `rgba(6, 10, 8, ${outroOpacity * 0.95})`,
            backdropFilter: `blur(${outroOpacity * 14}px)`,
            WebkitBackdropFilter: `blur(${outroOpacity * 14}px)`,
            opacity: outroOpacity,
            zIndex: 60,
          }}
        >
          <PalacioOutro
            brand={PALACIO_ACOLHIMENTO_BRAND}
            sloganHighlightWord="viver"
          />
        </div>
      )}
    </AbsoluteFill>
  );
};
