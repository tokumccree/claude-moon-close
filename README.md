# claude-moon-close

A visual closing ceremony for Claude Code sessions.

Shows the current moon phase as ASCII art, then signs off with a personality-matched haiku. Drop it into any session-close skill — or run it on its own.

First run walks you through a one-minute setup: choose your assistant's name, personality, and haiku style. Skip setup to use the defaults.

---

## What it looks like

```
                                      _..._   
                                    .'     `. 
        .-.                        :         :
     .-(   )-.                     :         :
    (___.__)__)                    `.       .'
                                     `-...-'  
                   ,_,                        
                  (ò,ó)                       
                  (   )                       
~~~~~|~~~~~|~~~~~|~"~"~|~~~~~|~~~~~|~~~~~|~~~~
~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~
~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~~|~~~~
```

```
the cursor blinks once
then goes still — the work remains
somewhere in the dark

---

"Good session. The moon agrees."
— Zeno
```

96 variants across 8 moon phases. Rotates through all 12 variants per phase before repeating.

---

## Install

1. Copy this repo's contents into `.claude/skills/moon-close/` in your project
2. Run a session — setup launches automatically on first use

---

## Add to your session-close skill

At the end of your SKILL.md, add:

```markdown
### Final Step: Moon Close
Run the moon-close skill.
```

Or invoke it standalone whenever you want the ceremony.

---

## Setup

On first run, you'll be asked:

**1. Does your assistant have a name?**
If yes, enter it. If no, continue to personality.

**2. Choose a personality:**
- Zen — spare, mystical, contemplative
- Philosopher — thoughtful, questioning, a little Socratic
- Warm & playful — light, encouraging, a little fun
- Big Thinker — curious, brilliant, a bit of mad scientist energy

**3. Name options (if you don't have one yet)** — matched to your personality:
- Zen: Mu, Basho, Dogen, Ryokan, Enso, Kensho
- Philosopher: Seneca, Epictetus, Spinoza, Socrates, Marcus, Hypatia
- Warm & playful: Ember, Sage, Nova, Fern, Thistle, Lumen
- Big Thinker: Einstein, Tesla, Feynman, Sagan, Tyson, Turing

**4. Haiku style:**
- Session — a sidelong glance at what you worked on
- Whimsical — fun, a little absurd, warm
- Zen — mystical, spare, about impermanence or stillness
- Random — pick one each session (default)

Answers save to `config.md`. Re-run setup anytime: just say "moon-close setup".

**Skip setup?** It uses the defaults: name Zeno, warm & playful personality, random haiku mix.

---

## How it works

- Fetches moon phase from [wttr.in](https://wttr.in) (cached daily)
- Picks a random unused variant from 12 ASCII images for that phase
- Tracks shown variants in `moon-history.md` — resets after all 12 are shown
- Writes a haiku styled to your personality and haiku preference

---

## Customize

**Your city** — in `SKILL.md`, find the wttr.in fetch and change `New+York` to your city. Any major city works — moon phase doesn't vary much by location.

**Re-run setup** — say "moon-close setup" to change name, personality, or haiku style anytime.

---

## Files

```
moon-close/
├── SKILL.md                    — the skill definition
├── config.md                   — your setup preferences (auto-created on first run)
├── moon-history.md             — tracks shown variants (auto-managed)
├── moon-phase.md               — daily phase cache (auto-managed)
└── moon-phase-variants/
    ├── full/                   — 12 variants
    ├── new-dark/               — 12 variants
    ├── waxing-crescent/        — 12 variants
    ├── first-quarter/          — 12 variants
    ├── waxing-gibbous/         — 12 variants
    ├── waning-gibbous/         — 12 variants
    ├── last-quarter/           — 12 variants
    └── waning-crescent/        — 12 variants
```
