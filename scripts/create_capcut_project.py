import sys, json, os, uuid, time, shutil

if len(sys.argv) < 3:
    print("Usage: python3 create_capcut_project.py <project_name> <video_path> [cover_jpg]")
    sys.exit(1)

project_name = sys.argv[1]
video_path = os.path.abspath(sys.argv[2])
cover_path = sys.argv[3] if len(sys.argv) > 3 else None

capcut_drafts = os.path.expanduser('~/Movies/CapCut/User Data/Projects/com.lveditor.draft')
root_path = os.path.join(capcut_drafts, 'root_meta_info.json')
draft_dir = os.path.join(capcut_drafts, project_name)
os.makedirs(draft_dir, exist_ok=True)

# Find any existing project as base template
base_drafts = [d for d in os.listdir(capcut_drafts) if os.path.isdir(os.path.join(capcut_drafts, d)) and d != project_name]
base_dir = os.path.join(capcut_drafts, base_drafts[0]) if base_drafts else None

for f in ['draft_virtual_store.json', 'draft_settings', 'attachment_editing.json', 'timeline_layout.json', 'draft_agency_config.json', 'key_value.json', 'draft.extra']:
    if base_dir and os.path.exists(os.path.join(base_dir, f)):
        shutil.copy2(os.path.join(base_dir, f), os.path.join(draft_dir, f))

# cover
dest_cover = os.path.join(draft_dir, 'draft_cover.jpg')
if cover_path and os.path.exists(cover_path):
    shutil.copy2(cover_path, dest_cover)

project_id = str(uuid.uuid4()).upper()
video_id = str(uuid.uuid4()).upper()
segment_id = str(uuid.uuid4()).upper()

# estimate duration or 60s default
duration_us = 60000000

d = {
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

with open(os.path.join(draft_dir, 'draft_info.json'), 'w') as f:
    json.dump(d, f, indent=2)

with open(os.path.join(draft_dir, 'draft_meta_info.json'), 'w') as f:
    json.dump({
        'draft_id': project_id,
        'draft_name': project_name,
        'draft_root_path': capcut_drafts,
        'draft_json_file': os.path.join(draft_dir, 'draft_info.json'),
        'draft_fold_path': draft_dir,
        'tm_duration': duration_us,
        'draft_cover': dest_cover,
        'tm_draft_create': int(time.time() * 1e6),
        'tm_draft_modified': int(time.time() * 1e6)
    }, f, indent=2)

if os.path.exists(root_path):
    with open(root_path) as f:
        root_data = json.load(f)
    root_entry = {
        'draft_id': project_id,
        'draft_name': project_name,
        'draft_root_path': capcut_drafts,
        'draft_json_file': os.path.join(draft_dir, 'draft_info.json'),
        'draft_fold_path': draft_dir,
        'tm_duration': duration_us,
        'draft_cover': dest_cover,
        'tm_draft_create': int(time.time() * 1e6),
        'tm_draft_modified': int(time.time() * 1e6),
        'streaming_edit_draft_ready': True
    }
    root_data['all_draft_store'] = [x for x in root_data.get('all_draft_store', []) if x.get('draft_name') != project_name]
    root_data['all_draft_store'].insert(0, root_entry)
    with open(root_path, 'w') as f:
        json.dump(root_data, f, indent=2)

print(f"CapCut project '{project_name}' ready!")
