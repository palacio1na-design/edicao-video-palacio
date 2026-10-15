/**
 * PALÁCIO BRAND CONFIGURATION (v7.0)
 * Configuração Central Obrigatória da Identidade Audiovisual em TypeScript.
 *
 * REGRA INEGOCIÁVEL:
 * A marca principal é PALÁCIO ACOLHIMENTO.
 * Palácio.pro é proibido como assinatura, badge ou marca visual nos vídeos.
 */

export interface BrandConfig {
  brandId: string;
  brandName: string;
  brandDisplay: string;
  brandMode: "default" | "health";
  handle: string;
  website: string;
  slogan: string;
  subtext: string;
  monogram: string;
  colors: {
    primary: string;
    primaryLight: string;
    gold: string;
    goldLight: string;
    darkBg: string;
    textWhite: string;
  };
  forbiddenSignatures: string[];
}

export const PALACIO_ACOLHIMENTO_BRAND: BrandConfig = {
  brandId: "palacio-acolhimento",
  brandName: "Palácio Acolhimento",
  brandDisplay: "PALÁCIO ACOLHIMENTO",
  brandMode: "default",
  handle: "@palacioacolhimento",
  website: "palacioacolhimento.com.br",
  slogan: "A recuperação continua na forma de viver.",
  subtext: "Acolhimento Familiar & Tratamento Humanizado",
  monogram: "P",
  colors: {
    primary: "#074B32",
    primaryLight: "#0D6B4A",
    gold: "#D4AF37",
    goldLight: "#F3E5AB",
    darkBg: "#060A08",
    textWhite: "#FFFFFF",
  },
  forbiddenSignatures: [
    "palácio.pro",
    "palacio.pro",
    "palácio ponto pro",
    "palacio ponto pro",
    "palácio ai",
    "palacio ai",
    "@palacio.pro",
    "@palacio_pro",
  ],
};

export const MAIS_UM_PASSO_BRAND: BrandConfig = {
  brandId: "mais-um-passo-saude",
  brandName: "+1 Passo Saúde",
  brandDisplay: "+1 PASSO SAÚDE",
  brandMode: "health",
  handle: "@maisumpassosaude",
  website: "maisumpassosaude.com.br",
  slogan: "Cuidando de cada passo da sua saúde.",
  subtext: "Saúde Integrativa & Prevenção",
  monogram: "+1",
  colors: {
    primary: "#1E3A8A",
    primaryLight: "#3B82F6",
    gold: "#10B981",
    goldLight: "#6EE7B7",
    darkBg: "#050B14",
    textWhite: "#FFFFFF",
  },
  forbiddenSignatures: [
    "palácio.pro",
    "palacio.pro",
    "palácio ai",
    "@palacio.pro",
  ],
};

export function getBrandConfig(brandId: string = "palacio-acolhimento"): BrandConfig {
  if (brandId === "mais-um-passo-saude") {
    return MAIS_UM_PASSO_BRAND;
  }
  return PALACIO_ACOLHIMENTO_BRAND;
}

/**
 * Validação rigorosa em runtime de marca.
 * Lança erro ou retorna false se alguma assinatura proibida for detectada.
 */
export function validateBrandIntegrity(
  props: Record<string, any>,
  brandConfig: BrandConfig = PALACIO_ACOLHIMENTO_BRAND,
): { valid: boolean; violations: string[] } {
  const violations: string[] = [];
  const forbidden = brandConfig.forbiddenSignatures;

  function scan(val: any, path: string) {
    if (typeof val === "string") {
      const lower = val.toLowerCase();
      for (const f of forbidden) {
        if (lower.includes(f)) {
          violations.push(
            `Violação de marca em '${path}': termo proibido '${f}' encontrado no texto '${val}'`,
          );
        }
      }
    } else if (typeof val === "object" && val !== null) {
      for (const [k, v] of Object.entries(val)) {
        if (k === "forbiddenSignatures" || k === "forbidden_signatures") {
          continue;
        }
        scan(v, `${path}.${k}`);
      }
    }
  }

  scan(props, "props");
  return {
    valid: violations.length === 0,
    violations,
  };
}
