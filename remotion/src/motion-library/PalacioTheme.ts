export const PALACIO_THEME = {
  colors: {
    // Cores Primárias Oficiais Palácio.pro
    deepGreen: "#074B32",
    emeraldLight: "#0D6B4A",
    gold: "#D4AF37",
    goldLight: "#F3E5AB",
    darkBg: "#060A08",
    cardBg: "rgba(13, 22, 18, 0.75)",
    textWhite: "#F0F6FC",
    textMuted: "#8B949E",
    borderGlass: "rgba(212, 175, 55, 0.25)",
  },
  typography: {
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Helvetica Neue', Arial, sans-serif",
    headlineWeight: 800,
    bodyWeight: 500,
  },
  springs: {
    snappy: { damping: 15, mass: 0.8, stiffness: 120 },
    gentle: { damping: 20, mass: 1.2, stiffness: 80 },
    cinematic: { damping: 28, mass: 2.0, stiffness: 60 },
  },
};
