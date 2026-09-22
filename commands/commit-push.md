---
name: commit-push
description: Commit + push egy menetben, PR nélkül. Használd amikor a Fejlesztő /commit-push-t ír, vagy a kész munkát csak fel akarja tolni a remote-ra.
argument-hint: "commit üzenet vagy kontextus (opcionális)"
---

## 1. Pre-commit gate

Futtasd a projekt releváns ellenőrzéseit (lint, typecheck, unit/e2e teszt) a
`package.json` scripts, `pyproject.toml`, `Makefile` vagy a projekt `CLAUDE.md`-je
alapján. Ami nem létezik, azt hagyd ki; ami elbukik, ott **állj meg** és mutasd a
hibát — ne commitolj.

## 2. Commit

Hívd a `commit-commands:commit` commandot a `Skill` toollal; ha a *Fejlesztő*
adott argumentumot, add át `args`-ként.

## 3. Push

```bash
git push -u origin HEAD
```

Ha a remote elmozdult, `git pull --rebase` és újra push. `--force` tilos.

Végül írd ki a branch nevét és a pusholt commitok rövid SHA-ját.
