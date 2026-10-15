import React from "react";
import {
  AbsoluteFill,
  OffthreadVideo,
  interpolate,
  staticFile,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";

interface CreativeFramedLayerProps {
  videoSrc: string;
  frameProgress: number; // 0 = Full screen total, 1 = Moldura 2.5D flutuante total
  cameraScale: number; // escala da câmera virtual
  cameraOrigin?: string; // ponto de ancoragem, padrão "50% 36%"
}

export const CreativeFramedLayer: React.FC<CreativeFramedLayerProps> = ({
  videoSrc,
  frameProgress,
  cameraScale,
  cameraOrigin = "50% 36%",
}) => {
  const frame = useCurrentFrame();
  const { width, height } = useVideoConfig();

  // Dimensões interpoladas entre Full Screen (100% x 100%) e Moldura 2.5D (86% x 68%)
  const cardWidthPercent = interpolate(frameProgress, [0, 1], [100, 86], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cardHeightPercent = interpolate(frameProgress, [0, 1], [100, 68], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cardBorderRadius = interpolate(frameProgress, [0, 1], [0, 36], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cardBorderWidth = interpolate(frameProgress, [0, 1], [0, 2.5], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const cardBorderAlpha = interpolate(frameProgress, [0, 1], [0, 0.75], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  // Flutuação orgânica sutil em modo moldura (Math.sin a 30fps)
  const floatY = frameProgress > 0.05 ? Math.sin(frame * 0.06) * (6 * frameProgress) : 0;

  // Opacidade do fundo ambiental com blur
  const ambientOpacity = interpolate(frameProgress, [0, 0.3, 1], [0, 0.8, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill style={{ overflow: "hidden", backgroundColor: "#060A08" }}>
      {/* ============================================================== */}
      {/* CAMADA 0: AMBIENT BACKGROUND BLUR (Ativo na transição)         */}
      {/* ============================================================== */}
      {frameProgress > 0.01 && (
        <div
          style={{
            position: "absolute",
            inset: -40,
            opacity: ambientOpacity,
            filter: "blur(36px) brightness(0.42) saturate(1.4)",
            transform: "scale(1.15)",
            pointerEvents: "none",
            zIndex: 10,
          }}
        >
          <OffthreadVideo
            src={staticFile(videoSrc)}
            volume={0}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
            }}
          />
          {/* Malha de gradiente atmosférico Palácio Acolhimento sobre o blur */}
          <div
            style={{
              position: "absolute",
              inset: 0,
              background:
                "radial-gradient(circle at 50% 50%, rgba(7, 75, 50, 0.35) 0%, rgba(6, 10, 8, 0.85) 100%)",
            }}
          />
        </div>
      )}

      {/* ============================================================== */}
      {/* CAMADA 1: VÍDEO PRINCIPAL (Modo Full Screen OU Moldura 2.5D)    */}
      {/* ============================================================== */}
      <div
        style={{
          position: "absolute",
          top: "46%",
          left: "50%",
          transform: `translate(-50%, -50%) translateY(${floatY}px)`,
          width: `${cardWidthPercent}%`,
          height: `${cardHeightPercent}%`,
          borderRadius: `${cardBorderRadius}px`,
          border: `${cardBorderWidth}px solid rgba(229, 169, 60, ${cardBorderAlpha})`,
          boxShadow:
            frameProgress > 0.05
              ? `0 35px 85px rgba(0, 0, 0, 0.95), 0 0 45px rgba(229, 169, 60, ${0.2 * frameProgress})`
              : "none",
          overflow: "hidden",
          zIndex: 20,
          transition: "all 0.08s ease-out",
        }}
      >
        <div
          style={{
            width: "100%",
            height: "100%",
            transform: `scale(${cameraScale})`,
            transformOrigin: cameraOrigin,
            transition: "transform 0.12s ease-out",
          }}
        >
          <OffthreadVideo
            src={staticFile(videoSrc)}
            volume={0}
            style={{
              width: "100%",
              height: "100%",
              objectFit: "cover",
              filter: "contrast(1.06) brightness(1.02) saturate(1.04)",
            }}
          />
        </div>

        {/* Reflexo chanfrado superior na moldura */}
        {frameProgress > 0.1 && (
          <div
            style={{
              position: "absolute",
              top: 0,
              left: 0,
              right: 0,
              height: "35%",
              background:
                "linear-gradient(180deg, rgba(243, 229, 171, 0.18) 0%, transparent 100%)",
              pointerEvents: "none",
            }}
          />
        )}
      </div>

      {/* ============================================================== */}
      {/* CAMADA 5: VINHETA PERIMETRAL DE PROFUNDIDADE                    */}
      {/* ============================================================== */}
      <div
        style={{
          position: "absolute",
          inset: 0,
          background:
            "radial-gradient(circle at 50% 38%, transparent 40%, rgba(6, 10, 8, 0.45) 82%, rgba(6, 10, 8, 0.88) 100%)",
          pointerEvents: "none",
          zIndex: 60,
        }}
      />
    </AbsoluteFill>
  );
};
