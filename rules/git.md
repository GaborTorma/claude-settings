# Git workflow

- **Új projekt, ágak, merge, PR**: → [workflow.md](workflow.md).
- **Commit**: mindig a `/commit` commanddal Conventional Commits szerint.
- **Auto-commit**: Csak jóváhagyott terv / TODO önállóan végrehajtásakor, lépésenként.
- **Merge, push, PR**: sosem automatikus, csak külön commandra vagy megerősítés után.
- **Visszavonás**: `git revert <sha>` — nem patchek!
- **Tilos**: `--no-verify`, `push --force`, `reset --hard`.
