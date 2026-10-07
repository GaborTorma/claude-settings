---
name: worktree-open
description: Feature-jellegű munka indítása saját worktree-ben — szabad ágnév, EnterWorktree, feat/ vagy refactor/ ág, függőségek; meglévő worktree-be visszalép. Használd amikor a Fejlesztő /worktree-open-t ír, vagy feature-jellegű munkát kezd.
argument-hint: "<slug> vagy a feladat leírása (opcionális)"
allowed-tools: Bash(git worktree list *), Bash(git branch --list *), Bash(git ls-remote *), Bash(gh pr list *), Bash(git branch -m *), Bash(git rev-parse *), Bash(git ls-files *), Bash(ls *), Bash(mkdir -p *), Bash(cp -p *), Bash(pnpm install), Bash(uv sync), EnterWorktree, mcp__ccd_directory__change_directory, Skill(commit *)
---

## Kontextus

- Argumentum: $ARGUMENTS
- Worktree-k: !`git worktree list`
- Helyi ágak: !`git branch --list 'feat/*' 'refactor/*'`

## 1. Ágnév

- **Típus**: `refactor`, ha tisztán refactor; minden más feature-jellegű munka
  `feat` (→ `~/.claude/rules/workflow.md` / Útválasztás).
- **`<slug>`**: az **Argumentum** sorból vagy a feladatból, a `workflow.md`
  szerint (angol, ASCII kebab-case, 2–4 szó).
- **Van már ilyen worktree** a Kontextusban (`.claude/worktrees/<slug>`) → visszalépés:
  `EnterWorktree`, `path: .claude/worktrees/<slug>`, majd a **3. Létrehozás** 3. lépése és a **4. Az app cwd-je** — és kész.
- **Foglalt** → másik slug (pl. `-2` utótag). Foglalt, ha a slug bármelyik típussal
  (`feat/<slug>`, `refactor/<slug>`) létezik helyi ágként (Kontextus), remote ágként vagy
  PR-ként (bármilyen állapotban):

  ```bash
  git ls-remote --heads origin refs/heads/feat/<slug> refs/heads/refactor/<slug>
  gh pr list --state all --head feat/<slug> --json number
  gh pr list --state all --head refactor/<slug> --json number
  ```

  Üres kimenet / `[]` → szabad. Ha nincs remote, a hiba nem akadály: csak a helyi ágak számítanak.

## 2. Ellenőrzés

1. A `.gitignore`-ban benne van a `.claude/worktrees/`.
2. A gitignore-olt, de a worktree-ben is szükséges fájlok (pl. `.env`) benne
   vannak a `.worktreeinclude`-ban (repó gyökér, `.gitignore` szintaxis).

Ami hiányzik, azt a fő checkoutban pótold, és commitold `/commit`-tal.

3. Ha van `.worktreeinclude`: még a fő checkoutban jegyezd fel, mely fájlok
   tartoznak bele, és a fő checkout abszolút útját (`git rev-parse --show-toplevel`):

   ```bash
   git ls-files --others --ignored --exclude-from=.worktreeinclude
   ```

   Az `EnterWorktree` után ez már nem futtatható: a Bash eszköz worktree-ben a más
   mappára mutató (`git -C`) és a `$(…)`-os git-hívást visszautasítja.

## 3. Létrehozás

1. `EnterWorktree`, `name: <slug>` — a session átkerül a `.claude/worktrees/<slug>`-be,
   `worktree-<slug>` ágra, `origin/main`-ről.
2. `git branch -m <típus>/<slug>` — még az első push előtt, mert a PR az ágnévhez kötődik.
3. Az `EnterWorktree` elvileg átmásolja a `.worktreeinclude` fájljait. A **2. Ellenőrzés**
   3. pontjának listájából ami a worktree-ben hiányzik (`ls <fájl>`), azt fájlonként
   másold át a fő checkoutból — git és `$(…)` nélkül, abszolút úttal; a meglévőt ne írd
   felül, a tartalmukat ne olvasd be:

   ```bash
   cp -p <fő checkout>/<fájl> <fájl>    # almappánál előtte: mkdir -p <mappa>
   ```

4. Függőségek telepítése a stack szerint.

## 4. Az app cwd-je

Csak a Claude desktop appban (ha a `mcp__ccd_directory__change_directory` elérhető).
Az `EnterWorktree` az app session-fájljában (`cwd`) a fő checkoutot hagyja; erre épül
pl. a git-graph „saját” worktree-je. Utolsó lépésként:
`mcp__ccd_directory__change_directory` a worktree abszolút útjára
(`git rev-parse --show-toplevel`). A kör végén hat — utána ebben a körben ne futtass
semmit, ami a cwd-re épül.

A **play gomb** (```` ```bash ```` blokk) egy tartós shellben fut, amely megőrzi a
`cd`-t, de a munkakönyvtárát sem az `EnterWorktree`, sem a `change_directory` nem állítja
át (mérve, 2026.10.06.). Ezért a válasz végén adj egy blokkot, és kérd a *Fejlesztő*t,
hogy egyszer nyomja meg:

```bash
cd <a worktree abszolút útja>
```

Végül írd ki az ág nevét, a worktree útvonalát és az átmásolt fájlokat.
