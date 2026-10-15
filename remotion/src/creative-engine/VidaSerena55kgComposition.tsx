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
import chunksData from "../vida_serena_55kg_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "../motion-library/DynamicCaptions";
import { PalacioOutro } from "../motion-library/PalacioOutro";
import { ViralHeader } from "../motion-library/ViralHeader";
import { PALACIO_ACOLHIMENTO_BRAND } from "../motion-library/BrandConfig";
import { PALACIO_THEME } from "../motion-library/PalacioTheme";

const chunks = chunksData as SubtitleChunk[];

export const VidaSerena55kgComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // ==============================================================
  // 1. TIMING DE MONTAGEM E B-ROLLS (AUTÊNTICO & CONTEXTUAL)
  // ==============================================================
  // B-Roll 1 (Solidão / Corpo em Colapso na Cama): 23.0s a 27.5s (f690 a f825)
  // B-Roll 2 (Dor Familiar / Mãe Chorando): 94.5s a 98.6s (f2835 a f2958)
  const isBroll1Active = frame >= 690 && frame < 825;
  const isBroll2Active = frame >= 2835 && frame < 2958;
  const isArollActive = !isBroll1Active && !isBroll2Active;

  // Drift sutil nos B-Rolls para dinamismo cinematográfico
  const broll1Scale = interpolate(frame, [690, 825], [1.02, 1.08], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const broll2Scale = interpolate(frame, [2835, 2958], [1.02, 1.07], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // ==============================================================
  // 2. CÂMERA VIRTUAL DINÂMICA (A-ROLL ANCORADO NOS OLHOS 50% 34%)
  // ==============================================================
  let arollScale = 1.06;
  if (frame >= 0 && frame < 175) {
    // Abertura / Gancho 55kg
    arollScale = interpolate(frame, [0, 175], [1.05, 1.10], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 175 && frame < 265) {
    // Punch-in em "55 quilos, eu tenho 1,86m"
    arollScale = 1.14;
  } else if (frame >= 265 && frame < 525) {
    // Comparação com peso atual
    arollScale = 1.08;
  } else if (frame >= 525 && frame < 690) {
    // "só o osso mesmo"
    arollScale = 1.15;
  } else if (frame >= 825 && frame < 1050) {
    // Retorno pós B-roll 1
    arollScale = 1.08;
  } else if (frame >= 1050 && frame < 1620) {
    // Tensão da promessa e remédios
    arollScale = interpolate(frame, [1050, 1620], [1.10, 1.16], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 1620 && frame < 1710) {
    // Punch-in seco na fuga: "tem dinheiro na caixinha, vou embora"
    arollScale = 1.22;
  } else if (frame >= 1710 && frame < 1860) {
    // Respiração antes da revelação
    arollScale = 1.12;
  } else if (frame >= 1860 && frame < 2130) {
    // PUNCH-IN MÁXIMO NO CLÍMAX: "Dizer NÃO para mim mesmo... Chega!"
    arollScale = interpolate(frame, [1860, 1920, 2070, 2130], [1.14, 1.25, 1.25, 1.14], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 2130 && frame < 2640) {
    // Reflexão e rendição ao tratamento
    arollScale = 1.08;
  } else if (frame >= 2640 && frame < 2835) {
    // Honestidade visceral: "cansado de sofrer, cara"
    arollScale = 1.18;
  } else if (frame >= 2958) {
    arollScale = 1.04;
  }

  // ==============================================================
  // 3. BADGES CONTEXTUAIS NA ZONA SEGURA SUPERIOR
  // ==============================================================
  let currentBadgeText = "";
  if (frame >= 125 && frame < 520) {
    currentBadgeText = "55 QUILOS: O FUNDO DO POÇO";
  } else if (frame >= 690 && frame < 825) {
    currentBadgeText = "O CORPO EM COLAPSO";
  } else if (frame >= 1150 && frame < 1620) {
    currentBadgeText = "A ILUSÃO DA FUGA";
  } else if (frame >= 1860 && frame < 2130) {
    currentBadgeText = "O PODER DE DIZER NÃO";
  } else if (frame >= 2640 && frame < 2955) {
    currentBadgeText = "A DOR DE UMA MÃE";
  }

  // Fade do Badge
  const badgeOpacity = interpolate(
    frame % 200,
    [0, 12, 188, 200],
    [0.9, 1, 1, 0.9],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // ==============================================================
  // 4. OUTRO INSTITUCIONAL PALÁCIO ACOLHIMENTO (ÚLTIMOS 80 FRAMES)
  // ==============================================================
  const outroStartFrame = durationInFrames - 80; // frame 2965 (98.8s)
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 20],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* 1. TRILHA MULTITRACK MASTERIZADA (Voz Pedalboard + SFX + EBU R128) */}
      <Audio src={staticFile("vida_serena_master_soundtrack.wav")} />

      {/* 2. PISTA A-ROLL (MARCELO PALÁCIO - PALESTRA VIDA SERENA) */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          opacity: isArollActive ? 1 : 0,
          zIndex: 10,
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: `scale(${arollScale})`,
            transformOrigin: "50% 34%",
            transition: "transform 0.12s ease-out",
          }}
        >
          <OffthreadVideo
            src={staticFile("vida_serena_55kg_video.mp4")}
            volume={0}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "contrast(1.05) brightness(1.02) saturate(1.04)",
            }}
          />
        </div>
      </div>

      {/* 3. PISTA B-ROLL 1: SOLIDÃO / SEM CONSEGUIR ANDAR */}
      {isBroll1Active && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 20,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: "100%",
              height: "100%",
              transform: `scale(${broll1Scale})`,
              transformOrigin: "center center",
            }}
          >
            <OffthreadVideo
              src={staticFile("broll/homem_solidao_quarto.mp4")}
              volume={0}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "contrast(1.08) brightness(0.92) saturate(0.9)",
              }}
            />
          </div>
        </div>
      )}

      {/* 4. PISTA B-ROLL 2: DOR DA MÃE / IMPACTO FAMILIAR */}
      {isBroll2Active && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            zIndex: 20,
            overflow: "hidden",
          }}
        >
          <div
            style={{
              width: "100%",
              height: "100%",
              transform: `scale(${broll2Scale})`,
              transformOrigin: "center center",
            }}
          >
            <OffthreadVideo
              src={staticFile("broll_mae_droga.mp4")}
              volume={0}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "contrast(1.10) brightness(0.90) saturate(0.95)",
              }}
            />
          </div>
        </div>
      )}

      {/* 5. VINHETA CINEMATOGRÁFICA DE PROFUNDIDADE E FOCO */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 36%, transparent 40%, rgba(6, 10, 8, 0.45) 80%, rgba(6, 10, 8, 0.88) 100%)",
          pointerEvents: "none",
          zIndex: 35,
        }}
      />

      {/* 6. BADGE CONTEXTUAL NA SAFE ZONE SUPERIOR */}
      {currentBadgeText && frame < outroStartFrame && (
        <div
          style={{
            position: "absolute",
            top: "120px",
            left: "50%",
            transform: "translateX(-50%)",
            opacity: badgeOpacity,
            zIndex: 45,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "8px",
              backgroundColor: "rgba(6, 10, 8, 0.85)",
              backdropFilter: "blur(14px)",
              WebkitBackdropFilter: "blur(14px)",
              padding: "8px 24px",
              borderRadius: "999px",
              border: `1.5px solid ${PALACIO_THEME.colors.gold}`,
              boxShadow: "0 8px 30px rgba(0,0,0,0.85), 0 0 16px rgba(212, 175, 55, 0.25)",
            }}
          >
            <div
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                backgroundColor: PALACIO_THEME.colors.gold,
                boxShadow: "0 0 10px #D4AF37",
              }}
            />
            <span
              style={{
                fontFamily: PALACIO_THEME.typography.fontFamily,
                fontSize: "15px",
                fontWeight: 800,
                color: PALACIO_THEME.colors.goldLight,
                letterSpacing: "2.2px",
                textTransform: "uppercase",
              }}
            >
              {currentBadgeText}
            </span>
          </div>
        </div>
      )}

      {/* 7. HEADER VIRAL COM BARRA DE PROGRESSO & PALÁCIO ACOLHIMENTO */}
      <ViralHeader
        brand={PALACIO_ACOLHIMENTO_BRAND}
        title="O DIA QUE PESAVA 55 KG"
        category="HISTÓRIA REAL • PALÁCIO ACOLHIMENTO"
        hookSubtitle="O dia em que decidi dizer NÃO para mim mesmo."
      />

      {/* 8. LEGENDAS DINÂMICAS KARAOKE NA ZONA SEGURA (bottom: 540px) */}
      {frame < outroStartFrame && (
        <DynamicCaptions chunks={chunks} bottomPx={540} maxBoxWidth={880} />
      )}

      {/* 9. ENCERRAMENTO INSTITUCIONAL OFICIAL PALÁCIO ACOLHIMENTO */}
      {frame >= outroStartFrame && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            backgroundColor: `rgba(6, 10, 8, ${outroOpacity * 0.95})`,
            backdropFilter: `blur(${outroOpacity * 16}px)`,
            WebkitBackdropFilter: `blur(${outroOpacity * 16}px)`,
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
