import { Composition, staticFile } from "remotion";
import { Corte1Composition } from "./Corte1Composition";
import { Corte2Composition } from "./Corte2Composition";
import { Corte2CorrigidoComposition } from "./Corte2CorrigidoComposition";
import { Corte2CinematicoComposition } from "./Corte2CinematicoComposition";
import { CreativeMasterComposition } from "./creative-engine/CreativeMasterComposition";
import { IntelligentMontageComposition } from "./creative-engine/IntelligentMontageComposition";
import { CleuzaCananComposition } from "./creative-engine/CleuzaCananComposition";
import { DemoShowreel } from "./DemoShowreel";
import { Scene, myCompSchema } from "./Scene";
import { Teste1Composition } from "./Teste1Composition";
import { VersaoBComposition } from "./VersaoBComposition";
import { getMediaMetadata } from "./helpers/get-media-metadata";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="corte-2-cleuza-canan"
        component={CleuzaCananComposition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
        defaultProps={{
          headline: "POR QUE VOCÊ NÃO CONSEGUE DIZER NÃO?",
          category: "ACOLHIMENTO FAMILIAR",
          videoSrc: "corte2_video.mp4",
          audioSrc: "corte2_audio.wav",
          musicSrc: "versao_b_soundtrack.wav",
          musicVolume: 0.07,
        }}
      />
      <Composition
        id="corte-2-intelligent-montage"
        component={IntelligentMontageComposition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
      />
      <Composition
        id="corte-2-creative-master"
        component={CreativeMasterComposition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
      />
      <Composition
        id="corte-2-corrigido"
        component={Corte2CorrigidoComposition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
      />
      <Composition
        id="corte-2-cinematico"
        component={Corte2CinematicoComposition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
      />
      <Composition
        id="corte-1-55kg"
        component={Corte1Composition}
        fps={30}
        durationInFrames={1388}
        width={1080}
        height={1920}
      />
      <Composition
        id="corte-2-amigos"
        component={Corte2Composition}
        fps={30}
        durationInFrames={851}
        width={1080}
        height={1920}
      />
      <Composition
        id="versao-b"
        component={VersaoBComposition}
        fps={30}
        durationInFrames={1164}
        width={1080}
        height={1920}
      />
      <Composition
        id="teste-1"
        component={Teste1Composition}
        fps={30}
        durationInFrames={1468}
        width={1080}
        height={1920}
      />
      <Composition
        id="DemoShowreel"
        component={DemoShowreel}
        fps={30}
        durationInFrames={450}
        width={1080}
        height={1920}
      />
      <Composition
        id="Scene"
        component={Scene}
        fps={30}
        durationInFrames={300}
        width={1280}
        height={720}
        schema={myCompSchema}
        defaultProps={{
          deviceType: "phone",
          phoneColor: "rgb(110, 152, 191)" as const,
          baseScale: 1,
          mediaMetadata: null,
          videoSrc: null,
        }}
        calculateMetadata={async ({ props }) => {
          const videoSrc =
            props.deviceType === "phone"
              ? staticFile("phone.mp4")
              : staticFile("tablet.mp4");

          const mediaMetadata = await getMediaMetadata(videoSrc);

          return {
            props: {
              ...props,
              mediaMetadata,
              videoSrc,
            },
          };
        }}
      />
    </>
  );
};
