import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface AnimatedProcessProps {
  steps?: string[];
  activeStep?: number;
  accentColor?: string;
  width?: number;
}

/**
 * ANIMATED PROCESS — MOTION GRAPHICS (FASE 7)
 * Exibição de etapas/passos clínicos estruturados para orientação da família.
 */
export const AnimatedProcess: React.FC<AnimatedProcessProps> = ({
  steps = ["Reconhecer", "Limites Firmes", "Buscar Ajuda"],
  activeStep = 1,
  accentColor = "#E5A93C",
  width = 780,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const containerSpring = spring({
    frame,
    fps,
    config: { damping: 16, stiffness: 100 },
  });

  const opacity = interpolate(containerSpring, [0, 1], [0, 1]);
  const translateY = interpolate(containerSpring, [0, 1], [30, 0]);

  return (
    <div
      style={{
        width,
        display: "flex",
        flexDirection: "column",
        gap: 12,
        opacity,
        transform: `translateY(${translateY}px)`,
        padding: "20px 24px",
        backgroundColor: "rgba(6, 10, 14, 0.75)",
        backdropFilter: "blur(14px)",
        borderRadius: 22,
        border: "1px solid rgba(229, 169, 60, 0.28)",
        boxShadow: "0 10px 36px rgba(0, 0, 0, 0.55)",
      }}
    >
      {steps.map((st, idx) => {
        const stepNum = idx + 1;
        const isActive = stepNum === activeStep;

        const itemSpring = spring({
          frame: frame - (idx * 5 + 3),
          fps,
          config: { damping: 14, stiffness: 110 },
        });

        const itemScale = interpolate(itemSpring, [0, 1], [0.85, 1.0]);
        const itemOpacity = interpolate(itemSpring, [0, 1], [0, 1]);

        return (
          <div
            key={idx}
            style={{
              display: "flex",
              alignItems: "center",
              gap: 16,
              padding: "10px 16px",
              borderRadius: 14,
              backgroundColor: isActive ? "rgba(229, 169, 60, 0.18)" : "rgba(255, 255, 255, 0.05)",
              border: isActive ? `1.5px solid ${accentColor}` : "1px solid rgba(255, 255, 255, 0.1)",
              transform: `scale(${Math.max(0, itemScale)})`,
              opacity: itemOpacity,
            }}
          >
            {/* BADGE NUMÉRICO */}
            <div
              style={{
                width: 34,
                height: 34,
                borderRadius: "50%",
                backgroundColor: isActive ? accentColor : "rgba(255, 255, 255, 0.2)",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                fontFamily: "Inter, Montserrat, sans-serif",
                fontSize: 18,
                fontWeight: 800,
                color: isActive ? "#060A0E" : "#FFFFFF",
                boxShadow: isActive ? `0 0 14px ${accentColor}` : "none",
              }}
            >
              {stepNum}
            </div>

            {/* TEXTO DA ETAPA */}
            <span
              style={{
                fontFamily: "Inter, Montserrat, sans-serif",
                fontSize: 22,
                fontWeight: isActive ? 800 : 600,
                color: isActive ? accentColor : "rgba(255, 255, 255, 0.9)",
                letterSpacing: 0.4,
                textTransform: "uppercase",
              }}
            >
              {st}
            </span>
          </div>
        );
      })}
    </div>
  );
};
