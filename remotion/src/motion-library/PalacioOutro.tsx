import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import { PALACIO_THEME } from "./PalacioTheme";

export const PalacioOutro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Animação do Escudo / Brasão
  const emblemSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });

  // Animação da frase de impacto
  const quoteSpring = spring({
    frame: frame - 15,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Animação da marca Palácio Acolhimento
  const brandSpring = spring({
    frame: frame - 30,
    fps,
    config: PALACIO_THEME.springs.snappy,
  });

  // Animação da CTA
  const ctaSpring = spring({
    frame: frame - 45,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });

  const emblemScale = interpolate(emblemSpring, [0, 1], [0.6, 1.0]);
  const emblemRotate = interpolate(emblemSpring, [0, 1], [-25, 0]);

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
      {/* Brasão / Símbolo Dourado Central Palácio.pro */}
      <div
        style={{
          transform: `scale(${emblemScale}) rotate(${emblemRotate}deg)`,
          opacity: emblemSpring,
          width: "120px",
          height: "120px",
          borderRadius: "28px",
          background: `linear-gradient(135deg, ${PALACIO_THEME.colors.gold} 0%, #8A6D1C 100%)`,
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          boxShadow: `0 0 50px rgba(212, 175, 55, 0.4), 0 15px 30px rgba(0,0,0,0.7)`,
          marginBottom: "40px",
          position: "relative",
        }}
      >
        {/* Glow pulsing effect */}
        <div
          style={{
            position: "absolute",
            inset: -6,
            borderRadius: "32px",
            border: `2px solid rgba(212, 175, 55, 0.5)`,
            animation: "none",
          }}
        />
        {/* Monograma P estilizado */}
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "64px",
            fontWeight: 900,
            color: PALACIO_THEME.colors.darkBg,
            textShadow: "0 2px 4px rgba(255,255,255,0.3)",
          }}
        >
          P
        </span>
      </div>

      {/* Frase Central Conclusiva */}
      <div
        style={{
          opacity: Math.max(0, quoteSpring),
          transform: `translateY(${interpolate(quoteSpring, [0, 1], [40, 0])}px)`,
          maxWidth: "880px",
          marginBottom: "36px",
        }}
      >
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "24px",
            fontWeight: 600,
            color: PALACIO_THEME.colors.goldLight,
            letterSpacing: "4px",
            textTransform: "uppercase",
            display: "block",
            marginBottom: "16px",
          }}
        >
          Filosofia da Recuperação
        </span>
        <h2
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "52px",
            fontWeight: 800,
            lineHeight: 1.25,
            color: PALACIO_THEME.colors.textWhite,
            margin: 0,
            textShadow: "0 10px 40px rgba(0,0,0,0.9)",
          }}
        >
          “A recuperação continua na forma de{" "}
          <span style={{ color: PALACIO_THEME.colors.gold }}>viver</span>.”
        </h2>
      </div>

      {/* Divisor dourado sutil */}
      <div
        style={{
          width: interpolate(brandSpring, [0, 1], [0, 180]),
          height: "2px",
          background: `linear-gradient(90deg, transparent, ${PALACIO_THEME.colors.gold}, transparent)`,
          marginBottom: "36px",
        }}
      />

      {/* Assinatura de Marca Palácio Acolhimento */}
      <div
        style={{
          opacity: Math.max(0, brandSpring),
          transform: `translateY(${interpolate(brandSpring, [0, 1], [30, 0])}px)`,
          marginBottom: "44px",
        }}
      >
        <h3
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "36px",
            fontWeight: 900,
            letterSpacing: "6px",
            color: PALACIO_THEME.colors.textWhite,
            margin: "0 0 10px 0",
            textTransform: "uppercase",
          }}
        >
          PALÁCIO ACOLHIMENTO
        </h3>
        <p
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "22px",
            color: PALACIO_THEME.colors.textMuted,
            margin: 0,
            letterSpacing: "1px",
          }}
        >
          Acolhimento Familiar & Tratamento Humanizado
        </p>
      </div>

      {/* Chamada para Ação / Redes Sociais */}
      <div
        style={{
          opacity: Math.max(0, ctaSpring),
          transform: `translateY(${interpolate(ctaSpring, [0, 1], [30, 0])}px)`,
          padding: "16px 36px",
          borderRadius: "999px",
          backgroundColor: "rgba(7, 75, 50, 0.45)",
          border: `1.5px solid ${PALACIO_THEME.colors.gold}`,
          boxShadow: "0 10px 30px rgba(0, 0, 0, 0.6)",
        }}
      >
        <span
          style={{
            fontFamily: PALACIO_THEME.typography.fontFamily,
            fontSize: "22px",
            fontWeight: 700,
            color: PALACIO_THEME.colors.goldLight,
            letterSpacing: "1.5px",
          }}
        >
          palacioacolhimento.com.br • @palacio.pro
        </span>
      </div>
    </AbsoluteFill>
  );
};
