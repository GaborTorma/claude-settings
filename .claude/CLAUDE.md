# claude-settings — projekt-memória

A gyökér `CLAUDE.md` a **globális** user memory (symlink → `~/.claude/CLAUDE.md`),
ezért a repó saját tényei ide kerülnek.

- **Check**: nincs lint, typecheck vagy teszt. Ha a `settings.user.json` változott:
  `python3 -m json.tool settings.user.json` — managed drop-in, érvénytelen JSON-nal a Claude Code nem indul.
- **Parancsok**: `make install` / `make update` / `make push` (lásd `README.md`).
- **Inbox**: munka közben nézd az `inbox/`-ot (a `deferred/`-et is). Ami az aktuális
  témához kapcsolódik, hozd be a munkába; amit megcsináltunk belőle, a bejegyzését töröld
  ugyanabban a commitban.

## Git

- **Mindig a `main`-en dolgozunk**: nincs `dev`, nincs feature-ág (`feat/`, `refactor/`,
  worktree), nincs PR — minden commit közvetlenül a `main`-re megy.
- Felmentés a **teljes** globális `workflow.md` alól (ágak, útválasztás, Init, Fix- és
  Feature-munka, merge, kiadás) — ebben a repóban egyik utasítása sem érvényes.
- **Commit csak jóváhagyás után**: a változás a munkakönyvtárban marad, amíg a _Fejlesztő_ olvasta.
