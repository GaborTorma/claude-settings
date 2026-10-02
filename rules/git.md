# Git workflow

- **Új projekt, ágak, merge, PR**: → [workflow.md](workflow.md).
- **Commit**: mindig `/commit`, Conventional Commits üzenettel.
- **Auto-commit**: Csak jóváhagyott terv / TODO önállóan végrehajtásakor, lépésenként.
- **Merge, push, PR**: sosem automatikus, csak külön commandra vagy megerősítés után.
- **Visszavonás**: `git revert <sha>` — nem patchek! Keress korábbi commitot, ha a
  *Fejlesztő* utasítása visszavonásra, visszaállításra utal.
- **Commit hash**: 8 karakteres rövid SHA `git log --reverse --abbrev=8 --format='%h %H %s' <tartomány>`
- **Tilos**: `--no-verify`, `push --force`, `reset --hard`.
