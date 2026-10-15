import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

interface CinematicTitleProps {
  title: string;
  highlightWord?: string;
  subtitle?: string;
  categoryBadge?: string;
}

export const CinematicTitle: React.FC<CinematicTitleProps> = ({
  title,
  highlightWord,
  subtitle,
  categoryBadge,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animação de entrada do Badge de categoria
  const badgeSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Dividir o título em palavras para animação staggered individual
  const words = title.split(" ");

  // Entrada do subtítulo
  const subtitleSpring = spring({
    frame: frame - 18,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });

  // Leve movimento constante de zoom cinematográfico
  const cameraZoom = interpolate(frame, [0, 120], [1, 1.05]);

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
        perspective: 1000,
        transform: `scale(${cameraZoom})`,
      }}
    >
      {/* Badge Superior */}
      {categoryBadge && (
        <div
          style={{
            opacity: badgeSpring,
            transform: `translateY(${interpolate(badgeSpring, [0, 1], [30, 0])}px)`,
            marginBottom: "36px",
            padding: "10px 24px",
            borderRadius: "999px",
            backgroundColor: "rgba(7, 75, 50, 0.4)",
            border: `1px solid ${PALACIO_THEME.colors.gold}`,
            boxShadow: `0 0 25px rgba(212, 175, 55, 0.25)`,
            color: PALACIO_THEME.colors.goldLight,
            fontSize: "22px",
            fontWeight: 700,
            letterSpacing: "4px",
            textTransform: "uppercase",
          }}
        >
          {categoryBadge}
        </div>
      )}

      {/* Título Principal Tipografia Cinética */}
      <h1
        style={{
          fontFamily: PALACIO_THEME.typography.fontFamily,
          fontSize: "64px",
          fontWeight: 900,
          lineHeight: 1.15,
          textAlign: "center",
          margin: 0,
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: "14px 20px",
          maxWidth: "960px",
        }}
      >
        {words.map((word, index) => {
          // Stagger de 3 frames por palavra
          const wordSpring = spring({
            frame: frame - 8 - index * 3,
            fps,
            config: PALACIO_THEME.springs.snappy,
          });

          const isHighlighted =
            highlightWord &&
            word.toLowerCase().replace(/[^a-z0-9áéíóúãõç]/g, "") ===
              highlightWord.toLowerCase().replace(/[^a-z0-9áéíóúãõç]/g, "");

          const translateY = interpolate(wordSpring, [0, 1], [60, 0]);
          const rotateX = interpolate(wordSpring, [0, 1], [40, 0]);
          const opacity = interpolate(wordSpring, [0, 1], [0, 1]);

          return (
            <span
              key={index}
              style={{
                display: "inline-block",
                opacity,
                transform: `translateY(${translateY}px) rotateX(${rotateX}deg)`,
                color: isHighlighted
                  ? PALACIO_THEME.colors.gold
                  : PALACIO_THEME.colors.textWhite,
                textShadow: isHighlighted
                  ? `0 0 35px rgba(212, 175, 55, 0.6), 0 0 70px rgba(212, 175, 55, 0.2)`
                  : "0 10px 30px rgba(0,0,0,0.8)",
              }}
            >
              {word}
            </span>
          );
        })}
      </h1>

      {/* Subtítulo / Linha de Apoio */}
      {subtitle && (
        <div
          style={{
            marginTop: "36px",
            opacity: Math.max(0, subtitleSpring),
            transform: `translateY(${interpolate(subtitleSpring, [0, 1], [40, 0])}px)`,
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "30px",
            fontWeight: 500,
            color: PALACIO_THEME.colors.textMuted,
            textAlign: "center",
            maxWidth: "840px",
            lineHeight: 1.4,
          }}
        >
          {subtitle}
        </div>
      )}
    </AbsoluteFill>
  );
};
