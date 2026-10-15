import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

export interface KineticStepCardProps {
  stepNumber: 1 | 2 | 3;
  stepName: string;
  headline: string;
  explanation: string;
  quote?: string;
}

export const KineticStepCard: React.FC<KineticStepCardProps> = ({
  stepNumber,
  stepName,
  headline,
  explanation,
  quote,
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Animação de entrada com spring
  const enterSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Animação suave de saída nos últimos 12 frames
  const exitFrames = 12;
  const exitProgress = interpolate(
    frame,
    [durationInFrames - exitFrames, durationInFrames],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  const opacity = interpolate(enterSpring, [0, 1], [0, 1]) * (1 - exitProgress);
  const translateY =
    interpolate(enterSpring, [0, 1], [80, 0]) + exitProgress * -40;
  const scale = interpolate(enterSpring, [0, 1], [0.92, 1]) - exitProgress * 0.05;

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "flex-end",
        alignItems: "center",
        paddingBottom: "160px",
        paddingLeft: "48px",
        paddingRight: "48px",
        pointerEvents: "none",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "880px",
          backgroundColor: PALACIO_THEME.colors.cardBg,
          backdropFilter: "blur(24px)",
          WebkitBackdropFilter: "blur(24px)",
          borderRadius: "32px",
          border: `1.5px solid ${PALACIO_THEME.colors.borderGlass}`,
          boxShadow:
            "0 20px 60px rgba(0, 0, 0, 0.7), 0 0 40px rgba(212, 175, 55, 0.15)",
          padding: "44px 48px",
          transform: `translateY(${translateY}px) scale(${scale})`,
          opacity,
          boxSizing: "border-box",
        }}
      >
        {/* Barra Superior com Badge da Etapa e Progresso 1/2/3 */}
        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            alignItems: "center",
            marginBottom: "24px",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "10px",
              padding: "8px 18px",
              borderRadius: "999px",
              backgroundColor: "rgba(212, 175, 55, 0.15)",
              border: `1px solid ${PALACIO_THEME.colors.gold}`,
            }}
          >
            <span
              style={{
                width: "10px",
                height: "10px",
                borderRadius: "50%",
                backgroundColor: PALACIO_THEME.colors.gold,
                boxShadow: `0 0 10px ${PALACIO_THEME.colors.gold}`,
              }}
            />
            <span
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                color: PALACIO_THEME.colors.goldLight,
                fontSize: "18px",
                fontWeight: 700,
                letterSpacing: "3px",
                textTransform: "uppercase",
              }}
            >
              ETAPA 0{stepNumber} • {stepName}
            </span>
          </div>

          {/* Stepper Dots (1, 2, 3) */}
          <div style={{ display: "flex", gap: "8px" }}>
            {[1, 2, 3].map((num) => {
              const isActive = num === stepNumber;
              const isPassed = num < stepNumber;
              return (
                <div
                  key={num}
                  style={{
                    width: isActive ? "32px" : "12px",
                    height: "8px",
                    borderRadius: "4px",
                    backgroundColor: isActive
                      ? PALACIO_THEME.colors.gold
                      : isPassed
                      ? PALACIO_THEME.colors.emeraldLight
                      : "rgba(255, 255, 255, 0.2)",
                    transition: "all 0.3s ease",
                  }}
                />
              );
            })}
          </div>
        </div>

        {/* Headline da Etapa */}
        <h2
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "44px",
            fontWeight: 800,
            color: PALACIO_THEME.colors.textWhite,
            margin: "0 0 16px 0",
            lineHeight: 1.2,
          }}
        >
          {headline}
        </h2>

        {/* Explicação Profunda */}
        <p
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "24px",
            lineHeight: 1.5,
            color: PALACIO_THEME.colors.textMuted,
            margin: "0 0 16px 0",
          }}
        >
          {explanation}
        </p>

        {/* Frase de Destaque / Citação se houver */}
        {quote && (
          <div
            style={{
              borderLeft: `3px solid ${PALACIO_THEME.colors.gold}`,
              paddingLeft: "16px",
              fontFamily: PALACIO_THEME.typography.fontFamily,
              fontStyle: "italic",
              fontSize: "21px",
              color: PALACIO_THEME.colors.goldLight,
              marginTop: "16px",
            }}
          >
            “{quote}”
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
