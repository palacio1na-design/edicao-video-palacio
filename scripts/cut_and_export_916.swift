import Foundation
import AVFoundation

guard CommandLine.arguments.count >= 5 else {
    print("Usage: swift cut_and_export_916.swift <input.mp4> <output.mp4> <start_seconds> <duration_seconds>")
    exit(1)
}

let inputPath = CommandLine.arguments[1]
let outputPath = CommandLine.arguments[2]
let startSec = Double(CommandLine.arguments[3]) ?? 0.0
let durSec = Double(CommandLine.arguments[4]) ?? 60.0

let inputURL = URL(fileURLWithPath: inputPath)
let outputURL = URL(fileURLWithPath: outputPath)
try? FileManager.default.removeItem(at: outputURL)

let asset = AVURLAsset(url: inputURL)
guard let videoTrack = asset.tracks(withMediaType: .video).first,
      let audioTrack = asset.tracks(withMediaType: .audio).first else {
    print("Tracks not found")
    exit(1)
}

let composition = AVMutableComposition()
let compVideo = composition.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid)!
let compAudio = composition.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid)!

let startTime = CMTime(seconds: startSec, preferredTimescale: 600)
let duration = CMTime(seconds: durSec, preferredTimescale: 600)
let timeRange = CMTimeRange(start: startTime, duration: duration)

try! compVideo.insertTimeRange(timeRange, of: videoTrack, at: .zero)
try! compAudio.insertTimeRange(timeRange, of: audioTrack, at: .zero)

let videoComposition = AVMutableVideoComposition()
videoComposition.renderSize = CGSize(width: 1080, height: 1920)
videoComposition.frameDuration = CMTime(value: 1, timescale: 30)

let instruction = AVMutableVideoCompositionInstruction()
instruction.timeRange = CMTimeRange(start: .zero, duration: duration)

let scale: CGFloat = 1920.0 / 720.0
let tx: CGFloat = (1080.0 - 1280.0 * scale) / 2.0
let transform = CGAffineTransform(scaleX: scale, y: scale).concatenating(CGAffineTransform(translationX: tx, y: 0))

let layerInstruction = AVMutableVideoCompositionLayerInstruction(assetTrack: compVideo)
layerInstruction.setTransform(transform, at: .zero)

instruction.layerInstructions = [layerInstruction]
videoComposition.instructions = [instruction]

let exportSession = AVAssetExportSession(asset: composition, presetName: AVAssetExportPresetHighestQuality)!
exportSession.outputURL = outputURL
exportSession.outputFileType = .mp4
exportSession.videoComposition = videoComposition

let sema = DispatchSemaphore(value: 0)
exportSession.exportAsynchronously {
    if exportSession.status == .completed {
        print("Success: \(outputPath)")
    } else {
        print("Failed: \(String(describing: exportSession.error))")
    }
    sema.signal()
}
sema.wait()
