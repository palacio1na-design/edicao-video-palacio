import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

export const ViralHeader: React.FC<{
  title: string;
  category: string;
  hookSubtitle?: string;
}> = ({ title, category, hookSubtitle }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Barra de progresso linear no topo
  const progressPercent = interpolate(
    frame,
    [0, durationInFrames],
    [0, 100],
    { extrapolateRight: "clamp" },
  );

  // Animação de entrada do Hook nos primeiros frames
  const hookSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Saída suave do hook aos 105 frames (3.5 segundos)
  const hookFadeOut = interpolate(frame, [95, 115], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      {/* 1. Barra de Progresso no Topo */}
      <div
        style={{
          position: "absolute",
          top: 0,
          left: 0,
          width: "100%",
          height: "8px",
          backgroundColor: "rgba(0, 0, 0, 0.4)",
          zIndex: 50,
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPercent}%`,
            background: `linear-gradient(90deg, ${PALACIO_THEME.colors.deepGreen}, ${PALACIO_THEME.colors.gold})`,
            boxShadow: `0 0 12px ${PALACIO_THEME.colors.gold}`,
          }}
        />
      </div>

      {/* 2. Marca Superior Permanente (Safe Zone de Stories/Reels) */}
      <div
        style={{
          position: "absolute",
          top: "40px",
          left: "48px",
          right: "48px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 40,
        }}
      >
        {/* Logo / Marca Palácio Acolhimento */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "12px",
            backgroundColor: "rgba(6, 10, 8, 0.65)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
            padding: "8px 18px",
            borderRadius: "999px",
            border: `1px solid ${PALACIO_THEME.colors.borderGlass}`,
          }}
        >
          <div
            style={{
              width: "22px",
              height: "22px",
              borderRadius: "6px",
              backgroundColor: PALACIO_THEME.colors.gold,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "13px",
              fontWeight: 900,
              color: PALACIO_THEME.colors.darkBg,
            }}
          >
            P
          </div>
          <span
            style={{
              fontFamily: PALACIO_THEME.typography.fontFamily,
              fontSize: "18px",
              fontWeight: 800,
              letterSpacing: "2px",
              color: PALACIO_THEME.colors.textWhite,
              textTransform: "uppercase",
            }}
          >
            PALÁCIO ACOLHIMENTO
          </span>
        </div>

        {/* Tag @palacio.pro */}
        <div
          style={{
            backgroundColor: "rgba(7, 75, 50, 0.6)",
            backdropFilter: "blur(12px)",
            WebkitBackdropFilter: "blur(12px)",
            padding: "8px 18px",
            borderRadius: "999px",
            border: `1px solid ${PALACIO_THEME.colors.gold}`,
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "16px",
            fontWeight: 700,
            color: PALACIO_THEME.colors.goldLight,
            letterSpacing: "1px",
          }}
        >
          @palacio.pro
        </div>
      </div>

      {/* 3. Gancho / Título Inicial (Frames 0 a 115) */}
      {frame <= 115 && (
        <div
          style={{
            position: "absolute",
            top: "135px",
            left: "40px",
            right: "40px",
            display: "flex",
            justifyContent: "center",
            opacity: hookSpring * hookFadeOut,
            transform: `translateY(${interpolate(hookSpring, [0, 1], [-30, 0])}px)`,
            zIndex: 45,
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(6, 10, 8, 0.82)",
              backdropFilter: "blur(24px)",
              WebkitBackdropFilter: "blur(24px)",
              border: `1.5px solid ${PALACIO_THEME.colors.gold}`,
              borderRadius: "32px",
              padding: "28px 40px",
              boxShadow:
                "0 25px 60px rgba(0, 0, 0, 0.9), 0 0 35px rgba(212, 175, 55, 0.25)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              textAlign: "center",
              maxWidth: "860px",
              width: "100%",
            }}
          >
            {/* Badge de categoria do Gancho */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                backgroundColor: "rgba(212, 175, 55, 0.18)",
                border: `1px solid ${PALACIO_THEME.colors.gold}`,
                padding: "6px 20px",
                borderRadius: "999px",
                marginBottom: "14px",
              }}
            >
              <span
                style={{
                  fontFamily: PALACIO_THEME.typography.fontFamily,
                  fontSize: "16px",
                  fontWeight: 800,
                  color: PALACIO_THEME.colors.goldLight,
                  letterSpacing: "3px",
                  textTransform: "uppercase",
                }}
              >
                {category}
              </span>
            </div>

            {/* Título Principal de Gancho */}
            <h1
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "48px",
                fontWeight: 900,
                lineHeight: 1.15,
                color: PALACIO_THEME.colors.textWhite,
                margin: 0,
                textTransform: "uppercase",
                textShadow: "0 2px 10px rgba(0,0,0,0.8)",
              }}
            >
              {title}
            </h1>

            {/* Subtítulo do Gancho */}
            {hookSubtitle && (
              <p
                style={{
                  fontFamily: PALACIO_THEME.typography.fontFamily,
                  fontSize: "22px",
                  fontWeight: 500,
                  color: PALACIO_THEME.colors.goldLight,
                  margin: "12px 0 0 0",
                  lineHeight: 1.3,
                }}
              >
                “{hookSubtitle}”
              </p>
            )}
          </div>
        </div>
      )}
    </AbsoluteFill>
  );
};
