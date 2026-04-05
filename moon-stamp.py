#!/usr/bin/env python3
"""
Moon stamp script for session-close skill.
Handles phase lookup, image selection, history tracking, and prints the image.
Single call replaces 5 separate tool calls.
"""

import json
import os
import random
import subprocess
import sys
from datetime import date

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE_FILE = os.path.join(SKILL_DIR, "moon-phase.md")
HISTORY_FILE = os.path.join(SKILL_DIR, "moon-history.md")
VARIANTS_DIR = os.path.join(SKILL_DIR, "moon-phase-variants")

PHASE_MAP = {
    "new moon": "new-dark",
    "waxing crescent": "waxing-crescent",
    "first quarter": "first-quarter",
    "waxing gibbous": "waxing-gibbous",
    "full moon": "full",
    "waning gibbous": "waning-gibbous",
    "last quarter": "last-quarter",
    "waning crescent": "waning-crescent",
}

def get_phase():
    today = str(date.today())
    if os.path.exists(PHASE_FILE):
        with open(PHASE_FILE) as f:
            content = f.read()
        if f"updated: {today}" in content:
            for line in content.splitlines():
                if line.startswith("**Phase:**"):
                    return line.replace("**Phase:**", "").strip()
    try:
        result = subprocess.run(
            ["curl", "-s", "https://wttr.in/New+York?format=j1"],  # change to your city
            capture_output=True, text=True, timeout=5
        )
        data = json.loads(result.stdout)
        phase = data["weather"][0]["astronomy"][0]["moon_phase"]
        illum = data["weather"][0]["astronomy"][0]["moon_illumination"]
        with open(PHASE_FILE, "w") as f:
            f.write(f"---\nupdated: {today}\n---\n\n# Moon Phase\n\n**Phase:** {phase}\n**Illumination:** {illum}%\n")
        return phase
    except Exception:
        return "Full Moon"

def read_history():
    default = {k: [] for k in PHASE_MAP.values()}
    if not os.path.exists(HISTORY_FILE):
        return default
    with open(HISTORY_FILE) as f:
        content = f.read()
    history = dict(default)
    for line in content.splitlines():
        for folder in PHASE_MAP.values():
            if line.strip().startswith(f"{folder}:"):
                val = line.split(":", 1)[1].strip().strip("[]")
                history[folder] = [int(x.strip()) for x in val.split(",") if x.strip().isdigit()]
    return history

def write_history(history):
    lines = ["---"]
    for folder in sorted(history.keys()):
        used = history[folder]
        lines.append(f"{folder}: [{', '.join(str(n) for n in used)}]")
    lines.append("---")
    with open(HISTORY_FILE, "w") as f:
        f.write("\n".join(lines) + "\n")

def main():
    phase = get_phase()
    folder = PHASE_MAP.get(phase.lower(), "full")
    history = read_history()
    used = history.get(folder, [])
    available = [n for n in range(1, 13) if n not in used]
    if not available:
        history[folder] = []
        available = list(range(1, 13))
    chosen = random.choice(available)
    img_path = os.path.join(VARIANTS_DIR, folder, f"{chosen}-{folder}.txt")
    with open(img_path) as f:
        image = f.read()
    history[folder] = history.get(folder, []) + [chosen]
    write_history(history)
    print(image, end="")

if __name__ == "__main__":
    main()
