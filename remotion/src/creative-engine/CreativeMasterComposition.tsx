import React from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "../corte2_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "../motion-library/DynamicCaptions";
import { PalacioOutro } from "../motion-library/PalacioOutro";
import { ViralHeader } from "../motion-library/ViralHeader";
import { PALACIO_ACOLHIMENTO_BRAND } from "../motion-library/BrandConfig";
import { PALACIO_THEME } from "../motion-library/PalacioTheme";
import { CreativeFramedLayer } from "./CreativeFramedLayer";
import { CinematicAudioEngine, SfxCue } from "./CinematicAudioEngine";
import { ThreeDStepsScene } from "../motion-library/ThreeDStepsScene";

const chunks = chunksData as SubtitleChunk[];

// Matriz de Efeitos Sonoros Sincronizados Calibrados (Palácio Sound Library)
const SFX_CUES: SfxCue[] = [
  {
    id: "hook_impact",
    name: "Sub Impacto Abertura",
    src: "sfx/01_impactos/cinematic_sub_hit.wav",
    startFrame: 0,
    volume: 0.25,
  },
  {
    id: "morreu_impact",
    name: "Sub Impacto Morreu",
    src: "sfx/01_impactos/cinematic_sub_hit.wav",
    startFrame: 175,
    volume: 0.30,
  },
  {
    id: "tension_drone",
    name: "Drone de Tensão e Dor",
    src: "sfx/05_cinematograficos/tension_drone_c_minor.wav",
    startFrame: 180,
    volume: 0.12,
  },
  {
    id: "transition_whoosh",
    name: "Whoosh para Moldura 2.5D",
    src: "sfx/02_transicoes/cinematic_whoosh.wav",
    startFrame: 388,
    volume: 0.20,
  },
  {
    id: "card_pop_in",
    name: "Pop de Card Editorial",
    src: "sfx/06_motion_design/card_glass_pop.wav",
    startFrame: 410,
    volume: 0.20,
  },
  {
    id: "return_whoosh",
    name: "Whoosh Retorno Full Screen",
    src: "sfx/02_transicoes/cinematic_whoosh.wav",
    startFrame: 658,
    volume: 0.20,
  },
  {
    id: "hope_chord",
    name: "Acorde de Resolução e Esperança",
    src: "sfx/05_cinematograficos/hope_resolution_chord.wav",
    startFrame: 720,
    volume: 0.15,
  },
  {
    id: "outro_pop",
    name: "Pop Encerramento Oficial",
    src: "sfx/06_motion_design/card_glass_pop.wav",
    startFrame: 795,
    volume: 0.20,
  },
];

export const CreativeMasterComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // ==============================================================
  // 1. PALACIO-RITMO & PALACIO-MOVIMENTO: Curva de Câmera e Escala
  // ==============================================================
  // Ato 1 (0-135f / 0.0s - 4.5s): 1.05x (abertura estável com foco nos olhos)
  // Ato 2 (135-390f / 4.5s - 13.0s): Punch-in seco aos 175f (5.8s) em "morreu!" para 1.22x
  // Ato 3 (390-660f / 13.0s - 22.0s): Composição em Moldura 2.5D (câmera interna em 1.08x)
  // Ato 4 (660-780f / 22.0s - 26.0s): Retorno para Full Screen com close intimista em 1.16x
  // Ato 5 (780f+ / 26.0s+): Resolução e recuo suave para 1.04x
  let cameraScale = 1.05;
  if (frame >= 175 && frame < 390) {
    cameraScale = 1.22; // Punch-in semântico imediato
  } else if (frame >= 390 && frame < 660) {
    cameraScale = 1.08;
  } else if (frame >= 660 && frame < 780) {
    cameraScale = interpolate(frame, [660, 685, 750, 780], [1.08, 1.16, 1.16, 1.05], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 780) {
    cameraScale = 1.04;
  }

  // ==============================================================
  // 2. PALACIO-COMPOSICAO: Transição da Moldura Flutuante 2.5D
  // ==============================================================
  // Início da moldura: frame 390 (13.0s)
  // Fim da moldura: frame 660 (22.0s)
  const frameEntrance = spring({
    frame: frame - 390,
    fps,
    config: { damping: 14, mass: 0.9, stiffness: 110 },
  });
  const frameExit = spring({
    frame: frame - 650,
    fps,
    config: { damping: 14, mass: 0.9, stiffness: 110 },
  });

  let framedProgress = 0;
  if (frame >= 390 && frame < 650) {
    framedProgress = Math.min(1, Math.max(0, frameEntrance));
  } else if (frame >= 650 && frame < 685) {
    framedProgress = Math.max(0, 1 - frameExit);
  }

  // Badge Narrativo Glassmorphism no Modo Moldura
  const badgeStart = 410;
  const badgeEnd = 650;
  const isBadgeActive = frame >= badgeStart && frame <= badgeEnd;
  const badgeOpacity = interpolate(
    frame,
    [badgeStart, badgeStart + 15, badgeEnd - 15, badgeEnd],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  // Outro Institucional nos últimos 52 frames (~1.73s, após o término da fala)
  const outroStartFrame = durationInFrames - 52;
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 14],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* ============================================================== */}
      {/* MOTORES DE ÁUDIO SINCRONIZADOS (SOUND DIRECTOR + SFX LIBRARY)  */}
      {/* ============================================================== */}
      <CinematicAudioEngine
        masterVoiceSrc="corte2_audio.wav"
        cues={SFX_CUES}
      />

      {/* ============================================================== */}
      {/* COMPOSIÇÃO VISUAL: MOLDURA 2.5D, AMBIENT BLUR & CÂMERA VIRTUAL */}
      {/* ============================================================== */}
      <CreativeFramedLayer
        videoSrc="corte2_video.mp4"
        frameProgress={framedProgress}
        cameraScale={cameraScale}
        cameraOrigin="50% 36%"
      />

      {/* ============================================================== */}
      {/* ELEMENTO GRÁFICO 3D SUTIL NO MODO COMPOSIÇÃO (THREE.JS)       */}
      {/* ============================================================== */}
      {framedProgress > 0.4 && (
        <div
          style={{
            position: "absolute",
            top: "14%",
            right: "4%",
            width: "320px",
            height: "320px",
            opacity: framedProgress * 0.75,
            pointerEvents: "none",
            zIndex: 35,
          }}
        >
          <ThreeDStepsScene step={2} />
        </div>
      )}

      {/* ============================================================== */}
      {/* BADGE EDITORIAL GLASSMORHPISM EM ZONA SEGURA                   */}
      {/* ============================================================== */}
      {isBadgeActive && (
        <div
          style={{
            position: "absolute",
            top: "120px",
            left: "50%",
            transform: "translateX(-50%)",
            opacity: badgeOpacity,
            zIndex: 48,
            pointerEvents: "none",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: "10px",
              padding: "10px 24px",
              background: "rgba(7, 75, 50, 0.55)",
              backdropFilter: "blur(20px)",
              WebkitBackdropFilter: "blur(20px)",
              border: "1px solid rgba(229, 169, 60, 0.55)",
              borderRadius: "999px",
              boxShadow: "0 8px 32px rgba(0, 0, 0, 0.65)",
            }}
          >
            <span
              style={{
                width: "8px",
                height: "8px",
                borderRadius: "50%",
                backgroundColor: "#E5A93C",
                boxShadow: "0 0 10px #E5A93C",
              }}
            />
            <span
              style={{
                color: "#FFFFFF",
                fontFamily: "system-ui, -apple-system, sans-serif",
                fontSize: "19px",
                fontWeight: 700,
                letterSpacing: "0.14em",
                textTransform: "uppercase",
              }}
            >
              A Dor da Família • Salve uma Vida
            </span>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* CABEÇALHO COMPACTO SUPERIOR (PALACIO-ESTILO / BRAND CONFIG)    */}
      {/* ============================================================== */}
      <ViralHeader
        title="NÃO QUERO PERDER VOCÊ"
        category="HISTÓRIAS REAIS • ACOLHIMENTO"
        brand={PALACIO_ACOLHIMENTO_BRAND}
      />

      {/* ============================================================== */}
      {/* LEGENDAS DINÂMICAS ELEVADAS NA ZONA SEGURA (PALACIO-LEGENDAS)  */}
      {/* ============================================================== */}
      {frame < outroStartFrame && (
        <DynamicCaptions
          chunks={chunks}
          theme={PALACIO_THEME}
          bottomPx={540}
        />
      )}

      {/* ============================================================== */}
      {/* OUTRO INSTITUCIONAL OFICIAL PALÁCIO ACOLHIMENTO               */}
      {/* ============================================================== */}
      {frame >= outroStartFrame && (
        <div
          style={{
            position: "absolute",
            inset: 0,
            opacity: outroOpacity,
            zIndex: 90,
          }}
        >
          <PalacioOutro
            brand={PALACIO_ACOLHIMENTO_BRAND}
            theme={PALACIO_THEME}
          />
        </div>
      )}
    </AbsoluteFill>
  );
};
