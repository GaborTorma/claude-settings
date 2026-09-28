---
name: commit
description: Egyetlen git commit a jelenlegi változásokból — pre-commit gate után, Conventional Commits üzenettel. Használd amikor a Fejlesztő /commit-ot ír, vagy egy másik command commitot kér.
argument-hint: 'commit üzenet vagy kontextus (opcionális)'
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*)
---

## Kontextus

- Git status: !`git status`
- Diff (staged és unstaged): !`git diff HEAD`
- Aktuális ág: !`git branch --show-current`
- Utolsó commitok: !`git log --oneline -10`

## 1. Van mit commitolni?

Ha a munkakönyvtár tiszta: nincs commit, nincs gate — ez nem hiba, a hívó
command folytatja.

## 2. Pre-commit gate

Commit előtt minden változáshoz le kell futtatni a releváns ellenőrzéseket
(**lint, typecheck, unit/e2e tests**). Ha a projektben létezik az adott eszköz,
**kötelező** futtatni — ha hiányzik, kihagyható.

**Detektálás**: `package.json` scripts, `pyproject.toml`, `Makefile`, vagy projekt
`CLAUDE.md` alapján. Ha nem egyértelmű mi a parancs, kérdezd meg egyszer és
jegyezd meg.

Ha elbukik, **állj meg** és mutasd a hibát — ne commitolj.

## 3. Commit

Egyetlen commit, Conventional Commits üzenettel. Ha a _Fejlesztő_ adott
argumentumot, abból jön az üzenet vagy a kontextusa.

Formátum: `<type>(<scope>): <subject>` — scope opcionális, kebab-case.

**Típusok:**

| Type       | Jelentés                            |
| ---------- | ----------------------------------- |
| `feat`     | új feature                          |
| `fix`      | bugfix                              |
| `perf`     | performance                         |
| `refactor` | refactor (nincs viselkedésváltozás) |
| `docs`     | dokumentáció                        |
| `style`    | formázás (nincs kódváltozás)        |
| `test`     | tesztek                             |
| `build`    | build rendszer                      |
| `deploy`   | deploy rendszer                     |
| `chore`    | karbantartás                        |
| `revert`   | korábbi commit visszavonása         |

**Semver**: breaking change → MAJOR, `feat` → MINOR, minden más → PATCH.

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

## 4. Válasz

Mindig ebben a formában:

```markdown
Check: lint ✓ · typecheck ✓ · test ✓ · format ✓
Commit: `[c96661da]` · <commit subject>
```

- **Check-sor**: csak ha futott ellenőrzés — a ténylegesen lefutottak.
- **Nem volt mit commitolni**: csak ennyi — `Nincs új commit.`
- **Egy check elbukott**: `Check: <ellenőrzés> ✗`, alatta Commit-sor helyett: Hiba: röviden a hiba lényege
