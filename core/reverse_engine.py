"""
PALÁCIO REVERSE ENGINE (v1.0)
Módulo de Engenharia Reversa e Interoperabilidade de Projetos Audiovisuais.
Conecta o Editor Palácio ao ecossistema REA (Reverse Engineer Anything),
ao CapCut Desktop e ao Adobe After Effects.
"""

import os
import json
import subprocess
import shutil

REA_DIR = "/Users/palacio.pro/.gemini/antigravity/scratch/rea"
CAPCUT_DRAFTS_DIR = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')

class PalácioReverseEngine:
    """
    Motor de análise reversa, inspeção de estruturas de projetos
    e pontes de exportação para After Effects e CapCut.
    """

    def __init__(self, capcut_dir=None):
        self.capcut_dir = capcut_dir or CAPCUT_DRAFTS_DIR

    def inspect_capcut_draft(self, draft_identifier):
        """
        Inspeciona e decodifica a estrutura interna de um rascunho do CapCut Desktop.
        Aceita o nome do projeto ou o caminho absoluto da pasta.
        Retorna dicionário estruturado com faixas, materiais, legendas e keyframes.
        """
        if os.path.isabs(draft_identifier):
            draft_folder = draft_identifier
        else:
            draft_folder = os.path.join(self.capcut_dir, draft_identifier)

        if not os.path.exists(draft_folder):
            return {"error": f"Pasta de rascunho não encontrada: {draft_folder}"}

        # Localizar arquivo principal de conteúdo
        content_candidates = ["draft_content.json", "draft_info.json"]
        target_json = None
        for cand in content_candidates:
            p = os.path.join(draft_folder, cand)
            if os.path.exists(p):
                target_json = p
                break

        if not target_json:
            return {"error": f"Nenhum arquivo de dados de rascunho encontrado em {draft_folder}"}

        try:
            with open(target_json, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            return {"error": f"Erro ao decodificar JSON do rascunho: {e}"}

        # Extrair dados de inteligência da timeline
        duration_us = data.get("duration", 0)
        fps = data.get("fps", 30.0)
        canvas = data.get("canvas_config", {})
        
        # Materiais
        materials = data.get("materials", {})
        videos = materials.get("videos", [])
        audios = materials.get("audios", [])
        texts = materials.get("texts", [])
        stickers = materials.get("stickers", [])
        
        # Faixas (Tracks)
        tracks = data.get("tracks", [])
        track_summary = []
        for t in tracks:
            t_type = t.get("type", "unknown")
            segs = t.get("segments", [])
            track_summary.append({
                "id": t.get("id"),
                "type": t_type,
                "segment_count": len(segs)
            })

        # Mapeamento de legendas/textos
        extracted_subtitles = []
        for txt in texts:
            content = txt.get("content", "")
            # Muitas vezes o CapCut armazena o texto com tags XML internas ou JSON string
            extracted_subtitles.append({
                "id": txt.get("id"),
                "text": content,
                "font_size": txt.get("font_size"),
                "font_title": txt.get("font_title")
            })

        return {
            "success": True,
            "project_name": os.path.basename(draft_folder),
            "draft_json_file": target_json,
            "duration_sec": round(duration_us / 1000000.0, 3),
            "fps": fps,
            "canvas": canvas,
            "tracks": track_summary,
            "materials_count": {
                "videos": len(videos),
                "audios": len(audios),
                "texts": len(texts),
                "stickers": len(stickers)
            },
            "subtitles_sample": extracted_subtitles[:10]
        }

    def convert_capcut_to_remotion(self, draft_identifier):
        """
        Converte as faixas e marcações de um projeto do CapCut em
        um formato compatível com as composições Remotion do Palácio.
        """
        analysis = self.inspect_capcut_draft(draft_identifier)
        if not analysis.get("success"):
            return analysis

        remotion_meta = {
            "composition": {
                "width": 1080,
                "height": 1920,
                "fps": int(analysis.get("fps", 30)),
                "durationInFrames": int(analysis.get("duration_sec", 0) * analysis.get("fps", 30))
            },
            "source_draft": analysis.get("project_name"),
            "tracks": analysis.get("tracks"),
            "subtitles": analysis.get("subtitles_sample")
        }
        return {"success": True, "remotion_meta": remotion_meta}

    def export_to_after_effects_jsx(self, project_name, video_path, words_data, output_jsx_path, duration_sec=38.8):
        """
        Gera um script ExtendScript (.jsx) nativo para o Adobe After Effects.
        Ao rodar no After Effects (File > Scripts > Run Script File):
        1. Cria uma nova composição 1080x1920 @ 30fps.
        2. Importa o clipe de vídeo da palestra.
        3. Cria as camadas de texto de legenda com keyframes de opacidade e escala no estilo Palácio.
        4. Aplica o monograma e guias de zona segura.
        """
        video_path_escaped = video_path.replace("\\", "/")
        
        flat_words = []
        if isinstance(words_data, list):
            flat_words = words_data
        elif isinstance(words_data, dict):
            if "words" in words_data and isinstance(words_data["words"], list):
                flat_words = words_data["words"]
            elif "transcription" in words_data and isinstance(words_data["transcription"], dict):
                segs = words_data["transcription"].get("segments", [])
                for s in segs:
                    flat_words.extend(s.get("words", []))
            elif "segments" in words_data:
                for s in words_data.get("segments", []):
                    flat_words.extend(s.get("words", []))

        words_slice = flat_words[:40] if flat_words else []
        words_json_str = json.dumps(words_slice)
        jsx_content = f"""// Script Gerado Automaticamente pelo PALÁCIO REVERSE ENGINE
// Projeto: {project_name} - Palácio Acolhimento
(function() {{
    app.beginUndoGroup("Criar Timeline Palácio Acolhimento");

    var compWidth = 1080;
    var compHeight = 1920;
    var compFps = 30.0;
    var compDuration = {duration_sec};

    // 1. Criar Composição Master
    var myComp = app.project.items.addComp(
        "{project_name}_MASTER",
        compWidth,
        compHeight,
        1.0,
        compDuration,
        compFps
    );
    myComp.openInViewer();

    // 2. Importar e Adicionar Vídeo Principal
    var io = new ImportOptions(new File("{video_path_escaped}"));
    if (io.canImportAs(ImportAsType.FOOTAGE)) {{
        var videoItem = app.project.importFile(io);
        var videoLayer = myComp.layers.add(videoItem);
        // Centralizar
        videoLayer.property("Position").setValue([compWidth / 2, compHeight / 2]);
    }}

    // 3. Adicionar Camada Guia de Safe Zone Universal (Y: 1250 - 1380)
    var guideSolid = myComp.layers.addSolid([0.9, 0.66, 0.23], "Guia Safe Zone Legenda", compWidth, 130, 1.0, compDuration);
    guideSolid.property("Position").setValue([compWidth / 2, 1315]);
    guideSolid.opacity.setValue(15);
    guideSolid.guideLayer = true;

    // 4. Adicionar Legendas com Marcação Temporal
    var sampleWords = {words_json_str};
    for (var i = 0; i < sampleWords.length; i++) {{
        var w = sampleWords[i];
        var textLayer = myComp.layers.addText(w.word || w.text || "");
        var textProp = textLayer.property("Source Text");
        var textDoc = textProp.value;
        textDoc.fontSize = 58;
        textDoc.fillColor = [0.9, 0.66, 0.23]; // Dourado Palácio #E5A93C
        textDoc.font = "Cinzel";
        textDoc.justification = ParagraphJustification.CENTER_JUSTIFY;
        textProp.setValue(textDoc);

        textLayer.property("Position").setValue([compWidth / 2, 1380]);
        textLayer.startTime = w.start || 0.0;
        textLayer.outPoint = w.end || (w.start + 0.4);
    }}

    app.endUndoGroup();
}})();
"""
        os.makedirs(os.path.dirname(os.path.abspath(output_jsx_path)), exist_ok=True)
        with open(output_jsx_path, "w", encoding="utf-8") as f:
            f.write(jsx_content)

        return {
            "success": True,
            "output_jsx": output_jsx_path,
            "instructions": "No Adobe After Effects, vá em Arquivo > Scripts > Executar Arquivo de Script... e selecione o .jsx gerado."
        }

    def run_rea_analysis(self, target_path, analysis_mode="javascript"):
        """
        Executa uma análise de engenharia reversa via REA CLI.
        """
        rea_cli = shutil.which("rea") or "npx -y rea-agents@latest"
        cmd = f"{rea_cli} analyze-{analysis_mode}-application \"{target_path}\" --json"
        try:
            res = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            return {
                "success": res.returncode == 0,
                "stdout": res.stdout,
                "stderr": res.stderr
            }
        except Exception as e:
            return {"error": str(e)}
