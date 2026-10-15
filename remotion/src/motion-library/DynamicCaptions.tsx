import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

export interface WordToken {
  word: string;
  start: number;
  end: number;
}

export interface SubtitleChunk {
  start: number;
  end: number;
  text: string;
  words: WordToken[];
}

export const DynamicCaptions: React.FC<{
  chunks: SubtitleChunk[];
  bottomPx?: number; // Distância do chão (default 540px = Y central aprox 1300px)
  maxBoxWidth?: number;
}> = ({ chunks, bottomPx = 540, maxBoxWidth = 860 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentTime = frame / fps;

  // Encontrar o chunk ativo no segundo atual
  const activeChunk = chunks.find(
    (c) => currentTime >= c.start && currentTime <= c.end + 0.15,
  );

  if (!activeChunk) {
    return null;
  }

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: `${bottomPx}px`, // Elevado para respeitar a Zona Segura das redes
        pointerEvents: "none",
        zIndex: 55,
      }}
    >
      <div
        style={{
          display: "inline-flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "8px 14px",
          maxWidth: `${maxBoxWidth}px`,
          backgroundColor: "rgba(6, 10, 8, 0.85)",
          backdropFilter: "blur(20px)",
          WebkitBackdropFilter: "blur(20px)",
          border: `1.5px solid ${PALACIO_THEME.colors.borderGlass}`,
          boxShadow:
            "0 15px 40px rgba(0, 0, 0, 0.9), 0 0 20px rgba(212, 175, 55, 0.15)",
          borderRadius: "24px",
          padding: "16px 32px",
          textAlign: "center",
        }}
      >
        {activeChunk.words.map((w, idx) => {
          const isActive =
            currentTime >= w.start - 0.04 && currentTime <= w.end + 0.04;
          const isSpoken = currentTime > w.end + 0.04;

          const color = isActive
            ? PALACIO_THEME.colors.gold
            : isSpoken
            ? PALACIO_THEME.colors.textWhite
            : "rgba(240, 246, 252, 0.60)";

          const transform = isActive ? "scale(1.10)" : "scale(1.0)";
          const textShadow = isActive
            ? `0 0 20px rgba(212, 175, 55, 0.95), 0 0 40px rgba(212, 175, 55, 0.35)`
            : "0 2px 6px rgba(0, 0, 0, 0.9)";

          return (
            <span
              key={idx}
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "44px",
                fontWeight: 900,
                color,
                transform,
                textShadow,
                transition: "all 0.06s ease-out",
                display: "inline-block",
                margin: "4px 8px",
                letterSpacing: "0.5px",
              }}
            >
              {w.word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
