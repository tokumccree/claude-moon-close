#!/usr/bin/env python3
"""
Moon stamp script for session-close skill.
Handles phase lookup, image selection, history tracking, and prints the image.
Single call replaces 5 separate tool calls.
"""

import json
import math
import os
import random
import subprocess
import sys
from datetime import date, datetime, timezone

SKILL_DIR = os.path.dirname(os.path.abspath(__file__))
PHASE_FILE = os.path.join(SKILL_DIR, "moon-phase.md")
HISTORY_FILE = os.path.join(SKILL_DIR, "moon-history.md")
VARIANTS_DIR = os.path.join(SKILL_DIR, "moon-phase-variants")

def compute_moon_phase(dt=None):
    """Returns (phase_name, illumination_pct). dt is a datetime (UTC). Defaults to now."""
    if dt is None:
        dt = datetime.now(timezone.utc)
    ref = datetime(2000, 1, 6, 18, 14, tzinfo=timezone.utc)
    synodic = 29.530588853
    age = ((dt - ref).total_seconds() / 86400.0) % synodic
    illumination = (1 - math.cos(2 * math.pi * age / synodic)) / 2 * 100
    if age < 1.84:
        phase = "New Moon"
    elif age < 5.53:
        phase = "Waxing Crescent"
    elif age < 9.22:
        phase = "First Quarter"
    elif age < 12.91:
        phase = "Waxing Gibbous"
    elif age < 16.61:
        phase = "Full Moon"
    elif age < 20.30:
        phase = "Waning Gibbous"
    elif age < 23.99:
        phase = "Last Quarter"
    elif age < 27.68:
        phase = "Waning Crescent"
    else:
        phase = "New Moon"
    return phase, round(illumination, 1)


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
    phase, illum = compute_moon_phase()
    with open(PHASE_FILE, "w") as f:
        f.write(f"---\nupdated: {today}\n---\n\n# Moon Phase\n\n**Phase:** {phase}\n**Illumination:** {illum}%\n")
    return phase

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
