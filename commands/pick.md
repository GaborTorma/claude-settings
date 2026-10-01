---
name: pick
description: Egy parkoló tétel (P-ID) vagy GitHub issue (#szám) kiválasztása aktuális munkának — a nyitott munka lezárása vagy parkolása után. Használd amikor a Fejlesztő /pick-et ír, vagy egy parkoló témával vagy issue-val akar folytatni.
argument-hint: "P02 | #12"
allowed-tools: Bash(cat .parked.md *), Bash(git status *), Bash(gh issue view *), Skill(unpark *), Skill(park *), Skill(worktree-open *)
---

## Kontextus

- Parkoló: !`cat .parked.md || true`
- Git: !`git status -sb`

## 1. Melyik

- **P-ID** (`P02`; a `P` és a vezető nulla elhagyható: `2`): parkoló tétel. Nem létező
  ID → **állj meg**, jelezd.
- **Issue** (`#12`): `gh issue view 12 --json number,title,body,labels,state,url`.
  Lezárt vagy nem létező → **állj meg**, jelezd.
- **Nincs argumentum**: `AskUserQuestion`, header: `Kiválasztás`, az opciók a parkoló
  tételek, a `label` pontosan a tétel sora. Issue-hoz: `/issues`.
- **Üres parkoló** (Kontextus-hiba `No such file`, vagy nincs tétel) és nincs
  argumentum: csak ennyi — `Nincs parkoló tétel.`

## 2. A nyitott munka

Ha van aktuális munka (ebben a sessionben folyamatban, vagy commitolatlan változás a
Kontextusban): `~/.claude/rules/focus.md` 2. pontja szerint kérdezz — előbb lezárjuk,
parkoljuk (`/park`), vagy eldobjuk. A választás után folytasd.

## 3. Váltás

1. **P-ID**: `/unpark <ID>` — a tétel kikerül a parkolóból. **Issue**: nyitva marad; a
   száma a munka végéig a kontextusban marad (→ `/commit` Footer, `/pull-request` Issue).
2. Egy sorban: `Aktuális: <ID> · <tétel>`, ill. `Aktuális: [#<szám>](<URL>) · <cím>`.
3. Indulás a `~/.claude/rules/workflow.md` útválasztása szerint (fix-jellegű → `dev`,
   feature-jellegű → `/worktree-open`). Issue-nál a címke dönt (`fix` / `feature`), a
   slug a címéből; ha nincs címke vagy nem egyértelmű, kérdezz.
