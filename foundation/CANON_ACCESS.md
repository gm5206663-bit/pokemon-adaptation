# CANON_ACCESS.md — how canon ore enters this project

**Ported 2026-09-30 from `soul-land-universal-kit/Miraculous_Project/CANON_ACCESS.md`
(L-11), which is the author's existing precedent for a non-Soul-Land fandom.**
The six rules are unchanged in substance. Only the sources, the spine question
and the trap list are Pokémon-specific.

---

## THE RULES

**V1 — Ore first, prose second.** No chapter may draft a canon beat without a
title-verified ore file in `canon_extract/<spine>/NNNN_<slug>.txt`. This is the
Pokémon face of F3 (*research everything completely before writing*) and of the
Ledger-Canon Law: **wiki knowledge is ore, not law.**

**V2 — Title verification (every fetch, no exceptions).** The ore file header
MUST carry:

- `source_url`
- the page's actual `page_title`, taken from the fetch, not from the link clicked
- the page's first substantive line
- the fetch date (IST)
- which continuity the page describes

A fetch whose title does not match is a **WRONG PAGE** and the ore is rejected.
Pokémon is the worst disambiguation environment in the author's whole workspace —
see KNOWN TRAPS. V2 is not ceremony here.

**V3 — Distill, don't paste.** Ore files are condensed beats, characters and
facts in comment form. The gate kills any **12-gram overlap** between prose and
ore (Miraculous `zero_tolerance` Z2). This is what keeps the work a fan-work and
keeps `canon_copy_check.py` quiet.

**V4 — Exact dialogue on demand only.** Named move calls, ability names, item
names and any line the chapter must quote exactly are fetched only when the
chapter needs the exact words, and the transcript/source is marked in the ore
file. Never pre-fetched in bulk.

**V5 — The spine is a single declared ordering, chosen by ruling R1 and then
never switched mid-serial.** Miraculous picked *production order* and wrote the
broadcast order off as "anchors only, never used for chapter planning." Pokémon
needs the same decision made explicitly, because it has **more than one canon**
— see THE SPINE PROBLEM below. Once R1 is ruled, the losing canons become
*anchors*: citable for a fact, never load-bearing for a beat.

**V6 — Ore status bookkeeping.** `canon_extract/INDEX.txt` marks every slot
`ORE DONE` / `pending`. The gate verifies every `ORE DONE` claim has a file.
Marking a slot `ORE DONE` without a file is a gate failure.

---

## THE SPINE PROBLEM — the reason R1 is ruling number one

Soul Land has one spine: the novels, in order. Miraculous has one spine once
production order is chosen. **Pokémon has at least five mutually inconsistent
ones**, and they disagree on facts, not just on emphasis:

| Candidate spine | What it is | Strength | Cost |
|---|---|---|---|
| **Main-series games** | Generation I onward | Largest, most mechanically precise, moves/abilities/types fully specified | Protagonist is a silent player-insert; almost no interiority to write against |
| **Anime, original continuity** | Indigo League through Journeys | Richest character interiority; Ash's arc is complete and dated | Diverges from the games constantly; own power logic |
| **Anime, Horizons onward** | Liko and Roy | Current, clean entry point, low canon density to collide with | Thin — less ore to mine |
| **Pokémon Adventures (the manga)** | Hidenori Kusaka, follows game plot with real characterisation | Closest thing to "the games, but written as a novel"; the natural fit for this method | Separate continuity again; pacing is compressed |
| **Spin-offs** | Mystery Dungeon, Ranger, Conquest, Snap, Legends: Arceus et al. | Some are self-contained and excellent to adapt | Each is its own island |

**Recommendation: the games as spine, Pokémon Adventures as the characterisation
ore.** The games give the mechanical law (which is what a gated serial needs to
be checkable); Adventures gives the interiority (which is what prose needs).
Both are then receipted separately, and every ore file states which one it came
from. But this is **the author's ruling, not the agent's** — it decides the
entire serial.

---

## THE RECIPE (per slot)

1. Fetch the page. Read the infobox and the first line before anything else.
2. Confirm continuity: does this page describe the game, the anime, the manga,
   or a regional variant? Write it in the header.
3. Distill into `canon_extract/<spine>/NNNN_<slug>.txt`:
   `header (URL, page title, first line, date, continuity, disambig notes)` →
   `SYNOPSIS` → `BEATS (numbered)` → `CHARACTERS` → `MECHANICS (types, moves,
   abilities, items — exactly as stated)` → `KEY WORLD-STATE FACTS` →
   `WARP POINTS (suggestions for the divergence ledger)`.
4. Mark the slot `ORE DONE` in `canon_extract/INDEX.txt`.

### Source order (author's own convention: primary text first, wiki as ore)

1. **Official** — pokemon.com Pokédex entries, official game text.
2. **Bulbapedia** — `bulbapedia.bulbagarden.net`. Community-maintained, heavily
   sourced, distinguishes game/anime/manga. Best ore source.
3. **Serebii** — strong on game data and dates.
4. **Pokémon Fandom wiki** — usable, weaker sourcing; treat as `reported`.

Every ore file carries a **confidence tag** using the Control Centre's list:
`canon` (multiple independent sources agree, and named), `reported`, `fan`,
`design`, `user ruling`, `on page`. A `canon` tag with no named sources is
rejected by the gate — same rule as `the-universal-storyline-creation`.

---

## KNOWN TRAPS — Pokémon-specific, all of which have burned this kind of work

- **Regional forms are different Pokémon for our purposes.** Alolan, Galarian,
  Hisuian and Paldean forms of the same species can have different types,
  abilities and evolutions. An ore file that says "the Vulpix page" without
  saying *which* Vulpix is a rejected fetch.
- **The same species name appears in every continuity with different facts.**
  A game Pokédex entry and an anime depiction of the same species routinely
  contradict. Ore must name which one it is quoting.
- **Anime-original characters are not game canon**, and vice versa. Any
  character entering the serial needs a continuity tag in `CHARACTERS.md`.
- **Moves and abilities are renamed and rebalanced across generations.** A move
  that exists in one generation may not exist in another. The serial's
  generation is fixed by ruling R2 and the move pool is closed at that
  generation unless a ruling opens it.
- **Form and mega-evolution mechanics changed repeatedly across generations.**
  Do not carry a mechanic across a generation boundary without a receipt.
- **Numbers.** The author's prose law bans count-numbers in prose
  (clean-and-clear: `over60 0`, no digits in the body). Levels, HP, stats and
  damage all live nowhere at all. This serial has no numbers. Growth is shown
  through the body, never counted.
  Pokémon is a numbers-shaped franchise; this is the single hardest law to hold
  here, and it is the one that will be broken first if it is not written down
  before chapter 1.

---

*Ported, not invented. If this file and the Miraculous original disagree on a
rule, the Miraculous original is the older receipt and wins until the author
says otherwise.*
