# claude-settings — projekt-memória

A gyökér `CLAUDE.md` a **globális** user memory (symlink → `~/.claude/CLAUDE.md`),
ezért a repó saját tényei ide kerülnek.

- **Check**: nincs lint, typecheck vagy teszt. Ha a `settings.user.json` változott:
  `python3 -m json.tool settings.user.json` — managed drop-in, érvénytelen JSON-nal a Claude Code nem indul.
- **Parancsok**: `make install` / `make link` / `make update` / `make sync` (lásd `README.md`).
- **Inbox**: munka közben nézd az `inbox/`-ot (a `deferred/`-et is). Ami az aktuális
  témához kapcsolódik, hozd be a munkába; amit megcsináltunk belőle, a bejegyzését töröld
  ugyanabban a commitban.

## Git

- A globális `workflow.md` utasításai ebben a repóban **nem érvényesek**.
- Minden commit közvetlenül a `main`-re megy — nincs `dev`, nincs feature-ág, nincs PR.
