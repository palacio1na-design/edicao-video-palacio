import React from "react";
import { AbsoluteFill, interpolate, useCurrentFrame } from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

export const ParallaxBackground: React.FC<{
  intensity?: number;
}> = ({ intensity = 1 }) => {
  const frame = useCurrentFrame();

  // Movimento orgânico lento dos orbes de luz
  const orb1Y = interpolate(frame, [0, 450], [0, -80]) * intensity;
  const orb2X = interpolate(frame, [0, 450], [0, 60]) * intensity;
  const orbScale = interpolate(Math.sin(frame * 0.03), [-1, 1], [0.95, 1.15]);

  return (
    <AbsoluteFill
      style={{
        backgroundColor: PALACIO_THEME.colors.darkBg,
        overflow: "hidden",
      }}
    >
      {/* Gradiente radial esmeralda profundo no centro */}
      <div
        style={{
          position: "absolute",
          top: "30%",
          left: "50%",
          width: "1200px",
          height: "1200px",
          transform: `translate(-50%, -50%) translateY(${orb1Y}px) scale(${orbScale})`,
          background: `radial-gradient(circle, rgba(7, 75, 50, 0.45) 0%, rgba(6, 10, 8, 0) 70%)`,
          filter: "blur(60px)",
          pointerEvents: "none",
        }}
      />

      {/* Brilho dourado sutil no topo/canto */}
      <div
        style={{
          position: "absolute",
          top: "-10%",
          right: "-10%",
          width: "800px",
          height: "800px",
          transform: `translateX(${orb2X}px)`,
          background: `radial-gradient(circle, rgba(212, 175, 55, 0.15) 0%, rgba(6, 10, 8, 0) 65%)`,
          filter: "blur(70px)",
          pointerEvents: "none",
        }}
      />

      {/* Grid sutil cinematográfico */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          backgroundImage: `linear-gradient(rgba(212, 175, 55, 0.03) 1px, transparent 1px), linear-gradient(90deg, rgba(212, 175, 55, 0.03) 1px, transparent 1px)`,
          backgroundSize: "60px 60px",
          maskImage: "radial-gradient(circle, black 40%, transparent 80%)",
          WebkitMaskImage: "radial-gradient(circle, black 40%, transparent 80%)",
        }}
      />
    </AbsoluteFill>
  );
};
