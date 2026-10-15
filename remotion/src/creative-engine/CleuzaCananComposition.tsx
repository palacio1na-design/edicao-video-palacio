import React from "react";
import {
  AbsoluteFill,
  Audio,
  interpolate,
  OffthreadVideo,
  spring,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import chunksData from "../corte2_chunks_refined.json";
import { DynamicCaptions, SubtitleChunk } from "../motion-library/DynamicCaptions";
import { PalacioOutro } from "../motion-library/PalacioOutro";
import { PALACIO_ACOLHIMENTO_BRAND } from "../motion-library/BrandConfig";

const chunks = chunksData as SubtitleChunk[];

export interface CloseUpRange {
  startFrame: number;
  endFrame: number;
  zoom?: number;
}

export interface CleuzaCananProps {
  headline?: string;
  category?: string;
  videoSrc?: string;
  audioSrc?: string;
  musicSrc?: string;
  musicVolume?: number;
  chunks?: SubtitleChunk[];
  closeUpRanges?: CloseUpRange[];
}

/**
 * COMPOSIÇÃO ESTILO CLEUZA CANAN (PALÁCIO ACOLHIMENTO HUMANIZADO)
 * 
 * Filosofia:
 * 1. Zero poluição visual: tela cheia 9:16 nativa, sem molduras 2.5D artificiais ou fundos borrados.
 * 2. Headline de impacto na Zona Segura Superior (top: 130px) com contraste clínico refinado.
 * 3. Legendas dinâmicas em alta legibilidade (branco + destaque dourado suave).
 * 4. Alternância de Câmeras (Plano Médio 1.0x -> Close de Emoção 1.16x focado nos olhos).
 * 5. Cama sonora de piano/cordas a -24 dB abaixo da voz.
 * 6. Encerramento oficial com Monograma 'P' Dourado de Palácio Acolhimento.
 */
export const CleuzaCananComposition: React.FC<CleuzaCananProps> = ({
  headline = "SEU FILHO PRECISA DE AJUDA?",
  category = "ACOLHIMENTO FAMILIAR",
  videoSrc = "corte2_video.mp4",
  audioSrc = "corte2_audio.wav",
  musicSrc = "versao_b_soundtrack.wav",
  musicVolume = 0.07,
  chunks: customChunks,
  closeUpRanges = [
    { startFrame: 55, endFrame: 175, zoom: 1.16 },    // Gancho "morreu!"
    { startFrame: 390, endFrame: 720, zoom: 1.14 },   // Retorno íntimo olho no olho
  ],
}) => {
  const frame = useCurrentFrame();
  const { fps, durationInFrames, width, height } = useVideoConfig();
  const currentChunks = customChunks || chunks;

  // 1. Cálculo de Câmera (Plano A Médio -> Câmera B Close Íntimo)
  let activeZoom = 1.0;
  for (const range of closeUpRanges) {
    if (frame >= range.startFrame && frame <= range.endFrame) {
      const enterSpring = spring({
        frame: frame - range.startFrame,
        fps,
        config: { damping: 16, stiffness: 120, mass: 0.8 },
      });
      activeZoom = interpolate(enterSpring, [0, 1], [1.0, range.zoom || 1.16]);
      break;
    }
  }

  // 2. Transição de Entrada e Fade de Encerramento
  const outroDuration = 60; // 2 segundos
  const outroStartFrame = durationInFrames - outroDuration;
  const isOutroActive = frame >= outroStartFrame;

  const contentOpacity = interpolate(
    frame,
    [outroStartFrame - 15, outroStartFrame],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" }
  );

  // 3. Volume da Trilha Musical com Fade In / Fade Out
  const musicFadeIn = interpolate(frame, [0, 30], [0, musicVolume], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const musicCurrentVolume = isOutroActive
    ? interpolate(frame, [outroStartFrame, durationInFrames], [musicVolume, 0], {
        extrapolateLeft: "clamp",
        extrapolateRight: "clamp",
      })
    : musicFadeIn;

  return (
    <AbsoluteFill
      style={{
        backgroundColor: "#080B0E",
        overflow: "hidden",
      }}
    >
      {/* TRILHAS DE ÁUDIO */}
      {audioSrc && <Audio src={staticFile(audioSrc)} volume={1.0} />}
      {musicSrc && <Audio src={staticFile(musicSrc)} volume={musicCurrentVolume} />}

      {/* VÍDEO PRINCIPAL EM TELA CHEIA (SEM MOLDURAS ARTIFICIAIS) */}
      <AbsoluteFill
        style={{
          opacity: contentOpacity,
          transform: `scale(${activeZoom})`,
          transformOrigin: "50% 36%", // Foco na linha dos olhos
          transition: "transform 0.1s ease-out",
        }}
      >
        <OffthreadVideo
          src={staticFile(videoSrc)}
          style={{
            width: "100%",
            height: "100%",
            objectFit: "cover",
          }}
        />

        {/* VINHETA CINEMATOGRÁFICA SUTIL (Contraste sem escurecer a face) */}
        <AbsoluteFill
          style={{
            background:
              "radial-gradient(ellipse 90% 80% at 50% 40%, rgba(0,0,0,0) 50%, rgba(4,6,8,0.45) 100%)",
            pointerEvents: "none",
          }}
        />

        {/* GRADIENTE SUPERIOR PARA LEITURA DO HEADLINE */}
        <div
          style={{
            position: "absolute",
            top: 0,
            left: 0,
            right: 0,
            height: 380,
            background:
              "linear-gradient(to bottom, rgba(4,7,10,0.85) 0%, rgba(4,7,10,0.4) 60%, rgba(4,7,10,0) 100%)",
            pointerEvents: "none",
          }}
        />

        {/* GRADIENTE INFERIOR PARA LEITURA DAS LEGENDAS */}
        <div
          style={{
            position: "absolute",
            bottom: 0,
            left: 0,
            right: 0,
            height: 480,
            background:
              "linear-gradient(to top, rgba(4,7,10,0.88) 0%, rgba(4,7,10,0.45) 60%, rgba(4,7,10,0) 100%)",
            pointerEvents: "none",
          }}
        />
      </AbsoluteFill>

      {/* HEADLINE ESTILO CLEUZA CANAN (ZONA SEGURA SUPERIOR: TOP 130PX) */}
      <div
        style={{
          position: "absolute",
          top: 130,
          left: 48,
          right: 48,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          opacity: contentOpacity,
          pointerEvents: "none",
        }}
      >
        {/* BADGE DA CATEGORIA CLÍNICA */}
        <div
          style={{
            backgroundColor: "rgba(229, 169, 60, 0.18)",
            border: "1px solid rgba(229, 169, 60, 0.45)",
            padding: "6px 18px",
            borderRadius: 30,
            marginBottom: 10,
            backdropFilter: "blur(8px)",
          }}
        >
          <span
            style={{
              fontFamily: "Inter, Montserrat, sans-serif",
              fontSize: 18,
              fontWeight: 700,
              color: "#E5A93C",
              letterSpacing: 2.2,
              textTransform: "uppercase",
            }}
          >
            {category}
          </span>
        </div>

        {/* TÍTULO DE GANCHO IMPACTANTE */}
        <h1
          style={{
            fontFamily: "Inter, Montserrat, sans-serif",
            fontSize: 44,
            fontWeight: 800,
            color: "#FFFFFF",
            textAlign: "center",
            lineHeight: 1.18,
            letterSpacing: -0.5,
            margin: 0,
            textTransform: "uppercase",
            textShadow: "0 4px 18px rgba(0, 0, 0, 0.75)",
            maxWidth: 920,
          }}
        >
          {headline}
        </h1>
      </div>

      {/* LEGENDAS DINÂMICAS SÓBRIAS (ZONA SEGURA UNIVERSAL: BOTTOM 540PX) */}
      <div
        style={{
          opacity: contentOpacity,
          pointerEvents: "none",
        }}
      >
        <DynamicCaptions
          chunks={currentChunks}
          bottomPx={540}
          activeColor="#E5A93C" // Dourado Nobre
          inactiveColor="#FFFFFF"
          boxBackground="rgba(6, 10, 15, 0.75)"
          fontSize={44}
        />
      </div>

      {/* ENCERRAMENTO OFICIAL PALÁCIO ACOLHIMENTO */}
      {isOutroActive && (
        <AbsoluteFill
          style={{
            backgroundColor: "#060A0E",
          }}
        >
          <PalacioOutro
            brand={PALACIO_ACOLHIMENTO_BRAND}
            ctaText="Vem pro Acolhimento Familiar"
          />
        </AbsoluteFill>
      )}
    </AbsoluteFill>
  );
};
