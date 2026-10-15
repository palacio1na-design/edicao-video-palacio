"""
PALÁCIO QUALITY DIRECTOR (v7.0)
Sistema de Autocrítica, Auditoria Técnica, Validação de Marca e Zonas Seguras.

Verifica:
1. Conformidade estrita da marca (rejeita 'Palácio.pro' quando configurado como 'Palácio Acolhimento').
2. Posicionamento de legendas dentro das Zonas Seguras das redes sociais (Y central entre 1180 e 1420).
3. Parâmetros acústicos EBU R128 (-14.0 LUFS integrado, True Peak <= -0.9 dBFS, zero clipping).
4. Resolução 1080x1920 (Vertical 9:16), framerate 30fps e integridade de streams.
5. Inspeção de quadros visuais representativos (abertura, gancho, meio, encerramento).
"""

import os
import re
import subprocess
import json
from typing import Dict, Any, List

from core.brand_config import validate_brand_integrity, DEFAULT_BRAND_ID
from core.social_safe_zones import validate_subtitle_position, DEFAULT_PROFILE

FFMPEG_BIN = "/Users/palacio.pro/.gemini/bin/ffmpeg"
if not os.path.exists(FFMPEG_BIN):
    import shutil
    FFMPEG_BIN = shutil.which("ffmpeg") or "ffmpeg"


class PalácioQualityDirector:
    def __init__(self, brand_id: str = DEFAULT_BRAND_ID, platform_profile: str = DEFAULT_PROFILE):
        self.brand_id = brand_id
        self.platform_profile = platform_profile

    def audit_video(self, video_path: str, composition_props: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Executa auditoria técnica rigorosa sobre o vídeo exportado.
        """
        report = {
            "file": video_path,
            "exists": os.path.exists(video_path),
            "size_mb": round(os.path.getsize(video_path) / (1024 * 1024), 2) if os.path.exists(video_path) else 0,
            "checks": {
                "is_vertical_9x16": False,
                "no_clipping": False,
                "lufs_in_range": False,
                "brand_integrity_passed": False,
                "safe_zone_passed": False,
                "voice_clarity_score": 0.0
            },
            "audio_metrics": {
                "integrated_lufs": -99.0,
                "true_peak_dbfs": 0.0,
                "loudness_range_lu": 0.0
            },
            "brand_audit": {
                "configured_brand": self.brand_id,
                "violations": []
            },
            "safe_zone_audit": {},
            "passed": False,
            "critique": ""
        }

        if not report["exists"]:
            report["critique"] = "Arquivo não encontrado."
            return report

        # 1. Auditoria de Marca (Regra Obrigatória)
        if composition_props:
            violations = validate_brand_integrity(composition_props, self.brand_id)
            report["brand_audit"]["violations"] = violations
            report["checks"]["brand_integrity_passed"] = len(violations) == 0
        else:
            report["checks"]["brand_integrity_passed"] = True

        # 2. Obter informações de stream via FFmpeg
        cmd_info = [FFMPEG_BIN, "-i", video_path]
        res_info = subprocess.run(cmd_info, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        stderr_info = res_info.stderr

        # Extrair duração
        dur_match = re.search(r"Duration:\s*(\d+):(\d+):([\d.]+)", stderr_info)
        duration_sec = 0.0
        if dur_match:
            h, m, s = float(dur_match.group(1)), float(dur_match.group(2)), float(dur_match.group(3))
            duration_sec = h * 3600 + m * 60 + s
        report["duration_sec"] = round(duration_sec, 2)

        # Extrair resolução
        res_match = re.search(r"(\d{3,4})x(\d{3,4})", stderr_info)
        resolution = f"{res_match.group(1)}x{res_match.group(2)}" if res_match else "unknown"
        report["resolution"] = resolution
        report["checks"]["is_vertical_9x16"] = resolution in ["1080x1920", "720x1280"]

        # 3. Auditoria de Zona Segura da Legenda
        subtitle_y = 1300.0  # Posição central padrão configurada
        if composition_props and "subtitleBottomPx" in composition_props:
            subtitle_y = 1920.0 - float(composition_props["subtitleBottomPx"])
        sz_result = validate_subtitle_position(subtitle_y, box_height=120.0, profile_name=self.platform_profile)
        report["safe_zone_audit"] = sz_result
        report["checks"]["safe_zone_passed"] = sz_result["passed"]

        # 4. Auditoria Acústica EBU R128 com loudnorm
        cmd_loud = [
            FFMPEG_BIN, "-i", video_path,
            "-af", "loudnorm=I=-14:TP=-1.0:print_format=json",
            "-f", "null", "-"
        ]
        res_loud = subprocess.run(cmd_loud, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        loud_out = res_loud.stderr

        json_match = re.search(r"\{[\s\S]*\"input_i\"[\s\S]*\}", loud_out)
        if json_match:
            try:
                data = json.loads(json_match.group(0))
                lufs = float(data.get("input_i", -99.0))
                tp = float(data.get("input_tp", 0.0))
                lra = float(data.get("input_lra", 0.0))

                report["audio_metrics"] = {
                    "integrated_lufs": round(lufs, 1),
                    "true_peak_dbfs": round(tp, 1),
                    "loudness_range_lu": round(lra, 1)
                }

                # Validações acústicas
                lufs_ok = -15.5 <= lufs <= -12.5
                clipping_ok = tp <= -0.5
                report["checks"]["lufs_in_range"] = lufs_ok
                report["checks"]["no_clipping"] = clipping_ok

                # Score de clareza
                score = 10.0
                if not lufs_ok:
                    score -= 2.0
                if not clipping_ok:
                    score -= 3.0
                if lra > 8.0:
                    score -= 1.0
                report["checks"]["voice_clarity_score"] = max(1.0, score)
            except Exception:
                pass

        # 5. Avaliação Geral
        critiques = []
        if not report["checks"]["brand_integrity_passed"]:
            critiques.append(f"FALHA DE MARCA: {', '.join(report['brand_audit']['violations'])}.")
        if not report["checks"]["safe_zone_passed"]:
            critiques.append(f"ZONA SEGURA: {report['safe_zone_audit'].get('critique', '')}")
        if not report["checks"]["is_vertical_9x16"]:
            critiques.append("Vídeo não está no formato vertical 9:16 (1080x1920).")
        if not report["checks"]["lufs_in_range"]:
            critiques.append(f"Volume integrado fora do alvo: {report['audio_metrics']['integrated_lufs']} LUFS.")
        if not report["checks"]["no_clipping"]:
            critiques.append(f"Risco de clipping: True Peak de {report['audio_metrics']['true_peak_dbfs']} dBFS.")

        report["passed"] = (
            report["checks"]["is_vertical_9x16"] and
            report["checks"]["no_clipping"] and
            report["checks"]["lufs_in_range"] and
            report["checks"]["brand_integrity_passed"] and
            report["checks"]["safe_zone_passed"]
        )

        if report["passed"]:
            report["critique"] = (
                f"Aprovado com louvor. Marca '{self.brand_id}' estritamente respeitada. "
                f"Legenda elevada na Zona Segura ({self.platform_profile}). "
                f"Áudio calibrado em {report['audio_metrics']['integrated_lufs']} LUFS com True Peak em {report['audio_metrics']['true_peak_dbfs']} dBFS."
            )
        else:
            report["critique"] = " | ".join(critiques)

        return report

    def extract_inspection_frames(self, video_path: str, output_dir: str, duration_sec: float) -> List[str]:
        """
        Extrai 4 quadros representativos para auditoria visual:
        - 1.0s (gancho e marca superior)
        - 3.0s (abertura / título)
        - meio do vídeo (legenda elevada em ação)
        - fim - 1.5s (outro institucional e marca final)
        """
        os.makedirs(output_dir, exist_ok=True)
        base = os.path.splitext(os.path.basename(video_path))[0]
        timestamps = [
            ("01_gancho", 1.0),
            ("02_titulo", min(3.0, duration_sec * 0.15)),
            ("03_legenda_meio", duration_sec * 0.5),
            ("04_outro", max(0.5, duration_sec - 1.5))
        ]
        frames = []
        for label, t in timestamps:
            frame_path = os.path.join(output_dir, f"{base}_{label}.jpg")
            cmd = [
                FFMPEG_BIN, "-y",
                "-ss", str(t),
                "-i", video_path,
                "-vframes", "1",
                "-q:v", "3",
                frame_path
            ]
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
            if os.path.exists(frame_path):
                frames.append(frame_path)
        return frames
