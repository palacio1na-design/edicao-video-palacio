import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface AnimatedKeywordsProps {
  keyword?: string;
  subtitle?: string;
  accentColor?: string;
  width?: number;
}

/**
 * ANIMATED KEYWORDS — MOTION GRAPHICS (FASE 7)
 * Destaque cinético e elegante de palavras-chave pronunciadas na fala.
 */
export const AnimatedKeywords: React.FC<AnimatedKeywordsProps> = ({
  keyword = "ACOLHIMENTO",
  subtitle = "PALÁCIO ACOLHIMENTO",
  accentColor = "#E5A93C",
  width = 820,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const popSpring = spring({
    frame,
    fps,
    config: { damping: 14, stiffness: 120, mass: 0.8 },
  });

  const scale = interpolate(popSpring, [0, 1], [0.8, 1.0]);
  const opacity = interpolate(popSpring, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        transform: `scale(${scale})`,
        opacity,
        padding: "16px 28px",
        backgroundColor: "rgba(6, 10, 14, 0.72)",
        backdropFilter: "blur(12px)",
        borderRadius: 20,
        border: "1px solid rgba(229, 169, 60, 0.3)",
        boxShadow: "0 8px 30px rgba(0, 0, 0, 0.5)",
      }}
    >
      {subtitle && (
        <span
          style={{
            fontFamily: "Inter, Montserrat, sans-serif",
            fontSize: 16,
            fontWeight: 700,
            color: "rgba(255, 255, 255, 0.65)",
            letterSpacing: 2.5,
            textTransform: "uppercase",
            marginBottom: 4,
          }}
        >
          {subtitle}
        </span>
      )}

      <h2
        style={{
          margin: 0,
          fontFamily: "Inter, Montserrat, sans-serif",
          fontSize: 48,
          fontWeight: 900,
          color: accentColor,
          letterSpacing: 1.5,
          textTransform: "uppercase",
          textShadow: `0 0 24px rgba(229, 169, 60, 0.45)`,
        }}
      >
        {keyword}
      </h2>
    </div>
  );
};
