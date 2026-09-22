---
name: merge
description: Commit + push + PR + merge a mainbe egy menetben. Használd amikor a Fejlesztő /merge-öt ír, vagy egy kész branch munkáját azonnal a mainbe akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
---

Az aktuális branch munkáját végigviszed commitig, PR-ig és merge-ig. A merge
**azonnali** — nem várja meg a CI-t —, ezért a pre-commit gate itt nem
opcionális.

## 1. Pre-commit gate

Futtasd a projekt releváns ellenőrzéseit (lint, typecheck, unit/e2e teszt) a
`package.json` scripts, `pyproject.toml`, `Makefile` vagy a projekt `CLAUDE.md`-je
alapján. Ami nem létezik, azt hagyd ki; ami létezik és elbukik, ott **állj meg**
és mutasd a hibát — ne commitolj.

## 2. Commit, push, PR

Hívd a `commit-commands:commit-push-pr` commandot a `Skill` toollal. Ha a
*Fejlesztő* adott argumentumot, add át `args`-ként — abból lesz a PR kontextusa.

A command dönti el, kell-e új branch (ha `main`-en állunk), megírja a commitot,
pushol és megnyitja a PR-t.

## 3. Merge

```bash
gh pr merge --merge --delete-branch
```

- `--merge`: merge commit, a branch commitjai megmaradnak a gráfon
- `--delete-branch`: remote és lokális branch törlése

Ne használj `--admin`-t, és ne kerüld meg a branch protectiont. Ha a `gh` azt
mondja, a PR nem mergelhető (konfliktus, kötelező review, blokkoló check),
**állj meg** és írd le, mi a blokkoló — onnan a *Fejlesztő* dönt.

## 4. Lezárás

```bash
git checkout main && git pull
```

A `gh` ezt többnyire magától megteszi, de idempotens — futtasd le, hogy a
munkakönyvtár biztosan a friss `main`-en álljon.

Végül írd ki a PR számát és URL-jét, valamint a merge commit rövid SHA-ját.
