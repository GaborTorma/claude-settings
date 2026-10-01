---
name: commit
description: Git commit a jelenlegi változásokból — /check után, Conventional Commits üzenettel; tisztán elkülönülő témák külön commitba. Használd amikor a Fejlesztő /commit-ot ír, vagy egy másik command commitot kér.
argument-hint: 'commit üzenet vagy kontextus (opcionális)'
allowed-tools: Bash(git status *), Bash(git diff *), Bash(git branch --show-current), Bash(git log *), Bash(git rev-parse *), Bash(git add *), Bash(git commit *), Skill(check *)
---

## Kontextus

- Git status: !`git status`
- Diff (staged és unstaged): !`git diff HEAD || true`
- Aktuális ág: !`git branch --show-current`
- Utolsó commitok: !`git log --oneline -10 || true`

## 1. Van mit commitolni?

Ha a munkakönyvtár tiszta: nincs commit, nincs check — ez nem hiba, a hívó
command folytatja.

Üres repóban (még nincs commit) a **Diff** és az **Utolsó commitok** sor hibaüzenet
(`does not have any commits yet`, `ambiguous argument 'HEAD'`) — a változásokat ilyenkor
a **Git status** mutatja.

## 2. Check

`/check`. Ha elbukik, **állj meg**!

## 3. Commit

Témánként (nem fájlonként) egy atomic commit, Conventional Commits üzenettel:

- **Csoportosítás**: a változásokat témák szerint válaszd szét. Ha a témák
  **fájlszinten** tisztán elkülönülnek, mindegyik külön commit a saját típusával
  (`git add <fájlok>` → `git commit`), logikus sorrendben.
- **Egy fájlon belül kevert témák** → egy commit. Ha a szétválasztás fontos lenne,
  kérdezz rá a *Fejlesztő*nél.
- **Merge folyamatban** (`git rev-parse -q --verify MERGE_HEAD` sikeres): nincs témabontás — egy commit a git
  alapértelmezett merge-üzenetével (`git commit --no-edit`).
- **A *Fejlesztő* argumentuma**: ha fájlokat nevez meg, csak azok kerülnek bele; ha
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

## 4. Válasz

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

- **Check-sor**: a `/check` válasza, egyszer, az összes commit előtt; ha nem futott ellenőrzés, elmarad.
- **Nem volt mit commitolni**: csak ennyi — `Nincs új commit.`
- **Egy check elbukott**: `Check: <ellenőrzés> ✗`, alatta üres sor, majd Commit-sor helyett:
  `Hiba: <röviden a hiba lényege>`
