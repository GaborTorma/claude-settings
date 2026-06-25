# Git workflow

- **Új projekt**: `git init` → `.gitignore` → `git commit -m "Initial commit"`.
- **Commit**: automtikusan a tesztelt és **JÓVÁHAGYOTT** TODO lépések után.
- **Auto-commit**: Csak auto-plan/TODO végrejatáskor, ha nincs Fejlesztő-interakció.
- **Visszavonás**: `git revert <sha>` — nem patchek!
- **Tilos**: `--no-verify`, `push --force` main-re, `reset --hard` vagy `pr` megerősítés nélkül.

## Pre-commit gate

Commit előtt minden változáshoz le kell futtatni a releváns ellenőrzéseket (**lint, typecheck, unit/e2e tests**). Ha a projektben létezik az adott eszköz, **kötelező** futtatni — ha hiányzik, kihagyható.

**Detektálás**: `package.json` scripts, `pyproject.toml`, `Makefile`, vagy projekt CLAUDE.md alapján. Ha nem egyértelmű mi a parancs, kérdezd meg egyszer és jegyezd meg.

## Conventional Commits

Formátum: `<type>(<scope>): <subject>` — scope opcionális, kebab-case.

**Típusok:**

| Type       | Jelentés                            | Semver |
| ---------- | ----------------------------------- | ------ |
| `feat`     | új feature                          | MINOR  |
| `fix`      | bugfix                              | PATCH  |
| `perf`     | performance                         | PATCH  |
| `refactor` | refactor (nincs viselkedésváltozás) | —      |
| `docs`     | dokumentáció                        | —      |
| `style`    | formázás (nincs kódváltozás)        | —      |
| `test`     | tesztek                             | —      |
| `build`    | build rendszer                      | —      |
| `deploy`   | deploy rendszer                     | —      |
| `chore`    | karbantartás                        | —      |
| `revert`   | korábbi commit visszavonása         | —      |

**Subject szabályok:**

- Imperatív, jelen idő: `add`, `fix` — ne `added`/`fixed`.
- Max 100 karakter, kisbetűvel, végén nincs pont.
- Konkrét (`feat: improve API` ❌ → `feat: add rate limiting to auth endpoints` ✅).

**Breaking change**: `feat!:` vagy `BREAKING CHANGE:` footer a body-ban.

**Példák:**

```
feat(auth): add OAuth2 login support
fix(api): handle empty response from external service
refactor: extract user service for testability
feat!: remove deprecated v1 API endpoints
```

**Body (opcionális)**: akkor írj, ha a _miért_ nem triviális. Magyarázd a motivációt, ne a mit.

**Footer**: `Fixes #123`, `Closes #456`, `BREAKING CHANGE: ...`.
