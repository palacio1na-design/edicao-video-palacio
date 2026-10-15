import { Composition, staticFile } from "remotion";
import { DemoShowreel } from "./DemoShowreel";
import { Scene, myCompSchema } from "./Scene";
import { Teste1Composition } from "./Teste1Composition";
import { getMediaMetadata } from "./helpers/get-media-metadata";

export const RemotionRoot: React.FC = () => {
  return (
    <>
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
