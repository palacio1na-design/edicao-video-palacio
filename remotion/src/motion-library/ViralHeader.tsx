import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";
import {
  BrandConfig,
  PALACIO_ACOLHIMENTO_BRAND,
  validateBrandIntegrity,
} from "./BrandConfig";

export const ViralHeader: React.FC<{
  title: string;
  category: string;
  hookSubtitle?: string;
  brand?: BrandConfig;
}> = ({ title, category, hookSubtitle, brand = PALACIO_ACOLHIMENTO_BRAND }) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Validação obrigatória de integridade da marca
  const integrity = validateBrandIntegrity(
    { title, category, hookSubtitle, handle: brand.handle, website: brand.website },
    brand,
  );
  if (!integrity.valid) {
    throw new Error(`[PALÁCIO BRAND ERROR] ${integrity.violations.join(" | ")}`);
  }

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

  // Saída suave do gancho aos 105 frames (3.5 segundos)
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
          height: "6px",
          backgroundColor: "rgba(0, 0, 0, 0.4)",
          zIndex: 50,
        }}
      >
        <div
          style={{
            height: "100%",
            width: `${progressPercent}%`,
            background: `linear-gradient(90deg, ${brand.colors.primary}, ${brand.colors.gold})`,
            boxShadow: `0 0 10px ${brand.colors.gold}`,
          }}
        />
      </div>

      {/* 2. Marca Superior Permanente (Safe Zone de Stories/Reels - Top: 48px) */}
      <div
        style={{
          position: "absolute",
          top: "48px",
          left: "48px",
          right: "48px",
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          zIndex: 40,
        }}
      >
        {/* Logo / Marca Institucional Oficial */}
        <div
          style={{
            display: "inline-flex",
            alignItems: "center",
            gap: "10px",
            backgroundColor: "rgba(6, 10, 8, 0.70)",
            backdropFilter: "blur(14px)",
            WebkitBackdropFilter: "blur(14px)",
            padding: "8px 18px",
            borderRadius: "999px",
            border: `1px solid ${PALACIO_THEME.colors.borderGlass}`,
            boxShadow: "0 4px 15px rgba(0,0,0,0.5)",
          }}
        >
          <div
            style={{
              width: "22px",
              height: "22px",
              borderRadius: "6px",
              backgroundColor: brand.colors.gold,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              fontSize: "13px",
              fontWeight: 900,
              color: brand.colors.darkBg,
            }}
          >
            {brand.monogram}
          </div>
          <span
            style={{
              fontFamily: PALACIO_THEME.typography.fontFamily,
              fontSize: "17px",
              fontWeight: 800,
              letterSpacing: "2px",
              color: brand.colors.textWhite,
              textTransform: "uppercase",
            }}
          >
            {brand.brandDisplay}
          </span>
        </div>

        {/* Tag Oficial da Marca */}
        <div
          style={{
            backgroundColor: "rgba(7, 75, 50, 0.75)",
            backdropFilter: "blur(14px)",
            WebkitBackdropFilter: "blur(14px)",
            padding: "8px 18px",
            borderRadius: "999px",
            border: `1px solid ${brand.colors.gold}`,
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "15px",
            fontWeight: 700,
            color: brand.colors.goldLight,
            letterSpacing: "1px",
            boxShadow: "0 4px 15px rgba(0,0,0,0.5)",
          }}
        >
          {brand.handle}
        </div>
      </div>

      {/* 3. Gancho / Título Inicial Compacto (Frames 0 a 115) 
          Posicionado em top: 110px para NÃO invadir o rosto nem a testa do orador */}
      {frame <= 115 && (
        <div
          style={{
            position: "absolute",
            top: "116px",
            left: "48px",
            right: "48px",
            display: "flex",
            justifyContent: "center",
            opacity: hookSpring * hookFadeOut,
            transform: `translateY(${interpolate(hookSpring, [0, 1], [-20, 0])}px)`,
            zIndex: 45,
          }}
        >
          <div
            style={{
              backgroundColor: "rgba(6, 10, 8, 0.85)",
              backdropFilter: "blur(20px)",
              WebkitBackdropFilter: "blur(20px)",
              border: `1.5px solid ${brand.colors.gold}`,
              borderRadius: "24px",
              padding: "18px 32px",
              boxShadow:
                "0 20px 50px rgba(0, 0, 0, 0.9), 0 0 25px rgba(212, 175, 55, 0.2)",
              display: "flex",
              flexDirection: "column",
              alignItems: "center",
              textAlign: "center",
              maxWidth: "840px",
              width: "100%",
            }}
          >
            {/* Badge de categoria do Gancho */}
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                backgroundColor: "rgba(212, 175, 55, 0.16)",
                border: `1px solid ${brand.colors.gold}`,
                padding: "4px 16px",
                borderRadius: "999px",
                marginBottom: "10px",
              }}
            >
              <span
                style={{
                  fontFamily: PALACIO_THEME.typography.fontFamily,
                  fontSize: "14px",
                  fontWeight: 800,
                  color: brand.colors.goldLight,
                  letterSpacing: "2.5px",
                  textTransform: "uppercase",
                }}
              >
                {category}
              </span>
            </div>

            {/* Título Principal de Gancho Compacto e Elegante */}
            <h1
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "38px",
                fontWeight: 900,
                lineHeight: 1.15,
                color: brand.colors.textWhite,
                margin: 0,
                textTransform: "uppercase",
                textShadow: "0 2px 8px rgba(0,0,0,0.85)",
              }}
            >
              {title}
            </h1>

            {/* Subtítulo do Gancho */}
            {hookSubtitle && (
              <p
                style={{
                  fontFamily: PALACIO_THEME.typography.fontFamily,
                  fontSize: "18px",
                  fontWeight: 500,
                  color: brand.colors.goldLight,
                  margin: "8px 0 0 0",
                  lineHeight: 1.25,
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
