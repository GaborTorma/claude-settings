---
date: 2026-10-01
source: git-graph
kind: skill
---

# Új feature-worktree: új sessionben, ha ebben már volt mergelt PR

## Mi

Ha egy olyan sessionben döntünk új worktree (új feature) nyitása mellett,
amelyben már van mergelt PR, a `/worktree-open` ne ebben a sessionben lépjen be
a worktree-be, hanem a Claude Code app felugró ablakát (`spawn_task` chip)
jelenítse meg — arra kattintva új session indul, és abban készül az új feature.

## Miért

A git-graph sessionben egymás után három feature-kör ment le (PR #7, #8, #10,
mindegyik saját worktree-ben, `/worktree-open` → `/commit-push-pr-merge`), plusz
két `/release`. Ugyanabban a sessionben:

- a kontextus egyre hosszabb és zajosabb lett a lezárt munkák részleteivel;
- az app „Switch artifact” menüjében ott maradt minden lezárt worktree törölt
  Artifactja (a menü a session átiratából épül, a törlés nem frissíti);
- a fókusz-szabály szerint egy session = egy nyitott téma, de a lezárt témák
  terhe megmarad.

Egy új session tiszta kontextussal és tiszta Artifact-menüvel indul.

## Hogyan alkalmazd

- A `/worktree-open` elején nézd meg, volt-e már ebben a sessionben mergelt PR
  (a beszélgetésben `/merge-pr` / `/commit-push-pr-merge` futott, vagy
  `gh pr list --state merged --author @me` a session kezdete óta).
- Ha igen: ne `EnterWorktree`, hanem `spawn_task` (Claude desktop app,
  `mcp__ccd_session__spawn_task`) — cím: imperatív, a feature lényege; a prompt
  önállóan megálljon: a feladat, a javasolt ágnév (`feat/<slug>` /
  `refactor/<slug>`), és hogy az új session a `/worktree-open`-nel kezdjen. A
  *Fejlesztő* a chipre kattintva indítja.
- Ha nem (ez az első feature a sessionben): marad a mai viselkedés.
- CLI-ben, ahol nincs `spawn_task`: mondd meg, hogy új sessionben érdemes
  folytatni, és add meg a promptot másolható formában.
