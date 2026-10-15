import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "../corte2_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "../motion-library/DynamicCaptions";
import { PalacioOutro } from "../motion-library/PalacioOutro";
import { ViralHeader } from "../motion-library/ViralHeader";
import { PALACIO_ACOLHIMENTO_BRAND } from "../motion-library/BrandConfig";
import { PALACIO_THEME } from "../motion-library/PalacioTheme";
import { CinematicAudioEngine, SfxCue } from "./CinematicAudioEngine";

const chunks = chunksData as SubtitleChunk[];

// Efeitos Sonoros Sincronizados com a Montagem
const SFX_CUES: SfxCue[] = [
  {
    id: "hook_impact",
    name: "Sub Impacto Gancho",
    src: "sfx/01_impactos/cinematic_sub_hit.wav",
    startFrame: 0,
    volume: 0.25,
  },
  {
    id: "morreu_impact",
    name: "Punch-in Morreu",
    src: "sfx/01_impactos/cinematic_sub_hit.wav",
    startFrame: 175,
    volume: 0.30,
  },
  {
    id: "broll1_whoosh",
    name: "Whoosh Entrada B-Roll 1",
    src: "sfx/02_transicoes/cinematic_whoosh.wav",
    startFrame: 216,
    volume: 0.22,
  },
  {
    id: "aroll_return_whoosh",
    name: "Whoosh Retorno A-Roll Close",
    src: "sfx/02_transicoes/cinematic_whoosh.wav",
    startFrame: 388,
    volume: 0.22,
  },
  {
    id: "broll2_whoosh",
    name: "Whoosh Entrada B-Roll 2",
    src: "sfx/02_transicoes/cinematic_whoosh.wav",
    startFrame: 718,
    volume: 0.20,
  },
  {
    id: "hope_chord",
    name: "Acorde de Resolução e Esperança",
    src: "sfx/05_cinematograficos/hope_resolution_chord.wav",
    startFrame: 720,
    volume: 0.18,
  },
  {
    id: "outro_pop",
    name: "Pop Encerramento Oficial",
    src: "sfx/06_motion_design/card_glass_pop.wav",
    startFrame: 795,
    volume: 0.20,
  },
];

export const IntelligentMontageComposition: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames } = useVideoConfig();

  // ==============================================================
  // DEFINIÇÃO DAS CENAS DE MONTAGEM (AUTO-BROLL MULTI-TRACK)
  // ==============================================================
  // Cena 1 (A-Roll Gancho): 0 a 218 frames (0.0s a 7.29s)
  // Cena 2 (B-Roll Cutaway 1 - Quarto / Solidão): 218 a 390 frames (7.29s a 13.0s)
  // Cena 3 (A-Roll Close Íntimo nos Olhos): 390 a 720 frames (13.0s a 24.0s)
  // Cena 4 (B-Roll Cutaway 2 - Família / Abraço na Clínica): 720 a 795 frames (24.0s a 26.5s)
  // Cena 5 (A-Roll Final + Outro Oficial): 795 a 851 frames (26.5s a 28.37s)

  const isBroll1Active = frame >= 218 && frame < 390;
  const isBroll2Active = frame >= 720 && frame < 795;
  const isArollActive = !isBroll1Active && !isBroll2Active;

  // Câmera Virtual A-Roll (Ancorada nos Olhos 50% 36%)
  let arollScale = 1.05;
  if (frame >= 175 && frame < 218) {
    arollScale = 1.22; // Punch-in semântico seco em "morreu!"
  } else if (frame >= 390 && frame < 720) {
    arollScale = interpolate(frame, [390, 420, 680, 720], [1.10, 1.15, 1.15, 1.08], {
      extrapolateLeft: "clamp",
      extrapolateRight: "clamp",
    });
  } else if (frame >= 795) {
    arollScale = 1.04;
  }

  // Drift Suave nos B-Rolls para dinamismo cinematográfico
  const broll1Scale = interpolate(frame, [218, 390], [1.02, 1.08], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const broll2Scale = interpolate(frame, [720, 795], [1.02, 1.06], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Outro Institucional Oficial a partir do frame 795
  const outroStartFrame = durationInFrames - 54; // 797f (~26.6s)
  const outroOpacity = interpolate(
    frame,
    [outroStartFrame, outroStartFrame + 14],
    [0, 1],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  return (
    <AbsoluteFill style={{ backgroundColor: "#060A08" }}>
      {/* ============================================================== */}
      {/* 1. MOTOR DE ÁUDIO SINCRONIZADO (VOZ MASTER + SFX NARRATIVOS)   */}
      {/* ============================================================== */}
      <CinematicAudioEngine
        masterVoiceSrc="corte2_audio.wav"
        cues={SFX_CUES}
      />

      {/* ============================================================== */}
      {/* 2. PISTA DE VÍDEO PRINCIPAL (A-ROLL: MARCELO PALÁCIO)          */}
      {/* ============================================================== */}
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
            transformOrigin: "50% 36%",
            transition: "transform 0.1s ease-out",
          }}
        >
          <OffthreadVideo
            src={staticFile("corte2_video.mp4")}
            volume={0}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "contrast(1.06) brightness(1.02) saturate(1.03)",
            }}
          />
        </div>
      </div>

      {/* ============================================================== */}
      {/* 3. PISTA B-ROLL 1: CUTAWAY DA SOLIDÃO / DOR (AutoBroll Style)   */}
      {/* ============================================================== */}
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
              transformOrigin: "50% 50%",
            }}
          >
            <OffthreadVideo
              src={staticFile("broll/homem_solidao_quarto.mp4")}
              volume={0}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "contrast(1.08) brightness(0.96) saturate(1.1)",
              }}
            />
          </div>

          {/* Badge Contextual Glassmorphism */}
          <div
            style={{
              position: "absolute",
              top: "120px",
              left: "50%",
              transform: "translateX(-50%)",
              zIndex: 35,
              pointerEvents: "none",
            }}
          >
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "8px 20px",
                background: "rgba(6, 10, 8, 0.65)",
                backdropFilter: "blur(16px)",
                border: "1px solid rgba(229, 169, 60, 0.45)",
                borderRadius: "999px",
                boxShadow: "0 8px 30px rgba(0, 0, 0, 0.7)",
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
                  fontSize: "17px",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                }}
              >
                A Dor da Dependência
              </span>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* 4. PISTA B-ROLL 2: CUTAWAY DO ACOLHIMENTO FAMILIAR NA CLÍNICA  */}
      {/* ============================================================== */}
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
              transformOrigin: "50% 50%",
            }}
          >
            <OffthreadVideo
              src={staticFile("broll/pai_filho_acolhimento.mp4")}
              volume={0}
              style={{
                width: "100%",
                height: "100%",
                objectFit: "cover",
                filter: "contrast(1.05) brightness(1.0) saturate(1.05)",
              }}
            />
          </div>

          {/* Badge Contextual de Família & Acolhimento */}
          <div
            style={{
              position: "absolute",
              top: "120px",
              left: "50%",
              transform: "translateX(-50%)",
              zIndex: 35,
              pointerEvents: "none",
            }}
          >
            <div
              style={{
                display: "inline-flex",
                alignItems: "center",
                gap: "8px",
                padding: "8px 20px",
                background: "rgba(7, 75, 50, 0.65)",
                backdropFilter: "blur(16px)",
                border: "1px solid rgba(229, 169, 60, 0.55)",
                borderRadius: "999px",
                boxShadow: "0 8px 30px rgba(0, 0, 0, 0.7)",
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
                  fontSize: "17px",
                  fontWeight: 700,
                  letterSpacing: "0.12em",
                  textTransform: "uppercase",
                }}
              >
                Acolhimento Familiar • Palácio Acolhimento
              </span>
            </div>
          </div>
        </div>
      )}

      {/* ============================================================== */}
      {/* 5. VINHETA PERIMETRAL DE PROFUNDIDADE CINEMATOGRÁFICA          */}
      {/* ============================================================== */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 38%, transparent 42%, rgba(6, 10, 8, 0.42) 84%, rgba(6, 10, 8, 0.88) 100%)",
          pointerEvents: "none",
          zIndex: 40,
        }}
      />

      {/* ============================================================== */}
      {/* 6. CABEÇALHO COMPACTO SUPERIOR (ZONA SEGURA TOP: 116PX)       */}
      {/* ============================================================== */}
      <ViralHeader
        title="NÃO QUERO PERDER VOCÊ"
        category="HISTÓRIAS REAIS • ACOLHIMENTO"
        brand={PALACIO_ACOLHIMENTO_BRAND}
      />

      {/* ============================================================== */}
      {/* 7. LEGENDAS DINÂMICAS ANIMADAS NA ZONA SEGURA (Y: 1380PX)      */}
      {/* ============================================================== */}
      {frame < outroStartFrame && (
        <DynamicCaptions
          chunks={chunks}
          theme={PALACIO_THEME}
          bottomPx={540}
        />
      )}

      {/* ============================================================== */}
      {/* 8. OUTRO INSTITUCIONAL OFICIAL PALÁCIO ACOLHIMENTO             */}
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
