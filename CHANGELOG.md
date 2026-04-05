# Changelog

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
