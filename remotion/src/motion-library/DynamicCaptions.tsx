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
}> = ({ chunks }) => {
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
        paddingBottom: "240px",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          display: "inline-flex",
          flexWrap: "wrap",
          justifyContent: "center",
          alignItems: "center",
          gap: "10px 16px",
          maxWidth: "920px",
          backgroundColor: "rgba(6, 10, 8, 0.78)",
          backdropFilter: "blur(18px)",
          WebkitBackdropFilter: "blur(18px)",
          border: `1.5px solid ${PALACIO_THEME.colors.borderGlass}`,
          boxShadow:
            "0 15px 40px rgba(0, 0, 0, 0.85), 0 0 25px rgba(212, 175, 55, 0.2)",
          borderRadius: "26px",
          padding: "20px 36px",
          textAlign: "center",
        }}
      >
        {activeChunk.words.map((w, idx) => {
          const isActive =
            currentTime >= w.start - 0.05 && currentTime <= w.end + 0.05;
          const isSpoken = currentTime > w.end + 0.05;

          const color = isActive
            ? PALACIO_THEME.colors.gold
            : isSpoken
            ? PALACIO_THEME.colors.textWhite
            : "rgba(240, 246, 252, 0.55)";

          const transform = isActive ? "scale(1.12)" : "scale(1.0)";
          const textShadow = isActive
            ? `0 0 25px rgba(212, 175, 55, 0.9), 0 0 50px rgba(212, 175, 55, 0.4)`
            : "0 2px 6px rgba(0, 0, 0, 0.8)";

          return (
            <span
              key={idx}
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "46px",
                fontWeight: 900,
                color,
                transform,
                textShadow,
                transition: "all 0.08s ease-out",
                display: "inline-block",
                margin: "4px 10px",
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
