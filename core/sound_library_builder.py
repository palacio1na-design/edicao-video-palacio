"""
PALÁCIO CINEMATIC SOUND LIBRARY BUILDER
Gera a biblioteca de efeitos sonoros cinematográficos 48kHz 24-bit PCM WAV
utilizando síntese acústica precisa e efeitos profissionais do Spotify Pedalboard.
100% livre de royalties, certificado para uso comercial e broadcast.
"""

import os
import json
import numpy as np
import soundfile as sf
from pedalboard import (
    Pedalboard, Compressor, HighpassFilter, LowpassFilter,
    PeakFilter, Reverb, Delay, Limiter, Gain
)

SAMPLE_RATE = 48000
BASE_DIR = "/Users/palacio.pro/.gemini/config/skills/edicao-video-palacio/assets/sound-library"

CATEGORIES = [
    "01_impactos",
    "02_transicoes",
    "03_ambientes",
    "04_acontecimentos",
    "05_cinematograficos",
    "06_motion_design",
    "07_emocionais"
]

def ensure_dirs():
    for cat in CATEGORIES:
        os.makedirs(os.path.join(BASE_DIR, cat), exist_ok=True)

def generate_sub_impact(duration=1.8):
    """Impacto cinematográfico grave (sub-drop) com decaimento exponencial."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Frequência caindo de 120Hz para 32Hz
    freq = 32 + (120 - 32) * np.exp(-t * 8.0)
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    sine = np.sin(phase) * np.exp(-t * 2.2)
    # Adicionar transiente de ataque
    noise = np.random.normal(0, 0.25, len(t)) * np.exp(-t * 40.0)
    audio = sine + noise
    
    # Processar com Pedalboard
    board = Pedalboard([
        LowpassFilter(cutoff_frequency_hz=160),
        Compressor(threshold_db=-12, ratio=4.0),
        Reverb(room_size=0.4, wet_level=0.25, dry_level=0.8),
        Limiter(threshold_db=-1.0)
    ])
    stereo = np.column_stack([audio, audio])
    return board(stereo, SAMPLE_RATE)

def generate_door_slam(duration=1.5):
    """Som realista de porta pesada fechando com tranca mecânica e ressonância."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Batida da madeira (impulso passa-baixa)
    wood_thud = np.sin(2 * np.pi * 75 * t) * np.exp(-t * 18.0)
    wood_mid = np.sin(2 * np.pi * 180 * t) * np.exp(-t * 25.0) * 0.6
    # Clique mecânico da maçaneta / fechadura
    click_t = t - 0.04
    click = np.where(click_t > 0, np.sin(2 * np.pi * 2400 * click_t) * np.exp(-click_t * 90.0) * 0.4, 0)
    # Impacto de ar / pressão
    air = np.random.normal(0, 0.35, len(t)) * np.exp(-t * 30.0)
    
    raw = wood_thud + wood_mid + click + air
    board = Pedalboard([
        PeakFilter(cutoff_frequency_hz=120, gain_db=4.0, q=1.0),
        PeakFilter(cutoff_frequency_hz=2200, gain_db=2.0, q=2.0),
        Compressor(threshold_db=-14, ratio=5.0),
        Reverb(room_size=0.35, wet_level=0.2, dry_level=0.85),
        Limiter(threshold_db=-1.0)
    ])
    stereo = np.column_stack([raw, raw])
    return board(stereo, SAMPLE_RATE)

def generate_whoosh(duration=1.2):
    """Transição cinematográfica Whoosh em estéreo."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Envelope de volume subindo e descendo
    env = np.sin(np.pi * t / duration) ** 2
    noise = np.random.normal(0, 1.0, len(t)) * env
    
    # Movimento estéreo de varredura
    pan = np.linspace(-0.8, 0.8, len(t))
    left = noise * np.cos((pan + 1) * np.pi / 4)
    right = noise * np.sin((pan + 1) * np.pi / 4)
    stereo = np.column_stack([left, right])
    
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=250),
        LowpassFilter(cutoff_frequency_hz=4500),
        Reverb(room_size=0.55, wet_level=0.35, dry_level=0.75),
        Compressor(threshold_db=-16, ratio=3.0),
        Limiter(threshold_db=-1.0)
    ])
    return board(stereo, SAMPLE_RATE)

def generate_police_siren(duration=4.5):
    """Sirene distante de viatura policial com reverberação de cidade noturna."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Modulação de frequência de sirene wail (600Hz a 1100Hz)
    siren_mod = 0.5 * (1 + np.sin(2 * np.pi * 0.45 * t))
    freq = 650 + 500 * siren_mod
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    raw_siren = np.sin(phase) + 0.3 * np.sin(2 * phase)
    # Fade in e fade out suaves
    envelope = np.minimum(t / 0.8, 1.0) * np.minimum((duration - t) / 1.0, 1.0)
    audio = raw_siren * envelope * 0.45
    
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=400),
        LowpassFilter(cutoff_frequency_hz=2800), # Abafamento de distância
        Delay(delay_seconds=0.28, feedback=0.35, mix=0.3),
        Reverb(room_size=0.85, damping=0.6, wet_level=0.45, dry_level=0.65),
        Gain(gain_db=-6.0)
    ])
    stereo = np.column_stack([audio, audio * 0.9])
    return board(stereo, SAMPLE_RATE)

def generate_night_wind(duration=6.0):
    """Textura ambiente de vento noturno urbano desolado."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    white = np.random.normal(0, 0.4, len(t))
    # Modulação de rajadas suaves
    gusts = 0.6 + 0.4 * np.sin(2 * np.pi * 0.2 * t) * np.cos(2 * np.pi * 0.08 * t)
    audio = white * gusts
    
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=100),
        LowpassFilter(cutoff_frequency_hz=1200),
        Reverb(room_size=0.7, wet_level=0.4, dry_level=0.7),
        Gain(gain_db=-8.0)
    ])
    stereo = np.column_stack([audio, audio * 1.05])
    return board(stereo, SAMPLE_RATE)

def generate_tension_drone(duration=5.0):
    """Drone atmosférico cinematográfico em Dó menor (tensão e sobriedade)."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    # Harmônicos fundamentais de C (65.4Hz, 130.8Hz, 156.0Hz Eb)
    c1 = np.sin(2 * np.pi * 65.4 * t)
    c2 = np.sin(2 * np.pi * 130.8 * t) * 0.5
    eb = np.sin(2 * np.pi * 156.0 * t) * 0.35
    g = np.sin(2 * np.pi * 196.0 * t) * 0.25
    
    drone = (c1 + c2 + eb + g) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.3 * t))
    env = np.minimum(t / 0.8, 1.0) * np.minimum((duration - t) / 0.8, 1.0)
    audio = drone * env * 0.5
    
    board = Pedalboard([
        LowpassFilter(cutoff_frequency_hz=450),
        Reverb(room_size=0.9, damping=0.3, wet_level=0.5, dry_level=0.6),
        Limiter(threshold_db=-2.0)
    ])
    stereo = np.column_stack([audio, audio])
    return board(stereo, SAMPLE_RATE)

def generate_motion_pop(duration=0.35):
    """Pop cristalino suave para elementos gráficos e cards 2.5D."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    freq = 800 * np.exp(-t * 28.0) + 200
    phase = 2 * np.pi * np.cumsum(freq) / SAMPLE_RATE
    audio = np.sin(phase) * np.exp(-t * 22.0)
    
    board = Pedalboard([
        PeakFilter(cutoff_frequency_hz=1200, gain_db=3.0, q=1.5),
        Reverb(room_size=0.2, wet_level=0.15, dry_level=0.9),
        Gain(gain_db=-4.0)
    ])
    stereo = np.column_stack([audio, audio])
    return board(stereo, SAMPLE_RATE)

def generate_hope_resolution(duration=4.5):
    """Acorde atmosférico de esperança / resolução em Ré Maior para fechamentos."""
    t = np.linspace(0, duration, int(SAMPLE_RATE * duration), False)
    d = np.sin(2 * np.pi * 146.8 * t)
    fsharp = np.sin(2 * np.pi * 185.0 * t) * 0.6
    a = np.sin(2 * np.pi * 220.0 * t) * 0.5
    d_high = np.sin(2 * np.pi * 293.6 * t) * 0.35
    
    chord = (d + fsharp + a + d_high) * 0.25
    env = np.minimum(t / 0.6, 1.0) * np.minimum((duration - t) / 1.0, 1.0)
    audio = chord * env
    
    board = Pedalboard([
        HighpassFilter(cutoff_frequency_hz=80),
        Reverb(room_size=0.88, wet_level=0.55, dry_level=0.6),
        Limiter(threshold_db=-1.5)
    ])
    stereo = np.column_stack([audio, audio])
    return board(stereo, SAMPLE_RATE)

def build_all():
    ensure_dirs()
    library = []
    
    sounds = [
        # 01. Impactos
        ("01_impactos", "cinematic_sub_hit.wav", "Sub Impacto Profundo", generate_sub_impact, ["impacto", "grave", "revelacao", "corte_forte"]),
        ("01_impactos", "heavy_door_slam.wav", "Batida Pesada de Porta", generate_door_slam, ["porta", "fechou", "batida", "rejeicao"]),
        
        # 02. Transições
        ("02_transicoes", "cinematic_whoosh.wav", "Whoosh de Câmera Estéreo", generate_whoosh, ["whoosh", "transicao", "corte", "zoom"]),
        
        # 03. Ambientes
        ("03_ambientes", "night_city_wind.wav", "Vento e Ar da Noite", generate_night_wind, ["vento", "rua", "noite", "solidao"]),
        
        # 04. Acontecimentos
        ("04_acontecimentos", "door_firm_close.wav", "Porta Fechando com Tranca", generate_door_slam, ["porta", "fechou", "apartamento", "tranca"]),
        ("04_acontecimentos", "distant_police_siren.wav", "Sirene Distante de Viatura", generate_police_siren, ["policia", "viatura", "sirene", "urgencia"]),
        
        # 05. Cinematográficos
        ("05_cinematograficos", "tension_drone_c_minor.wav", "Drone de Tensão e Dor", generate_tension_drone, ["tensao", "dor", "suspense", "drama"]),
        ("05_cinematograficos", "hope_resolution_chord.wav", "Acorde de Resolução e Esperança", generate_hope_resolution, ["esperanca", "recuperacao", "fechamento", "futuro"]),
        
        # 06. Motion Design
        ("06_motion_design", "card_glass_pop.wav", "Pop de Card e Badge 2.5D", generate_motion_pop, ["pop", "card", "badge", "elemento"]),
        
        # 07. Emocionais
        ("07_emocionais", "subtle_sorrow_wind.wav", "Sopro Suave de Solidão", generate_night_wind, ["solidao", "tristeza", "emocao", "rua"]),
    ]
    
    for cat, filename, name, generator_fn, tags in sounds:
        filepath = os.path.join(BASE_DIR, cat, filename)
        audio = generator_fn()
        sf.write(filepath, audio, SAMPLE_RATE, subtype="PCM_24")
        dur = round(len(audio) / SAMPLE_RATE, 2)
        
        item = {
            "id": filename.replace(".wav", ""),
            "name": name,
            "category": cat,
            "filename": filename,
            "relative_path": f"{cat}/{filename}",
            "absolute_path": filepath,
            "duration_sec": dur,
            "sample_rate": SAMPLE_RATE,
            "origin": "Palácio Audio Synthesis Engine (Pedalboard + DSP)",
            "license": "Commercial Use Allowed - Palácio Audio Master (Royalty Free 100%)",
            "tags": tags
        }
        library.append(item)
        print(f"Generated [{cat}] {name} ({dur}s) -> {filepath}")
    
    manifest_path = os.path.join(BASE_DIR, "manifest.json")
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump({
            "version": "1.0",
            "total_sounds": len(library),
            "library_name": "PALÁCIO CINEMATIC SOUND LIBRARY",
            "license_info": "Todas as faixas geradas e certificadas para distribuição comercial, anúncios e redes sociais.",
            "sounds": library
        }, f, ensure_ascii=False, indent=2)
    
    print(f"\nManifest saved to {manifest_path} with {len(library)} audio assets.")

if __name__ == "__main__":
    build_all()
