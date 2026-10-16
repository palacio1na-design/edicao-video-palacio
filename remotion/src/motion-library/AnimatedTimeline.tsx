import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface TimelinePoint {
  label: string;
  yearOrStep?: string;
}

export interface AnimatedTimelineProps {
  points?: string[];
  highlightIndex?: number;
  accentColor?: string;
  width?: number;
}

/**
 * ANIMATED TIMELINE — MOTION GRAPHICS (FASE 7)
 * Linha do tempo minimalista para ilustrar passagem dos anos ou trajetória de vida.
 */
export const AnimatedTimeline: React.FC<AnimatedTimelineProps> = ({
  points = ["Início", "Alerta", "Presente"],
  highlightIndex = 1,
  accentColor = "#E5A93C",
  width = 750,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Entrada suave da linha principal
  const lineSpring = spring({
    frame,
    fps,
    config: { damping: 18, stiffness: 90, mass: 0.9 },
  });

  const lineWidth = interpolate(lineSpring, [0, 1], [0, width]);
  const opacity = interpolate(lineSpring, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        opacity,
        padding: "16px 24px",
        backgroundColor: "rgba(6, 10, 14, 0.72)",
        backdropFilter: "blur(12px)",
        borderRadius: 20,
        border: "1px solid rgba(229, 169, 60, 0.25)",
        boxShadow: "0 8px 32px rgba(0, 0, 0, 0.5)",
      }}
    >
      {/* LINHA HORIZONTAL */}
      <div
        style={{
          width: "100%",
          height: 4,
          backgroundColor: "rgba(255, 255, 255, 0.2)",
          position: "relative",
          margin: "32px 0 20px 0",
          borderRadius: 2,
        }}
      >
        <div
          style={{
            position: "absolute",
            left: 0,
            top: 0,
            height: "100%",
            width: lineWidth,
            backgroundColor: accentColor,
            borderRadius: 2,
            boxShadow: `0 0 12px ${accentColor}`,
          }}
        />

        {/* PONTOS DA LINHA DO TEMPO */}
        {points.map((pt, idx) => {
          const ptSpring = spring({
            frame: frame - (idx * 6 + 4),
            fps,
            config: { damping: 14, stiffness: 120 },
          });

          const isHighlighted = idx === highlightIndex;
          const pointScale = interpolate(ptSpring, [0, 1], [0, isHighlighted ? 1.3 : 1.0]);
          const leftPercent = (idx / (points.length - 1 || 1)) * 100;

          return (
            <div
              key={idx}
              style={{
                position: "absolute",
                left: `${leftPercent}%`,
                top: "50%",
                transform: `translate(-50%, -50%) scale(${Math.max(0, pointScale)})`,
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
              }}
            >
              {/* CÍRCULO NÓ */}
              <div
                style={{
                  width: isHighlighted ? 20 : 14,
                  height: isHighlighted ? 20 : 14,
                  borderRadius: "50%",
                  backgroundColor: isHighlighted ? accentColor : "#FFFFFF",
                  border: `3px solid ${isHighlighted ? "#060A0E" : "rgba(0,0,0,0.4)"}`,
                  boxShadow: isHighlighted ? `0 0 16px ${accentColor}` : "none",
                }}
              />

              {/* RÓTULO DO PONTO */}
              <span
                style={{
                  marginTop: 14,
                  fontFamily: "Inter, Montserrat, sans-serif",
                  fontSize: isHighlighted ? 22 : 18,
                  fontWeight: isHighlighted ? 800 : 600,
                  color: isHighlighted ? accentColor : "rgba(255, 255, 255, 0.85)",
                  letterSpacing: 0.5,
                  textTransform: "uppercase",
                  whiteSpace: "nowrap",
                }}
              >
                {pt}
              </span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
