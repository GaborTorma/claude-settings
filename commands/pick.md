---
name: pick
description: Egy parkoló tétel kiválasztása aktuális munkának ID alapján — a nyitott munka lezárása vagy parkolása után. Használd amikor a Fejlesztő /pick-et ír, vagy egy parkoló témával akar folytatni.
argument-hint: "P02"
allowed-tools: Bash(cat .parked.md), Bash(git status *)
---

## Kontextus

- Parkoló: !`cat .parked.md`
- Git: !`git status -sb`

## 1. Melyik

- **Argumentum**: egy ID (`P02`; a `P` és a vezető nulla elhagyható: `2`). Nem létező ID → **állj meg**, jelezd.
- **Nincs argumentum**: `AskUserQuestion`, header: `Kiválasztás`, az opciók a parkoló
  tételek, a `label` pontosan a tétel sora.
- **Üres parkoló** (Kontextus-hiba `No such file`, vagy nincs tétel): csak ennyi —
  `Nincs parkoló tétel.`

## 2. A nyitott munka

Ha van aktuális munka (ebben a sessionben folyamatban, vagy commitolatlan változás a
Kontextusban): `~/.claude/rules/focus.md` 2. pontja szerint kérdezz — előbb lezárjuk,
parkoljuk (`/park`), vagy eldobjuk. A választás után folytasd.

## 3. Váltás

1. `/unpark <ID>` — a tétel kikerül a parkolóból.
2. Egy sorban: `Aktuális: <ID> · <tétel>`.
3. Indulás a `~/.claude/rules/workflow.md` útválasztása szerint (fix-jellegű → `dev`,
   feature-jellegű → `/worktree-open`); ha nem egyértelmű, melyik, kérdezz.
