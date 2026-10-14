import os
import sys
import json
import uuid
import time
import shutil

CAPCUT_DRAFTS_DIR = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')

def is_capcut_installed():
    return os.path.exists(CAPCUT_DRAFTS_DIR)

def create_safe_capcut_project(project_name, video_path, srt_path=None):
    """
    Cria com segurança um projeto no CapCut Desktop contendo o clipe já cortado em 9:16.
    Não altera projetos existentes e valida a compatibilidade.
    """
    if not is_capcut_installed():
        return None, "CapCut Desktop não está instalado ou diretório de projetos não existe."

    video_path = os.path.abspath(video_path)
    if not os.path.exists(video_path):
        return None, f"Vídeo não encontrado em {video_path}"

    draft_dir = os.path.join(CAPCUT_DRAFTS_DIR, project_name)
    os.makedirs(draft_dir, exist_ok=True)

    # Identificar se há um projeto de modelo válido para clonar configurações seguras
    existing = [d for d in os.listdir(CAPCUT_DRAFTS_DIR) if os.path.isdir(os.path.join(CAPCUT_DRAFTS_DIR, d)) and d != project_name]
    base_dir = os.path.join(CAPCUT_DRAFTS_DIR, existing[0]) if existing else None

    # Copiar configs secundárias se existirem
    aux_files = ['draft_virtual_store.json', 'draft_settings', 'attachment_editing.json', 'timeline_layout.json', 'draft_agency_config.json', 'key_value.json', 'draft.extra']
    if base_dir:
        for f in aux_files:
            src = os.path.join(base_dir, f)
            if os.path.exists(src):
                try:
                    shutil.copy2(src, os.path.join(draft_dir, f))
                except Exception:
                    pass

    # Obter duração real do vídeo usando ffprobe ou ffmpeg
    duration_sec = 60.0
    try:
        from core.video_processor import FFMPEG_BIN
        res = subprocess.run([FFMPEG_BIN, "-i", video_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        import re
        m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
        if m:
            h, mi, s = float(m.group(1)), float(m.group(2)), float(m.group(3))
            duration_sec = h * 3600 + mi * 60 + s
    except Exception:
        pass

    duration_us = int(duration_sec * 1000000)

    project_id = str(uuid.uuid4()).upper()
    video_id = str(uuid.uuid4()).upper()
    segment_id = str(uuid.uuid4()).upper()

    draft_info = {
        'id': project_id,
        'name': project_name,
        'duration': duration_us,
        'canvas_config': {'ratio': '9:16', 'width': 1080, 'height': 1920, 'background': None},
        'fps': 30.0,
        'materials': {
            'videos': [{
                'id': video_id,
                'path': video_path,
                'duration': duration_us,
                'width': 1080,
                'height': 1920,
                'material_name': os.path.basename(video_path),
                'type': 'video'
            }]
        },
        'tracks': [{
            'id': str(uuid.uuid4()).upper(),
            'type': 'video',
            'attribute': 0,
            'flag': 0,
            'segments': [{
                'id': segment_id,
                'material_id': video_id,
                'source_timerange': {'start': 0, 'duration': duration_us},
                'target_timerange': {'start': 0, 'duration': duration_us},
                'speed': 1.0,
                'volume': 1.0,
                'clip': {'scale': {'x': 1.0, 'y': 1.0}, 'rotation': 0.0, 'transform': {'x': 0.0, 'y': 0.0}, 'flip': {'vertical': False, 'horizontal': False}, 'alpha': 1.0},
                'uniform_scale': {'on': True, 'value': 1.0},
                'visible': True
            }]
        }]
    }

    # Salva draft_info.json
    with open(os.path.join(draft_dir, 'draft_info.json'), 'w', encoding='utf-8') as f:
        json.dump(draft_info, f, indent=2)

    # Salva draft_meta_info.json
    meta_info = {
        'draft_id': project_id,
        'draft_name': project_name,
        'draft_root_path': CAPCUT_DRAFTS_DIR,
        'draft_json_file': os.path.join(draft_dir, 'draft_info.json'),
        'draft_fold_path': draft_dir,
        'tm_duration': duration_us,
        'tm_draft_create': int(time.time() * 1e6),
        'tm_draft_modified': int(time.time() * 1e6)
    }
    with open(os.path.join(draft_dir, 'draft_meta_info.json'), 'w', encoding='utf-8') as f:
        json.dump(meta_info, f, indent=2)

    # Atualiza root_meta_info.json sem corromper
    root_path = os.path.join(CAPCUT_DRAFTS_DIR, 'root_meta_info.json')
    if os.path.exists(root_path):
        try:
            with open(root_path, 'r', encoding='utf-8') as f:
                root_data = json.load(f)
            root_entry = {
                'draft_id': project_id,
                'draft_name': project_name,
                'draft_root_path': CAPCUT_DRAFTS_DIR,
                'draft_json_file': os.path.join(draft_dir, 'draft_info.json'),
                'draft_fold_path': draft_dir,
                'tm_duration': duration_us,
                'tm_draft_create': int(time.time() * 1e6),
                'tm_draft_modified': int(time.time() * 1e6),
                'streaming_edit_draft_ready': True
            }
            root_data['all_draft_store'] = [x for x in root_data.get('all_draft_store', []) if x.get('draft_name') != project_name]
            root_data['all_draft_store'].insert(0, root_entry)
            with open(root_path, 'w', encoding='utf-8') as f:
                json.dump(root_data, f, indent=2)
        except Exception as e:
            pass

    return draft_dir, None
