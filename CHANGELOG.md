# Changelog

## v1.3.0 — 2026-04-16
- Haiku log: each haiku is now appended to `haiku-log.md` with the date — builds a record over time
- `/tmp` redirect pattern: moon script now writes to `/tmp/moon_stamp.txt` and is read with the Read tool, decoupling script execution from display (allows commits or other work in between)
- Date detection: `date +%Y-%m-%d` run at startup and held as `LOG_DATE` for accurate date fields

## v1.2.0 — 2026-04-04
- Optional SESSION CLOSED footer — configurable during onboarding (Question 4), defaults to on
- Ninja mode output: skipped steps run silently, no "None." or "Skipped." lines
- Everything in one fenced block (moon art + haiku + sign-off) for cleaner rendering
- `git status --short` instead of `git status`

## v1.1.0 — 2026-04-04
- Added `moon-stamp.py` — single script handles phase lookup, image selection, and history tracking
- Replaces 5 separate tool calls with one bash call for cleaner session output
- SKILL.md updated to reference the script

## v1.0.0 — 2026-04-04
- Initial release
- 96 ASCII moon phase images across 8 phases (12 variants each)
- First-run setup: personality selection, assistant name, haiku style
- Personality options: Zen, Philosopher, Warm & playful, Big Thinker
- Name suggestions matched to personality
- Haiku styles: session, whimsical, zen, or random
- Moon phase fetched live from wttr.in, cached daily
- Rotation tracker so variants don't repeat until all 12 are shown
