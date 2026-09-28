# claude-settings — projekt-memória

A gyökér `CLAUDE.md` a **globális** user memory (symlink → `~/.claude/CLAUDE.md`),
ezért a repó saját tényei ide kerülnek.

- **Pre-commit gate**: nincs lint, typecheck vagy teszt. Ha a `settings.user.json` változott:
  `python3 -m json.tool settings.user.json` — managed drop-in, érvénytelen JSON-nal a Claude Code nem indul.
- **Parancsok**: `make install` / `make link` / `make update` / `make sync` (lásd `README.md`).

## Git

- A globális `workflow.md` utasításai ebben a repóban **nem érvényesek**.
- Minden commit közvetlenül a `main`-re megy — nincs `dev`, nincs feature-ág, nincs PR.
