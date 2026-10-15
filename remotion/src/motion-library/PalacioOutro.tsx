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

export const PalacioOutro: React.FC<{
  brand?: BrandConfig;
  sloganHighlightWord?: string;
}> = ({ brand = PALACIO_ACOLHIMENTO_BRAND, sloganHighlightWord = "viver" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Validação de marca no encerramento
  const integrity = validateBrandIntegrity(brand, brand);
  if (!integrity.valid) {
    throw new Error(`[PALÁCIO OUTRO ERROR] ${integrity.violations.join(" | ")}`);
  }

  // Animação do Escudo / Brasão
  const emblemSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });

  // Animação da frase de impacto
  const quoteSpring = spring({
    frame: frame - 12,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Animação da marca oficial
  const brandSpring = spring({
    frame: frame - 25,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Animação da CTA
  const ctaSpring = spring({
    frame: frame - 38,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });

  const emblemScale = interpolate(emblemSpring, [0, 1], [0.6, 1.0]);
  const emblemRotate = interpolate(emblemSpring, [0, 1], [-20, 0]);

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        flexDirection: "column",
        justifyContent: "center",
        alignItems: "center",
        padding: "0 60px",
        textAlign: "center",
        pointerEvents: "none",
      }}
    >
      {/* Brasão Dourado Central Oficial */}
      <div
        style={{
          transform: `scale(${emblemScale}) rotate(${emblemRotate}deg)`,
          opacity: emblemSpring,
          width: "110px",
          height: "110px",
          borderRadius: "26px",
          background: `linear-gradient(135deg, ${brand.colors.gold} 0%, #8A6D1C 100%)`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          boxShadow: `0 0 50px rgba(212, 175, 55, 0.4), 0 15px 30px rgba(0,0,0,0.7)`,
          marginBottom: "36px",
          position: "relative",
        }}
      >
        <div
          style={{
            position: "absolute",
            inset: -5,
            borderRadius: "30px",
            border: `2px solid rgba(212, 175, 55, 0.5)`,
          }}
        />
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "60px",
            fontWeight: 900,
            color: brand.colors.darkBg,
            textShadow: "0 2px 4px rgba(255,255,255,0.3)",
          }}
        >
          {brand.monogram}
        </span>
      </div>

      {/* Frase Conclusiva Oficial */}
      <div
        style={{
          opacity: Math.max(0, quoteSpring),
          transform: `translateY(${interpolate(quoteSpring, [0, 1], [30, 0])}px)`,
          maxWidth: "860px",
          marginBottom: "32px",
        }}
      >
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "22px",
            fontWeight: 600,
            color: brand.colors.goldLight,
            letterSpacing: "4px",
            textTransform: "uppercase",
            display: "block",
            marginBottom: "14px",
          }}
        >
          Filosofia da Recuperação
        </span>
        <h2
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "48px",
            fontWeight: 800,
            lineHeight: 1.25,
            color: brand.colors.textWhite,
            margin: 0,
            textShadow: "0 10px 40px rgba(0,0,0,0.9)",
          }}
        >
          “A recuperação continua na forma de{" "}
          <span style={{ color: brand.colors.gold }}>{sloganHighlightWord}</span>.”
        </h2>
      </div>

      {/* Divisor dourado sutil */}
      <div
        style={{
          width: interpolate(brandSpring, [0, 1], [0, 160]),
          height: "2px",
          background: `linear-gradient(90deg, transparent, ${brand.colors.gold}, transparent)`,
          marginBottom: "32px",
        }}
      />

      {/* Assinatura de Marca Oficial */}
      <div
        style={{
          opacity: Math.max(0, brandSpring),
          transform: `translateY(${interpolate(brandSpring, [0, 1], [25, 0])}px)`,
          marginBottom: "38px",
        }}
      >
        <h3
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "34px",
            fontWeight: 900,
            letterSpacing: "5px",
            color: brand.colors.textWhite,
            margin: "0 0 8px 0",
            textTransform: "uppercase",
          }}
        >
          {brand.brandDisplay}
        </h3>
        <p
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "20px",
            color: PALACIO_THEME.colors.textMuted,
            margin: 0,
            letterSpacing: "1px",
          }}
        >
          {brand.subtext}
        </p>
      </div>

      {/* Chamada para Ação / Redes Sociais com Handle Oficial */}
      <div
        style={{
          opacity: Math.max(0, ctaSpring),
          transform: `translateY(${interpolate(ctaSpring, [0, 1], [25, 0])}px)`,
          padding: "14px 34px",
          borderRadius: "999px",
          backgroundColor: "rgba(7, 75, 50, 0.55)",
          border: `1.5px solid ${brand.colors.gold}`,
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.6)",
        }}
      >
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "20px",
            fontWeight: 700,
            color: brand.colors.goldLight,
            letterSpacing: "1.5px",
          }}
        >
          {brand.website} • {brand.handle}
        </span>
      </div>
    </AbsoluteFill>
  );
};
