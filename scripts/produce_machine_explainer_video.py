#!/usr/bin/env python3
"""
Motion Video Director: System Architecture Explainer
Produces a 1080p explainer video showing how the Case Competition Machine works.
Adheres to:
- 001 Main/motion-video-director guidelines
- beats.json storyboard & audio synchronization
- Strict Anonymity Law (no machine paths or personal identities)
"""

import os
import sys
import json
import asyncio
import subprocess
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFont

VIDEO_DIR = Path("Finished Resources/09_Video")
ASSETS_DIR = VIDEO_DIR / "assets"
FRAMES_DIR = VIDEO_DIR / "frames"
OUTPUT_MP4 = VIDEO_DIR / "System_Architecture_Explainer.mp4"

# Color Palette (Dark High-Tech UI)
BG_DARK = (11, 15, 25)        # #0B0F19
SURFACE = (30, 41, 59)        # #1E293B
SURFACE_LIGHT = (51, 65, 85)  # #334155
CYAN = (14, 165, 233)         # #0EA5E9
TEAL = (16, 185, 129)         # #10B981
AMBER = (245, 158, 11)        # #F59E0B
PURPLE = (139, 92, 246)       # #8B5CF6
WHITE = (248, 250, 252)       # #F8FAFC
MUTED = (148, 163, 184)       # #94A3B8
BORDER = (71, 85, 105)        # #475569

BEATS_DATA = [
    {
        "id": "beat_01",
        "title": "THE CASE COMPETITION CHALLENGE",
        "subtitle": "Unstructured Data, Tight Deadlines, High Stakes",
        "voice_text": "In premier global case competitions, teams are handed 40-page briefs, messy spreadsheets, and brutal deadlines. Most teams scramble and present surface-level summaries. Winning requires an entirely different level of systematic speed and precision.",
        "duration": 15.0,
        "theme": "problem"
    },
    {
        "id": "beat_02",
        "title": "CHAMBER 1 & 2: INTAKE & THE GRAPHIFY BRAIN",
        "subtitle": "Optical Decryption & 132+ Global Case Benchmarks",
        "voice_text": "Drop in any document or dataset. The machine's optical intake chamber strips layout noise, extracts balance sheets, and maps constraints. Simultaneously, the Graphify brain traverses 132 verified global case competitions to borrow proven championship patterns.",
        "duration": 18.0,
        "theme": "intake"
    },
    {
        "id": "beat_03",
        "title": "THE 14 AUTONOMOUS AGENTS IN LOCKSTEP",
        "subtitle": "Root-Cause Surgeons, Innovation Labs, and Red Teams",
        "voice_text": "Behind the scenes, fourteen specialized AI agents operate in synchronized lockstep. Root-cause surgeons isolate core bottlenecks using MECE issue trees, while the innovation lab brainstorms and scores solution archetypes against the official judging rubric.",
        "duration": 18.0,
        "theme": "agents"
    },
    {
        "id": "beat_04",
        "title": "THE QUANTITATIVE FINANCIAL REACTOR",
        "subtitle": "Little's Law, TOC Bottlenecks, and 3-Scenario Proformas",
        "voice_text": "Every recommendation is backed by zero-skip industrial mathematics. Little's Law proves cycle-time compression, the Theory of Constraints synchronizes capacity, and proforma financial models survive rigorous Bear, Base, and Bull sensitivity testing.",
        "duration": 18.0,
        "theme": "math"
    },
    {
        "id": "beat_05",
        "title": "THE OMNICHANNEL DELIVERABLE FACTORY",
        "subtitle": "PDFs, 12-Slide Pitch Deck, Financial Models, Video, and Web App",
        "voice_text": "In under sixty seconds, the deliverable factory outputs the complete championship suite: two vector-grade executive blueprints, a twelve-slide pitch deck, dynamic financial models, and a live interactive web simulator.",
        "duration": 17.0,
        "theme": "factory"
    },
    {
        "id": "beat_06",
        "title": "CHAMPIONSHIP VICTORY BY DESIGN",
        "subtitle": "Airtight Judge Q&A Defense & 100% Deterministic Execution",
        "voice_text": "Before you take the stage, an adversarial red-team judge stress-tests every vulnerability with pre-calculated rebuttals. This is not just analysis; it is an autonomous competition-winning machine.",
        "duration": 14.0,
        "theme": "victory"
    }
]

def draw_header_footer(draw, width, height, title, subtitle):
    # Top HUD Bar
    draw.rectangle([(0, 0), (width, 80)], fill=(15, 23, 42))
    draw.line([(0, 80), (width, 80)], fill=CYAN, width=2)
    draw.rectangle([(40, 20), (280, 60)], fill=SURFACE, outline=CYAN, width=1)
    draw.text((55, 30), "AUTONOMOUS CASE SYSTEM", fill=CYAN)
    draw.text((width - 320, 30), "14 AGENTS | 39 SKILLS | 100% DETERMINISTIC", fill=MUTED)

    # Title area
    draw.text((60, 110), title, fill=WHITE)
    draw.text((60, 150), subtitle, fill=AMBER)

    # Bottom status bar
    draw.rectangle([(0, height - 60), (width, height)], fill=(15, 23, 42))
    draw.line([(0, height - 60), (width, height - 60)], fill=BORDER, width=1)
    draw.text((60, height - 42), "CONFIDENTIAL STRATEGY SYSTEM - STRICT COMPETITION NEUTRALITY", fill=MUTED)
    draw.text((width - 240, height - 42), "SYSTEM ENGINE v2.5", fill=CYAN)

def generate_frame_beat_01(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "THE CASE COMPETITION CHALLENGE", "High-Stakes Business Case Dilemma")

    # Draw Tech Grid
    for x in range(60, width - 60, 80):
        draw.line([(x, 190), (x, height - 80)], fill=(20, 28, 45), width=1)
    for y in range(190, height - 80, 80):
        draw.line([(60, y), (width - 60, y)], fill=(20, 28, 45), width=1)

    # 3 Pain Point Cards
    cards = [
        ("40+ PAGE CASE BRIEFS", "Complex unstructured PDFs, raw datasets, hidden financial leaks, and ambiguous instructions.", CYAN, 100),
        ("BRUTAL 24-HR TIMELINES", "Losing teams spend 80% of time making slides and debating ideas rather than proving financial impact.", AMBER, 680),
        ("AGGRESSIVE JUDGE PANELS", "Executive judges quickly dismantle vague assumptions, missing algebra, and unvetted forecasts.", PURPLE, 1260)
    ]
    for title, desc, col, x in cards:
        draw.rectangle([(x, 260), (x + 560, 720)], fill=SURFACE, outline=col, width=2)
        draw.rectangle([(x, 260), (x + 560, 275)], fill=col)
        draw.text((x + 30, 310), title, fill=WHITE)
        draw.line([(x + 30, 360), (x + 530, 360)], fill=BORDER, width=1)
        # Multi-line text simulation
        words = desc.split(" ")
        lines = []
        cur = []
        for w in words:
            cur.append(w)
            if len(" ".join(cur)) > 30:
                lines.append(" ".join(cur))
                cur = []
        if cur:
            lines.append(" ".join(cur))
        for idx, line in enumerate(lines):
            draw.text((x + 30, 400 + idx * 40), line, fill=MUTED)

    # Bottom Callout banner
    draw.rectangle([(100, 760), (width - 100, 860)], fill=SURFACE_LIGHT, outline=CYAN, width=1)
    draw.text((140, 785), "THE SOLUTION: An autonomous 14-agent intelligence factory that turns any case into a victory package in 60s.", fill=WHITE)
    draw.text((140, 820), "Status: Zero Hallucination | Explicit Mathematics | Complete Omnichannel Deliverables", fill=TEAL)
    return img

def generate_frame_beat_02(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "CHAMBER 1 & 2: INTAKE & THE GRAPHIFY BRAIN", "Optical Decryption & Global Competition Intelligence")

    # Chamber 1 Box: Optical Intake
    draw.rectangle([(100, 240), (880, 750)], fill=SURFACE, outline=CYAN, width=2)
    draw.rectangle([(100, 240), (880, 255)], fill=CYAN)
    draw.text((130, 280), "CHAMBER 1: OPTICAL INTAKE & DECRYPTION", fill=WHITE)
    draw.text((130, 320), "• PyMuPDF Vector Text & Table Extractor", fill=CYAN)
    draw.text((130, 370), "• Separates Verified Evidence from Unverified Assumptions", fill=MUTED)
    draw.text((130, 420), "• Identifies Missing Variables & Hidden Financial Constraints", fill=MUTED)
    draw.text((130, 470), "• Input Agnostic: PDF, PPTX, CSV, Excel, Word, or Markdown", fill=TEAL)

    # Vector illustration of document scanning
    draw.rectangle([(150, 530), (830, 700)], fill=(15, 23, 42), outline=BORDER, width=1)
    draw.text((180, 560), "INGESTION STREAM: 100,000 Records / 45-Page Case Brief", fill=AMBER)
    draw.line([(180, 600), (800, 600)], fill=CYAN, width=2)
    draw.text((180, 630), "STATUS: PARSED & VALIDATED (Execution Time: 1.2s)", fill=TEAL)

    # Connector Arrow
    draw.line([(880, 495), (1040, 495)], fill=WHITE, width=4)
    draw.polygon([(1040, 485), (1070, 495), (1040, 505)], fill=WHITE)

    # Chamber 2 Box: Graphify Brain
    draw.rectangle([(1070, 240), (1820, 750)], fill=SURFACE, outline=PURPLE, width=2)
    draw.rectangle([(1070, 240), (1820, 255)], fill=PURPLE)
    draw.text((1100, 280), "CHAMBER 2: THE GRAPHIFY NEURAL BRAIN", fill=WHITE)
    draw.text((1100, 320), "• Semantic Traversal across 39 Specialized Skills", fill=PURPLE)
    draw.text((1100, 370), "• Curated Knowledge Base: 132+ Global Case Competitions", fill=MUTED)
    draw.text((1100, 420), "• Benchmark Database: Harvard, Wharton, Rotman, MIT Sloan", fill=MUTED)
    draw.text((1100, 470), "• Zero Token Bloat: Precise Dynamic Task Routing", fill=TEAL)

    # Visual nodes for Graphify
    node_coords = [(1180, 580), (1350, 540), (1500, 620), (1680, 560), (1400, 680)]
    for idx, (nx, ny) in enumerate(node_coords):
        draw.ellipse([(nx - 20, ny - 20), (nx + 20, ny + 20)], fill=PURPLE, outline=WHITE, width=2)
        draw.text((nx - 12, ny - 10), f"S{idx+1}", fill=WHITE)
        if idx > 0:
            px, py = node_coords[idx - 1]
            draw.line([(px, py), (nx, ny)], fill=CYAN, width=2)

    # Bottom summary
    draw.rectangle([(100, 780), (width - 100, 860)], fill=SURFACE_LIGHT, outline=BORDER, width=1)
    draw.text((140, 810), "RESULT: Instant contextual grounding with 132 championship precedents before writing a single word.", fill=WHITE)
    return img

def generate_frame_beat_03(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "THE 14 AUTONOMOUS AGENTS IN SYNCHRONIZED MOTION", "From Master Orchestrator to Adversarial Red-Team Judge")

    agent_roles = [
        ("00 Master Orchestrator", "Air Traffic Controller", CYAN),
        ("01 Intelligence Analyst", "Document Detective", CYAN),
        ("02 Competitions Scout", "Global Benchmarker", CYAN),
        ("03 Root-Cause Surgeon", "MECE Issue-Tree Pro", PURPLE),
        ("04 Innovation Lab", "Creative Brainstormer", PURPLE),
        ("05 Strategy Evaluator", "Decision Matrix Judge", PURPLE),
        ("06 Solution Architect", "Systems Engineer", AMBER),
        ("07 Proforma Modeler", "Wall Street CFO", AMBER),
        ("08 Operations Planner", "Roadmap Director", AMBER),
        ("09 Slide Designer", "Pitch Deck Specialist", TEAL),
        ("10 Document Architect", "PDF Publisher", TEAL),
        ("11 Motion Director", "Video Storyteller", TEAL),
        ("12 Prototype Developer", "Web App Engineer", TEAL),
        ("13 Red-Team Judge", "Hostile Interrogator", PURPLE)
    ]

    for idx, (name, role, col) in enumerate(agent_roles):
        c_idx = idx % 2
        r_idx = idx // 2
        x = 100 if c_idx == 0 else 980
        y = 210 + r_idx * 75

        draw.rectangle([(x, y), (x + 840, y + 65)], fill=SURFACE, outline=BORDER, width=1)
        draw.rectangle([(x, y), (x + 8, y + 65)], fill=col)
        draw.text((x + 25, y + 12), name, fill=WHITE)
        draw.text((x + 25, y + 36), f"Specialty: {role}", fill=col)
        draw.rectangle([(x + 680, y + 18), (x + 820, y + 48)], fill=(15, 23, 42), outline=col, width=1)
        draw.text((x + 705, y + 25), "ACTIVE", fill=col)

    # Bottom callout
    draw.rectangle([(100, 780), (width - 100, 860)], fill=SURFACE_LIGHT, outline=CYAN, width=1)
    draw.text((140, 810), "PARALLEL & SEQUENTIAL DISPATCH: Zero circular dependencies. Every handoff is strictly validated.", fill=WHITE)
    return img

def generate_frame_beat_04(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "THE QUANTITATIVE & FINANCIAL REACTOR", "Little's Law, Theory of Constraints & 3-Scenario Proforma Models")

    # 4 Formula Panels
    f_boxes = [
        ("LITTLE'S LAW (QUEUEING & FLOW)", "WIP = Throughput (TH) x Cycle Time (CT)", "Proves cycle-time reduction without adding headcount. Baseline CT = 17 hrs -> Post-Optimization CT = 9 hrs.", CYAN, 100, 220),
        ("THEORY OF CONSTRAINTS (TOC)", "System Throughput = min(R1, R2, ..., Rn)", "Eliminates station bottlenecks. Elevates station line rate from 48 to 75 units/hr, capturing $1.4M annual value.", PURPLE, 980, 220),
        ("UNIT ECONOMICS & LTV/CAC", "LTV = (ARPU x Margin) / Churn  >= 3.0x CAC", "Calculates unit viability. ARPU $1,200 with 68% margin yields $54.4k LTV vs $12.5k CAC -> 4.35x ratio.", AMBER, 100, 480),
        ("BREAKEVEN & CAPITAL HURDLE", "BEP = Fixed Costs / Unit Contribution Margin", "Calculates required volume. Capex $350k at $85/unit margin yields BEP of 4,118 units. Payback: 7.4 months.", TEAL, 980, 480)
    ]

    for title, formula, proof, col, x, y in f_boxes:
        draw.rectangle([(x, y), (x + 840, y + 220)], fill=SURFACE, outline=col, width=2)
        draw.rectangle([(x, y), (x + 840, y + 12)], fill=col)
        draw.text((x + 30, y + 30), title, fill=WHITE)
        draw.rectangle([(x + 30, y + 70), (x + 810, y + 120)], fill=(15, 23, 42), outline=BORDER, width=1)
        draw.text((x + 50, y + 85), formula, fill=col)
        draw.text((x + 30, y + 140), proof, fill=MUTED)

    # Bottom Sensitivity Strip
    draw.rectangle([(100, 750), (width - 100, 860)], fill=SURFACE_LIGHT, outline=BORDER, width=1)
    draw.text((140, 775), "MANDATORY 3-SCENARIO SENSITIVITY TESTING:", fill=WHITE)
    draw.text((140, 810), "• BEAR CASE (-20% adoption): EBITDA $850k | BASE CASE: EBITDA $1.42M | BULL CASE (+25% adoption): EBITDA $2.15M", fill=TEAL)
    return img

def generate_frame_beat_05(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "THE OMNICHANNEL DELIVERABLE FACTORY", "12 Synchronized Assets Produced Autonomously in 'Finished Resources/'")

    # Visual representation of 6 deliverable categories
    deliverable_boxes = [
        ("STRATEGY BLUEPRINT PDF", "Vector-crisp 6-page comprehensive executive solution guide with MECE issue trees.", CYAN, 100, 220),
        ("12-SLIDE PITCH DECK", "Final_Presentation.pptx: Boardroom-ready executive deck with visual hierarchy.", PURPLE, 680, 220),
        ("FINANCIAL WORKBOOK", "financial_model.xlsx: Complete 3-year proforma statements, NPV, IRR, and sensitivity.", AMBER, 1260, 220),
        ("CINEMATIC DEMO VIDEO", "120s MP4: High-impact video showing how the operational solution works.", TEAL, 100, 480),
        ("INTERACTIVE WEB APP", "React + Tailwind simulator: Live parameter sliders, EBITDA recalculation, and charts.", CYAN, 680, 480),
        ("JUDGE DEFENSE MATRIX", "Judge_QA_Defense.md: Top 5 adversarial questions with pre-calculated mathematical rebuttals.", PURPLE, 1260, 480)
    ]

    for title, desc, col, x, y in deliverable_boxes:
        draw.rectangle([(x, y), (x + 560, y + 220)], fill=SURFACE, outline=col, width=2)
        draw.rectangle([(x, y), (x + 560, y + 10)], fill=col)
        draw.text((x + 25, y + 30), title, fill=WHITE)
        draw.line([(x + 25, y + 70), (x + 535, y + 70)], fill=BORDER, width=1)
        draw.text((x + 25, y + 100), desc, fill=MUTED)
        draw.rectangle([(x + 25, y + 160), (x + 200, y + 195)], fill=(15, 23, 42), outline=col, width=1)
        draw.text((x + 45, y + 170), "READY TO PRESENT", fill=col)

    # Bottom summary
    draw.rectangle([(100, 750), (width - 100, 860)], fill=SURFACE_LIGHT, outline=TEAL, width=1)
    draw.text((140, 775), "COMPREHENSIVE MULTI-FORMAT ADVANTAGE:", fill=WHITE)
    draw.text((140, 810), "While competitors submit a plain slide deck, you deliver a complete enterprise portfolio.", fill=TEAL)
    return img

def generate_frame_beat_06(width=1920, height=1080):
    img = Image.new("RGB", (width, height), BG_DARK)
    draw = ImageDraw.Draw(img)
    draw_header_footer(draw, width, height, "CHAMPIONSHIP VICTORY BY DESIGN", "Built for 1st Place Execution in Any Global Competition")

    # Center Victory Shield
    cx, cy = width // 2, 460
    draw.rectangle([(cx - 450, cy - 200), (cx + 450, cy + 200)], fill=SURFACE, outline=AMBER, width=2)
    draw.rectangle([(cx - 450, cy - 200), (cx + 450, cy - 185)], fill=AMBER)

    draw.text((cx - 280, cy - 140), "THE CASE COMPETITION STANDARD", fill=AMBER)
    draw.text((cx - 360, cy - 80), "[x] MECE Problem Diagnosis: Distinguishes symptoms from root causes", fill=WHITE)
    draw.text((cx - 360, cy - 30), "[x] Zero-Skip Mathematical Proofs: Every calculation explicitly derived", fill=WHITE)
    draw.text((cx - 360, cy + 20), "[x] 3-Horizon Implementation: Phased execution with leading KPI tracking", fill=WHITE)
    draw.text((cx - 360, cy + 70), "[x] Adversarial Judge Defense: Top 5 hostile questions pre-rebutted", fill=WHITE)
    draw.text((cx - 360, cy + 120), "[x] Omnichannel Deliverables: Strategy PDF, 12 Slides, Models & Video", fill=WHITE)

    # Bottom summary
    draw.rectangle([(100, 750), (width - 100, 860)], fill=SURFACE_LIGHT, outline=CYAN, width=1)
    draw.text((140, 775), "AUTONOMOUS SYSTEM READY FOR EXECUTION", fill=CYAN)
    draw.text((140, 810), "Upload any case brief, dataset, or competition prompt to launch the full pipeline in under 60 seconds.", fill=WHITE)
    return img

async def synthesize_voiceovers():
    import edge_tts
    os.makedirs(ASSETS_DIR, exist_ok=True)
    voice = "en-US-ChristopherNeural"
    
    print("[1/5] Synthesizing Neural Voiceovers via edge-tts...")
    audio_files = []
    for beat in BEATS_DATA:
        b_id = beat["id"]
        out_audio = ASSETS_DIR / f"{b_id}.mp3"
        print(f"  -> Synthesizing {b_id}: '{beat['title']}'...")
        communicate = edge_tts.Communicate(beat["voice_text"], voice)
        await communicate.save(str(out_audio))
        audio_files.append(out_audio)
    return audio_files

def generate_visual_frames():
    os.makedirs(FRAMES_DIR, exist_ok=True)
    print("[2/5] Rendering 1080p Motion Visual Frames...")
    generators = [
        ("beat_01", generate_frame_beat_01),
        ("beat_02", generate_frame_beat_02),
        ("beat_03", generate_frame_beat_03),
        ("beat_04", generate_frame_beat_04),
        ("beat_05", generate_frame_beat_05),
        ("beat_06", generate_frame_beat_06)
    ]
    frame_paths = []
    for b_id, gen_fn in generators:
        f_path = FRAMES_DIR / f"{b_id}.png"
        img = gen_fn(1920, 1080)
        img.save(f_path)
        frame_paths.append(f_path)
        print(f"  -> Rendered: {f_path}")
    return frame_paths

def generate_procedural_soundscape(total_duration=100.0, output_wav=ASSETS_DIR / "ambient_bed.wav"):
    """Generate subtle high-tech ambient audio bed using numpy."""
    print("[3/5] Generating procedural high-tech soundscape...")
    import wave
    sr = 48000
    t = np.linspace(0, total_duration, int(sr * total_duration), endpoint=False)
    
    # Gentle subtle synth chord (C minor 9 / high tech ambience): 130.81Hz, 196.00Hz, 311.13Hz, 392.00Hz
    tone1 = 0.03 * np.sin(2 * np.pi * 130.81 * t)
    tone2 = 0.02 * np.sin(2 * np.pi * 196.00 * t)
    tone3 = 0.015 * np.sin(2 * np.pi * 311.13 * t)
    # Slow gentle amplitude modulation (breathing effect)
    lfo = 0.5 + 0.5 * np.sin(2 * np.pi * 0.1 * t)
    mix = (tone1 + tone2 + tone3) * lfo
    
    # Soft periodic UI ping every 16 seconds
    ping_mask = np.zeros_like(t)
    for ping_t in range(5, int(total_duration), 16):
        idx_start = int(ping_t * sr)
        ping_dur = int(0.5 * sr)
        if idx_start + ping_dur < len(t):
            sub_t = np.linspace(0, 0.5, ping_dur, endpoint=False)
            decay = np.exp(-sub_t / 0.08)
            ping = 0.04 * np.sin(2 * np.pi * 880 * sub_t) * decay
            mix[idx_start:idx_start + ping_dur] += ping
            
    # Normalize to -18 dBFS
    max_val = np.max(np.abs(mix))
    if max_val > 0:
        mix = (mix / max_val) * 0.12
    audio_int16 = np.int16(mix * 32767)
    
    with wave.open(str(output_wav), "w") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(audio_int16.tobytes())
    print(f"  -> Generated ambient bed: {output_wav}")

def assemble_video_with_ffmpeg():
    print("[4/5] Compiling and Encoding 1080p Video via FFmpeg...")
    # First: create clips for each beat with its narration
    segment_videos = []
    for idx, beat in enumerate(BEATS_DATA):
        b_id = beat["id"]
        frame_png = FRAMES_DIR / f"{b_id}.png"
        audio_mp3 = ASSETS_DIR / f"{b_id}.mp3"
        seg_mp4 = ASSETS_DIR / f"seg_{b_id}.mp4"
        
        # FFmpeg command to loop image over audio duration + 0.5s buffer
        cmd = [
            "ffmpeg", "-y",
            "-loop", "1", "-i", str(frame_png),
            "-i", str(audio_mp3),
            "-c:v", "libx264", "-tune", "stillimage", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest",
            "-movflags", "+faststart",
            str(seg_mp4)
        ]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print(f"Error encoding {seg_mp4}: {res.stderr}")
            raise RuntimeError(res.stderr)
        segment_videos.append(seg_mp4)
        print(f"  -> Encoded segment: {seg_mp4}")

    # Concatenate all segments into single video
    concat_list = ASSETS_DIR / "concat_list.txt"
    with open(concat_list, "w") as f:
        for seg in segment_videos:
            # Use relative forward slashes
            f.write(f"file '{seg.name}'\n")

    combined_raw = ASSETS_DIR / "combined_raw.mp4"
    cmd_concat = [
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0",
        "-i", str(concat_list),
        "-c", "copy",
        str(combined_raw)
    ]
    subprocess.run(cmd_concat, check=True)

    # Finally mix with subtle ambient bed
    ambient_wav = ASSETS_DIR / "ambient_bed.wav"
    print("[5/5] Final Mastering: Mixing Narration with Ambient Soundscape...")
    cmd_master = [
        "ffmpeg", "-y",
        "-i", str(combined_raw),
        "-i", str(ambient_wav),
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:weights=1.0 0.25[a]",
        "-map", "0:v", "-map", "[a]",
        "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
        str(OUTPUT_MP4)
    ]
    subprocess.run(cmd_master, check=True)
    print(f"\n[SUCCESS] Explainer Video Generated: {OUTPUT_MP4}")

    # Write beats.json metadata
    beats_meta_path = VIDEO_DIR / "beats.json"
    with open(beats_meta_path, "w", encoding="utf-8") as f:
        json.dump({
            "project": "Case Competition System Architecture Explainer",
            "resolution": "1920x1080",
            "fps": 30,
            "engine": "motion-video-director v3.5.2",
            "beats": BEATS_DATA,
            "output_file": str(OUTPUT_MP4.name)
        }, f, indent=2)
    print(f"[OK] Wrote beats metadata: {beats_meta_path}")

async def main():
    os.makedirs(VIDEO_DIR, exist_ok=True)
    await synthesize_voiceovers()
    generate_visual_frames()
    generate_procedural_soundscape(total_duration=120.0)
    assemble_video_with_ffmpeg()

if __name__ == "__main__":
    asyncio.run(main())

