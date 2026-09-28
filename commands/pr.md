---
name: pr
description: Worklog, az aktuális ág pusholása, majd PR nyitása vagy frissítése — a leírásban az ágon létrejött worklogokkal. Használd amikor a Fejlesztő /pr-t ír, vagy egy ág munkáját PR-ba akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
allowed-tools: Bash(git branch --show-current), Bash(gh pr view *)
---

## Kontextus

- Ág: !`git branch --show-current`
- PR: !`gh pr view --json number,url,state`

Ha a Kontextus szerint a `main`-en állsz, **állj meg — ez hiba**: a `main`-en
sosem dolgozunk (→ `~/.claude/rules/workflow.md`). Jelezd a *Fejlesztő*nek.

## 1. Worklog

`/worklog`

## 2. Push

`/push`

## 3. Leírás

- A változás rövid összefoglalója (a *Fejlesztő* argumentuma a kontextus).
- Alatta `## Worklog`, benne az ágon létrejött worklog-fájlok linkje, a fájl
  `# <cím>` sorával: `- [<cím>](<repó URL>/blob/<HEAD SHA>/.worklog/<fájl>)`.
  SHA-ra mutató link, mert az ág a merge után törlődik:

  ```bash
  git diff --name-only --diff-filter=A origin/main...HEAD -- .worklog/
  git rev-parse HEAD
  ```

## 4. PR

- **Nincs nyitott PR** → `gh pr create --title "<cím>" --body-file <leírás>`. A cím
  Conventional Commits formájú, a *Fejlesztő* argumentumából vagy a változásból.
- **Van nyitott PR** (`state: OPEN`) → `gh pr edit --body-file <leírás>`.

Végül írd ki a PR számát és URL-jét.
