---
name: worktree-open
description: Feature-jellegű munka indítása saját worktree-ben — szabad ágnév, EnterWorktree, feat/ vagy refactor/ ág, függőségek; meglévő worktree-be visszalép. Használd amikor a Fejlesztő /worktree-open-t ír, vagy feature-jellegű munkát kezd.
argument-hint: "<slug> vagy a feladat leírása (opcionális)"
allowed-tools: Bash(git worktree list *), Bash(git branch --list *), Bash(git ls-remote *), Bash(gh pr list *)
---

## Kontextus

- Worktree-k: !`git worktree list`
- Helyi ágak: !`git branch --list 'feat/*' 'refactor/*'`
- Remote ágak: !`git ls-remote --heads origin 'refs/heads/feat/*' 'refs/heads/refactor/*'`
- PR-ok (minden állapot): !`gh pr list --state all --limit 200 --json headRefName -q '.[].headRefName'`

## 1. Ágnév

- **Típus**: `refactor`, ha tisztán refactor; minden más feature-jellegű munka
  `feat` (→ `~/.claude/rules/workflow.md` / Útválasztás).
- **`<slug>`**: a *Fejlesztő* argumentumából vagy a feladatból, a `workflow.md`
  szerint (angol, ASCII kebab-case, 2–4 szó).
- **Van már ilyen worktree** a Kontextusban (`.claude/worktrees/<slug>`) → visszalépés:
  `EnterWorktree`, `path: .claude/worktrees/<slug>`, majd a **3. Létrehozás** 3. lépése — és kész.
- **Foglalt** (helyi ág, remote ág vagy bármilyen PR a Kontextusban) → másik slug
  (pl. `-2` utótag).

## 2. Ellenőrzés

1. A `.gitignore`-ban benne van a `.claude/worktrees/`.
2. A gitignore-olt, de a worktree-ben is szükséges fájlok (pl. `.env`) benne
   vannak a `.worktreeinclude`-ban (repó gyökér, `.gitignore` szintaxis).

Ami hiányzik, azt a fő checkoutban pótold, és commitold `/commit`-tal.

## 3. Létrehozás

1. `EnterWorktree`, `name: <slug>` — a session átkerül a `.claude/worktrees/<slug>`-be,
   `worktree-<slug>` ágra, `origin/main`-ről.
2. `git branch -m <típus>/<slug>` — még az első push előtt, mert a PR az ágnévhez kötődik.
3. Az `EnterWorktree` elvileg átmásolja a `.worktreeinclude` fájljait. Ami a
   worktree-ben hiányzik, azt a fő checkoutból másold át; a meglévőt ne írd felül,
   a tartalmukat ne olvasd be:

   ```bash
   root=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
   git -C "$root" ls-files --others --ignored --exclude-from=.worktreeinclude |
     while read -r f; do
       [ -e "$f" ] || { mkdir -p "$(dirname "$f")"; cp -p "$root/$f" "$f"; echo "átmásolva: $f"; }
     done
   ```

4. Függőségek telepítése a stack szerint.

Végül írd ki az ág nevét, a worktree útvonalát és az átmásolt fájlokat.
