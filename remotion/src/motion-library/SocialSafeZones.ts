/**
 * PALÁCIO SOCIAL SAFE ZONES (v7.0)
 * Sistema de Zonas Seguras para Redes Sociais em TypeScript.
 */

export interface SafeZoneProfile {
  platform: string;
  frameWidth: number;
  frameHeight: number;
  topMargin: number;
  bottomMargin: number;
  leftMargin: number;
  rightMargin: number;
  subtitleYMin: number;
  subtitleYMax: number;
  subtitleDefaultY: number;
  subtitleBottomPx: number;
  maxSubtitleWidth: number;
}

export const SOCIAL_SAFE_ZONES: Record<string, SafeZoneProfile> = {
  INSTAGRAM_REELS: {
    platform: "Instagram Reels",
    frameWidth: 1080,
    frameHeight: 1920,
    topMargin: 140,
    bottomMargin: 450,
    leftMargin: 60,
    rightMargin: 130,
    subtitleYMin: 1180,
    subtitleYMax: 1420,
    subtitleDefaultY: 1280,
    subtitleBottomPx: 540,
    maxSubtitleWidth: 860,
  },
  TIKTOK_VERTICAL: {
    platform: "TikTok",
    frameWidth: 1080,
    frameHeight: 1920,
    topMargin: 160,
    bottomMargin: 480,
    leftMargin: 60,
    rightMargin: 140,
    subtitleYMin: 1180,
    subtitleYMax: 1390,
    subtitleDefaultY: 1260,
    subtitleBottomPx: 560,
    maxSubtitleWidth: 850,
  },
  YOUTUBE_SHORTS: {
    platform: "YouTube Shorts",
    frameWidth: 1080,
    frameHeight: 1920,
    topMargin: 130,
    bottomMargin: 420,
    leftMargin: 60,
    rightMargin: 130,
    subtitleYMin: 1180,
    subtitleYMax: 1420,
    subtitleDefaultY: 1290,
    subtitleBottomPx: 530,
    maxSubtitleWidth: 860,
  },
  FACEBOOK_REELS: {
    platform: "Facebook Reels",
    frameWidth: 1080,
    frameHeight: 1920,
    topMargin: 140,
    bottomMargin: 440,
    leftMargin: 60,
    rightMargin: 130,
    subtitleYMin: 1180,
    subtitleYMax: 1410,
    subtitleDefaultY: 1280,
    subtitleBottomPx: 540,
    maxSubtitleWidth: 860,
  },
  SOCIAL_VERTICAL_MASTER: {
    platform: "Master Universal",
    frameWidth: 1080,
    frameHeight: 1920,
    topMargin: 160,
    bottomMargin: 480,
    leftMargin: 65,
    rightMargin: 140,
    subtitleYMin: 1200,
    subtitleYMax: 1380,
    subtitleDefaultY: 1280,
    subtitleBottomPx: 540,
    maxSubtitleWidth: 840,
  },
};

export function getSafeZoneProfile(profileName: string = "SOCIAL_VERTICAL_MASTER"): SafeZoneProfile {
  return SOCIAL_SAFE_ZONES[profileName] || SOCIAL_SAFE_ZONES["SOCIAL_VERTICAL_MASTER"];
}
