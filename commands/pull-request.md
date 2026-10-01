---
name: pull-request
description: Worklog, az aktuális ág pusholása, majd PR nyitása vagy frissítése — a leírásban az ágon létrejött worklogokkal. Használd amikor a Fejlesztő /pull-request-et (vagy /pr-t) ír, vagy egy ág munkáját PR-ba akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
allowed-tools: Bash(git branch --show-current), Bash(gh pr view *), Bash(git diff *), Bash(git rev-parse *), Skill(worklog *), Skill(push *)
---

## Kontextus

- Argumentum: $ARGUMENTS
- Ág: !`git branch --show-current`
- PR: !`gh pr view --json number,url,state 2>/dev/null || echo "NINCS"`

Ha a Kontextus szerint a `main`-en állsz, **állj meg — ez hiba**: a `main`-en
sosem dolgozunk (→ `~/.claude/rules/workflow.md`). Jelezd a *Fejlesztő*nek.

## 1. Worklog

`/worklog`

## 2. Push

`/push`

## 3. Leírás

Magyarul, ebben a sorrendben; az üres szakasz elmarad.

- **Összefoglaló**, 2–3 mondat: mi változott és miért — a miért az első
  mondatban (az **Argumentum** sor a kontextus).
- **Issue**: ha a munka egy issue-ból indult (`/pick #<szám>`, vagy a *Fejlesztő*
  megnevezte az **Argumentum** sorban vagy a beszélgetésben), az összefoglaló alá `Closes #<szám>` — a
  merge lezárja. Ha nem volt, a sor elmarad; ne keress és ne találd ki.
- **`## Ellenőrzés`**: csak ami ténylegesen lefutott — a `/check` eredménye (a
  `/commit` Check-sora vagy a CI), és amit kézzel megnéztünk. UI-változásnál
  képernyőkép.
- **`## Élesítés`**: ami a deploy előtt vagy közben teendő — migráció, új vagy
  megváltozott env-változó, ütemezett feladat, sorrend, rollback. Forrás a diff
  (migrációs könyvtár, `.env.example`), a worklogok és a *Fejlesztő*; ne találd ki.
  A `/merge-pr` ezt a merge commitba viszi, a `/release` onnan gyűjti.
- **`## Worklog`**: az ágon létrejött worklog-fájlok linkje, a fájl
  `# <cím>` sorával: `- [<cím>](<repó URL>/blob/<HEAD SHA>/.worklog/<fájl>)`.
  SHA-ra mutató link, mert az ág a merge után törlődik:

  ```bash
  git diff --name-only --diff-filter=A origin/main...HEAD -- .worklog/
  git rev-parse HEAD
  ```

## 4. PR

- **Nincs nyitott PR** → `gh pr create --title "<cím>" --body-file <leírás>`. A cím
  angol, Conventional Commits formájú, az **Argumentum** sorból vagy a változásból.
- **Van nyitott PR** (`state: OPEN`) → `gh pr edit --body-file <leírás>`.

Végül írd ki a PR számát és URL-jét.
