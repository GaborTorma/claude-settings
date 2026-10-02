---
name: commit
description: Git commit a jelenlegi változásokból — /check után, Conventional Commits üzenettel; tisztán elkülönülő témák külön commitba. Használd amikor a Fejlesztő /commit-ot ír, vagy egy másik command commitot kér.
argument-hint: 'commit üzenet vagy kontextus (opcionális)'
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git branch --show-current), Bash(git log *), Bash(git rev-parse *), Bash(git add *), Bash(git commit *), Skill(typo *), Skill(check *)
---

## Kontextus

- Argumentum: $ARGUMENTS
- Git status: !`git status`
- Aktuális ág: !`git branch --show-current`
- Utolsó commitok: !`git log --oneline -10 2>/dev/null || echo "NINCS"`

## 1. Van mit commitolni?

Ha a munkakönyvtár tiszta: nincs commit, nincs check — ez nem hiba, a hívó
command folytatja.

Az **Utolsó commitok** sor `NINCS`: üres repó, ez lesz az első commit.

## 2. `/typo`

## 3. `/check`

## 4. Commit

A `/typo` és a `/check` módosíthat fájlokat (`format --write`, `lint --fix`), ezért a csoportosítás előtt kérd le a friss állapotot:

```bash
git status --short
git diff --cached
git diff
```

Témánként (nem fájlonként) egy commit, Conventional Commits üzenettel:

- **Csoportosítás**: a változásokat témák szerint válaszd szét. Ha a témák
  **fájlszinten** tisztán elkülönülnek, mindegyik külön commit a saját típusával
  (`git add <fájlok>` → `git commit`), logikus sorrendben.
- **Egy fájlon belül kevert témák** → egy commit. Ha a szétválasztás fontos lenne,
  kérdezz rá a *Fejlesztő*nél.
- **Az Argumentum sor**: ha fájlokat nevez meg, csak azok kerülnek bele; ha
  szöveget ad, abból jön az üzenet vagy a kontextusa.

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

- Angolul, imperatív, jelen idő: `add`, `fix` — ne `added`/`fixed`.
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

**Body (opcionális)**: magyarul; akkor írj, ha a _miért_ nem triviális. Magyarázd a motivációt, ne a mit.

**Footer**: `BREAKING CHANGE: ...` (→ Breaking change). `Fixes #<szám>` csak ha a munka
issue-ból indult (`/pick #<szám>`), vagy a *Fejlesztő* megnevezte — soha ne találd ki.
Fix-jellegű munkánál ez zárja le az issue-t, amikor a commit a `main`-re kerül.

## 5. Válasz

Mindig ebben a formában!

Egy commit esetén:
```markdown
Check: lint ✓ · typecheck ✓ · test ✓ · format ✓

Commit: `[62ad1820]` · <commit subject>
```

Több commit esetén:
```markdown
Check: lint ✓ · typecheck ✓ · test ✓ · format ✓

Commits:
- `[c96661da]` · <commit subject>
- `[62ad1820]` · <commit subject>
```

- **Typo-sorok**: ha a `/typo` talált valamit, a sorai (`Typo:` / `Typo?:`) a Check-sor alatt.
- **Check-sor**: a `/check` válasza, egyszer, az összes commit előtt; ha nem futott ellenőrzés, elmarad.
- **Nem volt mit commitolni**: csak ennyi — `Nincs új commit.`
- **Egy check elbukott**: `Check: <ellenőrzés> ✗`, alatta üres sor, majd Commit-sor helyett:
  `Hiba: <röviden a hiba lényege>`
