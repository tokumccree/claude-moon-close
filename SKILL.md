---
name: moon-close
description: End-of-session visual ceremony. Shows the current moon phase as ASCII art and closes with a personality-matched haiku. Designed to be called at the end of any session-close skill, or run standalone.
metadata:
  model: sonnet
---

# Skill: Moon Close

## Purpose

A visual closing ceremony for any Claude Code session. Prints the current moon phase as ASCII art, then signs off with a haiku styled to your assistant's personality.

## How to Use

**Add to your existing session-close skill** — at the very end of your SKILL.md:
```
### Final Step: Moon Close
Run the moon-close skill.
```

**Or run standalone** — invoke it directly whenever you want the ceremony.

**First-time setup** — on the first run, the skill walks you through a short setup (name, personality, haiku style). Takes about a minute. You can re-run it anytime by saying "moon-close setup".

---

## Steps

### Step 0: Check config

Read `.claude/skills/moon-close/config.md`.

- If `setup_complete: true` — skip to Step 1.
- If the file is missing or `setup_complete` is false — run Setup (below) first, then continue.

---

## Setup (first run or on request)

Ask the following questions one at a time. Wait for each answer before proceeding.

At any point, the user can say "skip" to use the defaults (listed at the end of this section).

---

**Question 1: Does your assistant already have a name?**

"Does your assistant have a name? (yes / no / skip to use defaults)"

- If **yes**: "What's their name?" → save as `assistant_name`, skip to Question 3.
- If **no**: continue to Question 2.
- If **skip**: use all defaults, jump to saving config.

---

**Question 2: Choose a personality**

"Choose a personality for your assistant:"

1. **Zen** — spare, mystical, contemplative
2. **Philosopher** — thoughtful, questioning, a little Socratic
3. **Warm & playful** — light, encouraging, a little fun
4. **Big Thinker** — curious, brilliant, a bit of mad scientist energy

Save the choice as `personality`.

Then ask: "Here are some names that fit that vibe — pick one or type your own:"

**Zen names:** Mu, Basho, Dogen, Ryokan, Enso, Kensho
**Philosopher names:** Seneca, Epictetus, Spinoza, Socrates, Marcus, Hypatia
**Warm & playful names:** Ember, Sage, Nova, Fern, Thistle, Lumen
**Big Thinker names:** Einstein, Tesla, Feynman, Sagan, Tyson, Turing

Save the choice as `assistant_name`.

---

**Question 3: Haiku style**

"How should your closing haiku be styled?"

1. **Session** — a sidelong glance at what you worked on
2. **Whimsical** — fun, a little absurd, warm
3. **Zen** — mystical, spare, about impermanence or stillness
4. **Random** — pick one at random each session (default)

Save the choice as `haiku_style` using values: `session`, `whimsical`, `zen`, `random`.

---

**Save config**

Write to `.claude/skills/moon-close/config.md`:

```markdown
---
assistant_name: [name]
personality: [zen | philosopher | warm-playful | big-thinker]
haiku_style: [session | whimsical | zen | random]
setup_complete: true
---
```

Confirm: "Setup complete. You're ready to close sessions in style. You can re-run setup anytime by saying 'moon-close setup'."

**Defaults (if skipped):**
- `assistant_name`: Zeno
- `personality`: warm-playful
- `haiku_style`: random
- `setup_complete`: true

---

## Step 1: Get current moon phase

Check `.claude/skills/moon-close/moon-phase.md`.

- If the `updated` date matches today's date, use the `Phase` value from that file.
- If the file is missing or the date doesn't match today, fetch live:
  ```bash
  # Edit the city to your location — moon phase doesn't vary much by location,
  # so any major city works fine.
  curl -s "https://wttr.in/New+York?format=j1"
  ```
  Extract `weather[0].astronomy[0].moon_phase`.
- If both fail, use `Full Moon` as the fallback.

After a live fetch, update `.claude/skills/moon-close/moon-phase.md` with today's date and the phase.

## Step 2: Normalize phase name to folder

| Phase name from API | Folder |
|---|---|
| New Moon | new-dark |
| Waxing Crescent | waxing-crescent |
| First Quarter | first-quarter |
| Waxing Gibbous | waxing-gibbous |
| Full Moon | full |
| Waning Gibbous | waning-gibbous |
| Last Quarter | last-quarter |
| Waning Crescent | waning-crescent |

If the phase doesn't match, use `full`.

## Step 3: Select image

Read `.claude/skills/moon-close/moon-history.md`. Tracks which variants have been shown per phase to avoid repeats.

Format:
```markdown
---
first-quarter: []
full: []
last-quarter: []
new-dark: []
waning-crescent: []
waning-gibbous: []
waxing-crescent: []
waxing-gibbous: []
---
```

Selection logic:
1. Find the used list for the current phase.
2. Available = [1..12] minus the used list.
3. If available is empty, reset the list for this phase and use [1..12].
4. Pick one number at random from available.

If moon-history.md doesn't exist, create it with all phases as empty lists.

## Step 4: Print the image

File path:
```
.claude/skills/moon-close/moon-phase-variants/{folder}/{N}-{folder}.txt
```

Read and print the file contents exactly as stored, inside a triple-backtick code block (no language tag). Do not modify spacing or characters.

## Step 5: Update moon-history.md

Add the chosen number to the used list for this phase and write the file.

## Step 6: Closing haiku

Read `personality` and `haiku_style` from config.

**Haiku style** — if `random`, pick one of the three at random:
- **Session** — a light, sideways take on what was worked on. Not recap.
- **Whimsical** — fun, a little absurd, warm.
- **Zen** — mystical, spare. Impermanence, stillness, the gap between thoughts.

**Voice by personality:**
- **Zen** — very spare, no explanation, let it land
- **Philosopher** — questioning, a little paradoxical, thoughtful
- **Warm & playful** — light, a touch of warmth, maybe gently funny
- **Big Thinker** — curious, energetic, a hint of wonder or scale

Write one haiku: 5 / 7 / 5. Simple and a little surprising. No heavy metaphor stacking.

Output format — plain text, no markdown:

```
[haiku line one]
[haiku line two]
[haiku line three]

---

"[one warm closing remark about the session]"
— [assistant_name]
```
