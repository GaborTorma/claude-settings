---
name: push
description: Push a remote-ra; ha még nincs remote, GitHub-repót hoz létre — nevet és láthatóságot javasol, és kérdésként felteszi. Használd amikor a Fejlesztő /push-t ír, vagy a repót először vinné fel GitHubra.
argument-hint: "repó neve (opcionális)"
allowed-tools: Bash(git remote get-url *), Bash(git branch --show-current), Bash(git status *)
---

## Kontextus

- Remote: !`git remote get-url origin || true`
- Ág: !`git branch --show-current`
- Állapot: !`git status -sb`

## 1. Van remote?

A Kontextus **Remote** sora:

- **URL** → **3. Push**.
- **Hiba** (`No such remote`) → **2. Repó létrehozása**.

## 2. Repó létrehozása

### Javaslat

- **Név**: a *Fejlesztő* argumentuma; ha nincs, a projekt neve (`package.json`
  / `pyproject.toml` `name`, különben a mappa neve), kebab-case-re alakítva.
- **Owner**: `gh api user -q .login`; ha van szervezet (`gh api user/orgs -q '.[].login'`),
  az is opció.
- **Láthatóság**: alapból **private**. Publikust csak akkor javasolj, ha a repó
  nyílt forrásúnak látszik (pl. `LICENSE` nyílt licenccel), és indokold.

Publikus javaslat előtt nézd meg, került-e titok a történetbe:

```bash
git log --all --name-only --format= | grep -E '(^|/)(\.env(\..+)?|credentials\.json|.+\.(pem|key))$' | grep -v '\.env\.example$'
```

Találat esetén csak private javasolható, és a találatot mutasd meg.

### Kérdés

Az `AskUserQuestion` toollal, egy hívásban:

1. **Név** — a javaslat (Recommended) + 1–2 alternatíva; a *Fejlesztő* az „Other”
   mezőben mást is írhat.
2. **Láthatóság** — Private / Public, a javasolt elöl, (Recommended) jelöléssel, az
   indokkal a leírásban.
3. **Owner** — csak ha van szervezet.

Ha a név foglalt (`gh repo view <owner>/<név>` sikeres), kérdezz újra.

### Létrehozás

```bash
gh repo create <owner>/<név> --private|--public --source . --remote origin
```

## 3. Push

- **Most létrehozott remote**: minden helyi ág felmegy, upstreammel:
  `git push -u origin --all`
- **Meglévő remote**: van-e mit pusholni — a Kontextus **Állapot** sora (`[ahead N]`,
  vagy upstream nélküli ág → pusholandó). Fetch nincs: ha a remote közben
  elmozdult, a push elutasítja, és csak akkor kell `git pull --rebase`.

  - Nincs `[ahead N]` (és van upstream) → **állj meg**: nincs mit pusholni. Ha a munkakönyvtár nem tiszta, jelezd,
    hogy commitolatlan változás van (az nem megy fel).
  - Egyébként az aktuális ág: `git push -u origin HEAD`. Ha a remote elmozdult:
    `git pull --rebase`, majd újra push.

`--force` tilos. Push előtt jegyezd fel ágonként a remote korábbi állását
(`git rev-parse @{u}`; új ágnál / új repónál nincs ilyen).

## 4. Válasz

Mindig ebben a formában:

```markdown
Új <private|public> repó létrehozva: [[<owner>/<név>]](<repó URL>).

Push: `<ág>` (`<előtte>` → `<utána>`)

- [`[2a13d131]`](<repó URL>/commit/<teljes SHA>) · <commit subject>
- ...
```

- **„Új repó…” sor**: csak ha a 2. lépés most hozta létre; meglévő repónál nincs repó-sor.
- **Repó URL**: a Kontextus Remote sorából
  (`git@github.com:<owner>/<név>.git` → `https://github.com/<owner>/<név>`).
- **Ágak**: minden pusholt ágnak saját blokk; új ágnál `<előtte>` helyén `új ág`.
- **Commitok**: a pusholt tartomány, `<előtte>..<utána>` (új ágnál `<utána>` önmagában).
  20 fölött csak az utolsó 20, a lista végén új sorban: `… és még N commit`.
