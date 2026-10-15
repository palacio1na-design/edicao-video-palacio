import { useThree } from "@react-three/fiber";
import { ThreeCanvas } from "@remotion/three";
import React, { useEffect, useRef } from "react";
import {
  AbsoluteFill,
  interpolate,
  spring,
  useCurrentFrame,
  useVideoConfig,
} from "remotion";
import * as THREE from "three";
import { PALACIO_THEME } from "./PalacioTheme";

// Componente interno Three.js para o objeto 3D que reage deterministicamente ao frame
const Token3D: React.FC<{
  step: 1 | 2 | 3;
}> = ({ step }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const camera = useThree((state) => state.camera);

  useEffect(() => {
    camera.position.set(0, 1.2, 8.5);
    camera.lookAt(0, 0, 0);
  }, [camera]);

  // Rotação suave constante
  const rotationY = frame * 0.025;
  const rotationX = Math.sin(frame * 0.02) * 0.3;
  const floatY = Math.sin(frame * 0.04) * 0.25;

  // Transição de escala de entrada para cada etapa
  const scaleSpring = spring({
    frame,
    fps,
    config: PALACIO_THEME.springs.gentle,
  });
  const currentScale = interpolate(scaleSpring, [0, 1], [0.4, 1.0]);

  return (
    <group position={[0, floatY, 0]} scale={currentScale}>
      {step === 1 && (
        // ETAPA 1: Nó Toroidal Dourado / Escudo (Ruptura com a adicção / Parar)
        <group rotation={[rotationX, rotationY, 0]}>
          <mesh>
            <torusKnotGeometry args={[1.5, 0.42, 128, 32, 2, 3]} />
            <meshStandardMaterial
              color="#D4AF37"
              roughness={0.25}
              metalness={0.85}
              emissive="#3A2D05"
              emissiveIntensity={0.2}
            />
          </mesh>
          {/* Anel orbital externo esmeralda */}
          <mesh rotation={[Math.PI / 3, frame * 0.015, 0]}>
            <torusGeometry args={[2.4, 0.04, 16, 64]} />
            <meshStandardMaterial
              color="#074B32"
              roughness={0.1}
              metalness={0.9}
              emissive="#0D6B4A"
              emissiveIntensity={0.4}
            />
          </mesh>
        </group>
      )}

      {step === 2 && (
        // ETAPA 2: Icosaedro Esmeralda Multifacetado (Cuidar da mente e das emoções)
        <group rotation={[rotationX, -rotationY, 0]}>
          <mesh>
            <icosahedronGeometry args={[1.9, 0]} />
            <meshStandardMaterial
              color="#074B32"
              roughness={0.15}
              metalness={0.7}
              emissive="#0D6B4A"
              emissiveIntensity={0.35}
              flatShading
            />
          </mesh>
          {/* Wireframe dourado sobreposto */}
          <mesh scale={1.03}>
            <icosahedronGeometry args={[1.9, 0]} />
            <meshBasicMaterial
              color="#D4AF37"
              wireframe
              transparent
              opacity={0.65}
            />
          </mesh>
          {/* Halo sutil */}
          <mesh rotation={[-Math.PI / 4, frame * -0.02, 0]}>
            <torusGeometry args={[2.5, 0.03, 16, 64]} />
            <meshStandardMaterial
              color="#F3E5AB"
              roughness={0.2}
              metalness={0.8}
            />
          </mesh>
        </group>
      )}

      {step === 3 && (
        // ETAPA 3: Octaedro / Pilar Diamante (Reconstruir a vida com solidez)
        <group rotation={[rotationX * 0.7, rotationY * 1.2, 0]}>
          <mesh>
            <octahedronGeometry args={[2.0, 0]} />
            <meshStandardMaterial
              color="#F3E5AB"
              roughness={0.2}
              metalness={0.9}
              emissive="#D4AF37"
              emissiveIntensity={0.25}
              flatShading
            />
          </mesh>
          {/* Duplo anel orbital em eixos cruzados */}
          <mesh rotation={[Math.PI / 4, frame * 0.02, 0]}>
            <torusGeometry args={[2.6, 0.05, 16, 64]} />
            <meshStandardMaterial
              color="#074B32"
              roughness={0.1}
              metalness={0.9}
              emissive="#0D6B4A"
              emissiveIntensity={0.5}
            />
          </mesh>
          <mesh rotation={[-Math.PI / 4, -frame * 0.02, 0]}>
            <torusGeometry args={[2.8, 0.04, 16, 64]} />
            <meshStandardMaterial
              color="#D4AF37"
              roughness={0.2}
              metalness={0.8}
            />
          </mesh>
        </group>
      )}
    </group>
  );
};

export const ThreeDStepsScene: React.FC<{
  step: 1 | 2 | 3;
}> = ({ step }) => {
  const { width, height } = useVideoConfig();

  return (
    <AbsoluteFill style={{ pointerEvents: "none" }}>
      <ThreeCanvas
        linear
        width={width}
        height={height}
        style={{
          width: "100%",
          height: "100%",
        }}
      >
        {/* Iluminação de estúdio profissional com realce dourado e esmeralda */}
        <ambientLight intensity={1.2} color={0xffffff} />
        <directionalLight position={[5, 8, 5]} intensity={2.2} color={0xfff2cc} />
        <directionalLight position={[-6, -4, -3]} intensity={1.5} color={0x074b32} />
        <pointLight position={[0, -2, 4]} intensity={1.8} color={0xd4af37} />

        <Token3D step={step} />
      </ThreeCanvas>
    </AbsoluteFill>
  );
};
