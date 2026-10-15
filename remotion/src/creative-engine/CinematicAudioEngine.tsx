import React from "react";
import { Audio, Sequence, staticFile } from "remotion";

export interface SfxCue {
  id: string;
  name: string;
  src: string; // relativo à pasta public (ex: "sfx/01_impactos/cinematic_sub_hit.wav")
  startFrame: number;
  volume?: number;
}

interface CinematicAudioEngineProps {
  cues: SfxCue[];
  masterVoiceSrc: string; // ex: "corte2_audio.wav"
}

export const CinematicAudioEngine: React.FC<CinematicAudioEngineProps> = ({
  cues,
  masterVoiceSrc,
}) => {
  return (
    <>
      {/* 1. Trilha de Voz Masterizada Oficial (-14.1 LUFS) */}
      <Audio src={staticFile(masterVoiceSrc)} volume={1.0} />

      {/* 2. Efeitos Sonoros Narrativos Sincronizados Frame a Frame */}
      {cues.map((cue, idx) => (
        <Sequence
          key={`${cue.id}-${cue.startFrame}-${idx}`}
          from={cue.startFrame}
          name={`SFX_${cue.name}`}
        >
          <Audio src={staticFile(cue.src)} volume={cue.volume ?? 0.85} />
        </Sequence>
      ))}
    </>
  );
};
