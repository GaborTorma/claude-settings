---
name: pr-button
description: A Claude app Create PR gombja a saját láncunkon — /commit, majd /pull-request. Használd, amikor egy üzenetben <create-pr-command> blokk érkezik; a blokk lépései helyett ez fut.
user-invocable: false
allowed-tools: Bash(git branch --show-current), Skill(commit *), Skill(pull-request *)
---

## Kontextus

- Ág: !`git branch --show-current`

A `<create-pr-command>` blokk 1–3. lépése (commit, push, `gh pr create`) helyett a
saját commandok futnak. A blokkból csak ezt vedd át:

- **Draft**: ha a blokk draftot kér („as a draft”, `--draft`).
- A végén a **`<pr-created>` tag**: erről köti az app a PR-t a sessionhöz.

Ha az ág `dev`, **állj meg**: a `dev` PR nélkül megy a mainbe (`/commit-push-merge`,
→ `~/.claude/rules/workflow.md`). Jelezd a *Fejlesztő*nek.

Sorban — ha egy lépés megállt, **itt is állj meg**. A commandokat a Skill eszközzel
hívd meg:

1. `/commit`
2. `/pull-request` (`args`: `--draft`, ha a blokk draftot kér)
3. A PR URL-je külön sorban: `<pr-created><URL></pr-created>`

Minden lépés válaszát a lépés saját formájában írd ki, sorrendben; utána a tag.
