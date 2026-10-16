import React from "react";
import { interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

export interface AnimatedConnectionProps {
  nodes?: string[];
  mode?: "separate" | "connect";
  accentColor?: string;
  width?: number;
}

/**
 * ANIMATED CONNECTION — MOTION GRAPHICS (FASE 7)
 * Diagrama de vínculos afetivos que se afastam ou se aproximam com a narrativa.
 */
export const AnimatedConnection: React.FC<AnimatedConnectionProps> = ({
  nodes = ["Você", "Família", "Amigos"],
  mode = "separate",
  accentColor = "#E5A93C",
  width = 750,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  const animSpring = spring({
    frame,
    fps,
    config: { damping: 16, stiffness: 85 },
  });

  // Separação ou aproximação progressiva
  const distanceMultiplier = mode === "separate"
    ? interpolate(animSpring, [0, 1], [1.0, 1.45])
    : interpolate(animSpring, [0, 1], [1.45, 1.0]);

  const opacity = interpolate(animSpring, [0, 1], [0, 1]);

  return (
    <div
      style={{
        width,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        opacity,
        padding: "24px 30px",
        backgroundColor: "rgba(6, 10, 14, 0.76)",
        backdropFilter: "blur(14px)",
        borderRadius: 22,
        border: "1px solid rgba(229, 169, 60, 0.28)",
        boxShadow: "0 10px 36px rgba(0, 0, 0, 0.55)",
      }}
    >
      <div
        style={{
          width: "100%",
          display: "flex",
          justifyContent: "space-around",
          alignItems: "center",
          position: "relative",
          margin: "12px 0",
        }}
      >
        {nodes.map((nodeName, idx) => {
          const isCenter = idx === 1;
          const nodeColor = isCenter ? accentColor : "#FFFFFF";

          return (
            <div
              key={idx}
              style={{
                display: "flex",
                flexDirection: "column",
                alignItems: "center",
                gap: 10,
                transform: `scale(${isCenter ? 1.15 : 1.0})`,
                transition: "transform 0.2s ease-out",
              }}
            >
              {/* ÍCONE NÓ */}
              <div
                style={{
                  width: 52,
                  height: 52,
                  borderRadius: "50%",
                  backgroundColor: isCenter ? "rgba(229, 169, 60, 0.2)" : "rgba(255, 255, 255, 0.08)",
                  border: `2px solid ${nodeColor}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  boxShadow: isCenter ? `0 0 18px ${accentColor}` : "none",
                }}
              >
                <div
                  style={{
                    width: 16,
                    height: 16,
                    borderRadius: "50%",
                    backgroundColor: nodeColor,
                  }}
                />
              </div>

              {/* RÓTULO */}
              <span
                style={{
                  fontFamily: "Inter, Montserrat, sans-serif",
                  fontSize: 18,
                  fontWeight: 700,
                  color: nodeColor,
                  letterSpacing: 0.5,
                  textTransform: "uppercase",
                }}
              >
                {nodeName}
              </span>
            </div>
          );
        })}
      </div>

      {/* LEGENDA CONCEITUAL */}
      <span
        style={{
          marginTop: 8,
          fontFamily: "Inter, Montserrat, sans-serif",
          fontSize: 14,
          fontWeight: 600,
          color: "rgba(255, 255, 255, 0.65)",
          letterSpacing: 1.2,
          textTransform: "uppercase",
        }}
      >
        {mode === "separate" ? "• AFASTAMENTO PROGRESSIVO •" : "• RECONEXÃO FAMILIAR •"}
      </span>
    </div>
  );
};
