import React from "react";
import {
  AbsoluteFill,
  Audio,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "./corte2_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "./motion-library/DynamicCaptions";
import { PalacioOutro } from "./motion-library/PalacioOutro";
import { ViralHeader } from "./motion-library/ViralHeader";
import { PALACIO_ACOLHIMENTO_BRAND } from "./motion-library/BrandConfig";
import { PALACIO_THEME } from "./motion-library/PalacioTheme";

const chunks = chunksData as SubtitleChunk[];

export const Corte2CinematicoComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // Curva de Retenção e Câmera Virtual Cinematográfica (Retention & Cinematic Director)
  // 0s - 4.5s (0-135f): 1.05x (abertura e gancho)
  // 4.5s - 9.5s (135-285f): 1.15x (punch-in intimista em "o que eu tinha morreu")
  // 9.5s - 14.0s (285-420f): 1.08x (relato da perda de amigos)
  // 14.0s - 22.0s (420-660f): 1.18x (punch-in máximo em "E eu não quero que seja você...")
  // 22.0s - 25.5s (660-765f): 1.12x (impacto e dor da família)
  // 25.5s - fim: 1.04x (resolução e recuo para o outro)
  let cameraScale = 1.05;
  if (frame >= 135 && frame < 285) {
    cameraScale = interpolate(frame, [135, 160, 260, 285], [1.05, 1.15, 1.15, 1.08], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 285 && frame < 420) {
    cameraScale = 1.08;
  } else if (frame >= 420 && frame < 660) {
    cameraScale = interpolate(frame, [420, 450, 630, 660], [1.08, 1.18, 1.18, 1.12], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 660 && frame < 765) {
    cameraScale = interpolate(frame, [660, 680, 745, 765], [1.12, 1.12, 1.12, 1.04], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 765) {
    cameraScale = 1.04;
  }

  // Badge Emocional Sutil no Momento do Clímax (sem cobrir o rosto)
  // Aparece entre frame 600 (20.0s) e 750 (25.0s) quando Marcelo fala da dor da família
  const highlightStart = 600;
  const highlightEnd = 750;
  const isHighlightActive = frame >= highlightStart && frame <= highlightEnd;
  const highlightOpacity = interpolate(
    frame,
    [highlightStart, highlightStart + 15, highlightEnd - 15, highlightEnd],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Outro institucional nos últimos 68 frames (~2.26s)
  const outroStartFrame = durationInFrames - 68;
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 18],
    [0, 1],
    {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* 1. Rosto e Emoção do Orador Preservados com Movimento de Câmera Orgânico */}
      <div
        style={{
          width: "100%",
          height: "100%",
          transform: `scale(${cameraScale})`,
          transformOrigin: "50% 36%",
          transition: "transform 0.12s ease-out",
        }}
      >
        <OffthreadVideo
          src={staticFile("corte2_video.mp4")}
          volume={0}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />
      </div>

      {/* 2. Trilha Sonora Masterizada (Pedalboard + SFX Narrativos + EBU R128) */}
      <Audio src={staticFile("corte2_audio.wav")} />

      {/* 3. Vinheta Cinematográfica de Atmosfera e Foco */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 38%, transparent 42%, rgba(6, 10, 8, 0.42) 85%, rgba(6, 10, 8, 0.85) 100%)",
          pointerEvents: "none",
          zIndex: 40,
        }}
      />

      {/* 4. Badge Contextual Sutil de Impacto Familiar na Safe Zone Superior (sem cobrir o rosto) */}
      {isHighlightActive && (
        <div
          style={{
            position: "absolute",
            top: "115px",
            left: "50%",
            transform: "translateX(-50%)",
            opacity: highlightOpacity,
            zIndex: 45,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              backgroundColor: "rgba(6, 10, 8, 0.82)",
              backdropFilter: "blur(14px)",
              WebkitBackdropFilter: "blur(14px)",
              padding: "8px 22px",
              borderRadius: "999px",
              border: `1.5px solid ${PALACIO_THEME.colors.gold}`,
              boxShadow: "0 8px 30px rgba(0,0,0,0.8), 0 0 15px rgba(212, 175, 55, 0.25)",
            }}
          >
            <span
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "14px",
                fontWeight: 800,
                color: PALACIO_THEME.colors.goldLight,
                letterSpacing: "2.5px",
                textTransform: "uppercase",
              }}
            >
              A DOR DA FAMÍLIA NA DEPENDÊNCIA
            </span>
          </div>
        </div>
      )}

      {/* 5. Header Viral com Barra de Progresso e Marca PALÁCIO ACOLHIMENTO */}
      <ViralHeader
        brand={PALACIO_ACOLHIMENTO_BRAND}
        title="NÃO QUERO PERDER VOCÊ"
        category="ALERTA SOBRE A VIDA • PALÁCIO ACOLHIMENTO"
        hookSubtitle="A dor de quem já perdeu amigos pra droga."
      />

      {/* 6. Legendas Dinâmicas Karaoke na ZONA SEGURA (bottom: 540px = Y central ~1300px) */}
      {frame < outroStartFrame && (
        <DynamicCaptions chunks={chunks} bottomPx={540} maxBoxWidth={860} />
      )}

      {/* 7. Encerramento Institucional Oficial PALÁCIO ACOLHIMENTO */}
      {frame >= outroStartFrame && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: `rgba(6, 10, 8, ${outroOpacity * 0.95})`,
            backdropFilter: `blur(${outroOpacity * 14}px)`,
            WebkitBackdropFilter: `blur(${outroOpacity * 14}px)`,
            opacity: outroOpacity,
            zIndex: 60,
          }}
        >
          <PalacioOutro
            brand={PALACIO_ACOLHIMENTO_BRAND}
            sloganHighlightWord="viver"
          />
        </div>
      )}
    </AbsoluteFill>
  );
};
