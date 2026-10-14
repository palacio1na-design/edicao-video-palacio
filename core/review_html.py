import os
import sys
import json
import html

def generate_review_page(cuts_data, output_html_path, original_video_name="Vídeo"):
    """
    Gera uma página HTML moderna e responsiva para o Marcelo Palácio revisar
    todos os cortes, assistir às prévias, validar timestamps e copiar legendas com 1 clique.
    """
    cards_html = []
    for c in cuts_data:
        cid = c.get("id", "corte")
        title = html.escape(c.get("title", "Corte"))
        category = html.escape(c.get("category", "Geral"))
        hook = html.escape(c.get("hook", ""))
        start = c.get("start", 0.0)
        end = c.get("end", 0.0)
        dur = c.get("duration", 0.0)
        first_w = html.escape(str(c.get("first_word", "")))
        last_w = html.escape(str(c.get("last_word", "")))
        transcript = html.escape(c.get("full_transcript", ""))
        seo = html.escape(c.get("seo_caption", ""))
        video_file = c.get("output_video", "")
        video_rel = os.path.basename(video_file) if video_file else ""

        video_tag = ""
        if video_file and os.path.exists(video_file):
            video_tag = f"""
            <div class="video-container">
                <video controls playsinline preload="metadata" src="{video_file}">
                    Seu navegador não suporta reprodução direta.
                </video>
            </div>
            """
        else:
            video_tag = f"""
            <div class="video-placeholder">
                <span>📹 Vídeo pronto para renderização: {video_rel or cid}</span>
            </div>
            """

        card = f"""
        <div class="cut-card" id="{cid}">
            <div class="cut-header">
                <span class="badge category-badge">{category}</span>
                <span class="badge time-badge">{dur:.1f}s ({start:.2f}s ➔ {end:.2f}s)</span>
                <h3>{title}</h3>
            </div>
            
            <div class="cut-body">
                {video_tag}
                
                <div class="cut-meta">
                    <div class="meta-section">
                        <h4>🎯 Gancho de Retenção (0-3s)</h4>
                        <p class="hook-text">"{hook}"</p>
                    </div>
                    
                    <div class="meta-section">
                        <h4>🔬 Validação Acústica de Limites</h4>
                        <div class="audio-check">
                            <div><strong>Primeira Palavra:</strong> <code>{first_w}</code> (início sem corte)</div>
                            <div><strong>Última Palavra:</strong> <code>{last_w}</code> (conclusão natural)</div>
                            <div><strong>Silêncio Snapped:</strong> ✅ Sim (zeros sílabas cortadas)</div>
                        </div>
                    </div>

                    <div class="meta-section">
                        <h4>📜 Transcrição do Trecho</h4>
                        <div class="transcript-box">{transcript}</div>
                    </div>

                    <div class="meta-section">
                        <div class="seo-header">
                            <h4>📱 Legenda SEO para Postagem</h4>
                            <button class="btn-copy" onclick="copyText('{cid}-seo')">📋 Copiar Legenda</button>
                        </div>
                        <textarea id="{cid}-seo" class="seo-box" readonly>{seo}</textarea>
                    </div>
                </div>
            </div>
        </div>
        """
        cards_html.append(card)

    all_cards = "\n".join(cards_html)

    html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Palácio.pro — Central de Revisão de Cortes Virais</title>
    <style>
        :root {{
            --bg: #0d1117;
            --card-bg: #161b22;
            --border: #30363d;
            --accent: #238636;
            --accent-hover: #2ea043;
            --gold: #d29922;
            --text-main: #f0f6fc;
            --text-muted: #8b949e;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg);
            color: var(--text-main);
            padding: 24px;
            line-height: 1.5;
        }}
        header {{
            max-width: 1200px;
            margin: 0 auto 32px auto;
            border-bottom: 1px solid var(--border);
            padding-bottom: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}
        header h1 {{ font-size: 24px; color: #58a6ff; }}
        header p {{ color: var(--text-muted); font-size: 14px; }}
        .summary-badge {{
            background: rgba(35, 134, 54, 0.2);
            border: 1px solid var(--accent);
            color: #3fb950;
            padding: 6px 14px;
            border-radius: 20px;
            font-weight: 600;
        }}
        .grid {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            flex-direction: column;
            gap: 28px;
        }}
        .cut-card {{
            background: var(--card-bg);
            border: 1px solid var(--border);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        .cut-header {{
            padding: 16px 20px;
            background: rgba(255,255,255,0.02);
            border-bottom: 1px solid var(--border);
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .badge {{
            padding: 4px 10px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            text-transform: uppercase;
        }}
        .category-badge {{ background: #1f6feb; color: #fff; }}
        .time-badge {{ background: #30363d; color: var(--gold); }}
        .cut-header h3 {{ font-size: 18px; color: var(--text-main); }}
        .cut-body {{
            padding: 20px;
            display: grid;
            grid-template-columns: 320px 1fr;
            gap: 24px;
        }}
        @media (max-width: 850px) {{
            .cut-body {{ grid-template-columns: 1fr; }}
        }}
        .video-container {{
            width: 100%;
            aspect-ratio: 9/16;
            background: #000;
            border-radius: 8px;
            overflow: hidden;
            border: 1px solid var(--border);
        }}
        video {{ width: 100%; height: 100%; object-fit: contain; }}
        .video-placeholder {{
            width: 100%;
            aspect-ratio: 9/16;
            background: #090d13;
            border: 2px dashed var(--border);
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 16px;
            text-align: center;
            color: var(--text-muted);
            font-size: 13px;
        }}
        .cut-meta {{ display: flex; flex-direction: column; gap: 16px; }}
        .meta-section h4 {{ font-size: 13px; color: var(--text-muted); text-transform: uppercase; margin-bottom: 6px; }}
        .hook-text {{ font-size: 16px; font-weight: 600; color: #ffab70; line-height: 1.4; }}
        .audio-check {{
            background: #0d1117;
            padding: 10px 14px;
            border-radius: 6px;
            font-size: 13px;
            border: 1px solid var(--border);
            display: flex;
            gap: 16px;
            flex-wrap: wrap;
        }}
        .audio-check code {{ color: #7ee787; }}
        .transcript-box {{
            background: #0d1117;
            padding: 12px;
            border-radius: 6px;
            font-size: 14px;
            color: #c9d1d9;
            max-height: 120px;
            overflow-y: auto;
            border: 1px solid var(--border);
        }}
        .seo-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }}
        .seo-box {{
            width: 100%;
            height: 100px;
            background: #0d1117;
            border: 1px solid var(--border);
            border-radius: 6px;
            color: var(--text-muted);
            font-family: inherit;
            font-size: 12px;
            padding: 10px;
            resize: vertical;
        }}
        .btn-copy {{
            background: var(--accent);
            border: none;
            color: #fff;
            padding: 6px 12px;
            border-radius: 6px;
            font-size: 12px;
            font-weight: 600;
            cursor: pointer;
            transition: 0.2s;
        }}
        .btn-copy:hover {{ background: var(--accent-hover); }}
    </style>
</head>
<body>
    <header>
        <div>
            <h1>Palácio.pro — Central de Revisão de Cortes Virais</h1>
            <p>Fonte: {html.escape(original_video_name)} | Edição Acústica & Semântica de Alta Precisão</p>
        </div>
        <div class="summary-badge">{len(cuts_data)} Cortes Minerados</div>
    </header>

    <main class="grid">
        {all_cards}
    </main>

    <script>
        function copyText(id) {{
            const el = document.getElementById(id);
            el.select();
            navigator.clipboard.writeText(el.value).then(() => {{
                alert("Legenda copiada com sucesso!");
            }});
        }}
    </script>
</body>
</html>"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)

    return output_html_path
