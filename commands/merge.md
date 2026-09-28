---
name: merge
description: Az aktuális ág mergelése a mainbe — feature-ágnál a PR-t próba-merge és gate után, dev ágnál lokális fast-forwarddal —, majd takarítás. Használd amikor a Fejlesztő /merge-et ír, vagy egy kész ágat a mainbe akar vinni.
allowed-tools: Bash(git branch --show-current), Bash(gh pr view *)
---

## Kontextus

- Ág: !`git branch --show-current`
- PR: !`gh pr view --json number,url,state`

A command meghívása maga a merge-engedély — de csak akkor, ha a lépések
hibátlanul lefutnak. A `main` pusholása nem deploy — kiadás csak `/release`-szel.
`--force` és `--admin` tilos.

- **`main`** → **állj meg — ez hiba**.
- **Van nyitott PR** → **A. PR-merge**.
- **`dev`, PR nélkül** → **B. Lokális merge**.
- **Más ág, PR nélkül** → **állj meg**: előbb `/pr`.

A pre-commit gate mindkét útvonalon a `~/.claude/commands/commit.md` /
2. Pre-commit gate szerint fut.

## A. PR-merge

### 1. Próba-merge

A PR csak a saját commitjait tartalmazza; a `main` az ágba nem kerül be. Ha a
`main` a leválás óta elmozdult, a merge eredményét próbaként teszteld:

```bash
git fetch
git merge-base --is-ancestor origin/main HEAD   # 0: nem mozdult → ugorj a 2. lépésre
git merge --no-commit --no-ff origin/main
```

- **Ütközés** → `git merge --abort`, majd **3. Ütközés**.
- **Párhuzamos migráció**: ha a projektnek van migrációs könyvtára (projekt
  `CLAUDE.md` vagy stack skill szerint, pl. `drizzle/`, `migrations/`), és a közös
  ős óta az `origin/main` és az ág is hozott új migrációt → `git merge --abort`,
  **állj meg**: a sorrendről a *Fejlesztő* dönt.

  ```bash
  base=$(git merge-base origin/main HEAD)
  git diff --name-only --diff-filter=A $base origin/main -- <migrációs könyvtár>
  git diff --name-only --diff-filter=A $base HEAD -- <migrációs könyvtár>
  ```

- **Pre-commit gate** a próba-merge eredményén. Elbukik → `git merge --abort`,
  **állj meg**, mutasd a hibát.

Végül mindenképp: `git merge --abort` — az ág érintetlen marad.

### 2. Merge

A merge commit leírása egy ideiglenes fájlba kerül:

- első sor: `PR: <PR URL>` (a Kontextusból);
- alatta `## Worklog`, benne az ágon létrejött összes worklog-fájl teljes
  tartalma, időrendben:

  ```bash
  git diff --name-only --diff-filter=A origin/main...HEAD -- .worklog/
  ```

  Ha nincs worklog, a szakasz elmarad.

```bash
gh pr merge --merge --body-file <leírás>
```

A tárgysor a `gh` alapértelmezése marad (`Merge pull request #<szám> from …`).
Merge commit a `main`-en; `--delete-branch` nincs (a takarítás a 4. lépés). Ha a
`gh` szerint a PR nem mergelhető (kötelező review, blokkoló check), **állj meg**
és írd le, mi a blokkoló.

### 3. Ütközés

Csak a *Fejlesztő* jóváhagyásával. A feloldás a merge commitba kerül, nem az ágba —
egy ideiglenes, detached worktree-ben:

```bash
root=$(dirname "$(git rev-parse --path-format=absolute --git-common-dir)")
git worktree add --detach "$root/.claude/worktrees/merge-<slug>" origin/main
cd "$root/.claude/worktrees/merge-<slug>"
git merge --no-ff <ág>        # ütközések feloldása
# pre-commit gate, majd commit a 2. lépés leírásával:
# git commit -F <üzenet>  — tárgy: "Merge pull request #<szám> from <owner>/<ág>"
git push origin HEAD:main
cd - && git worktree remove "$root/.claude/worktrees/merge-<slug>"
```

A GitHub a PR-t automatikusan `merged` állapotba teszi, mert az ág commitjai a
`main`-re kerültek.

### 4. Takarítás

`/worktree-close` — kilépés a fő checkoutba (`dev`), a worktree és az ág törlése,
a `dev` utoléri a `main`-t.

Végül írd ki a PR számát és URL-jét, valamint a merge commit rövid SHA-ját.

## B. Lokális merge

```bash
git switch main
git pull --ff-only
git merge --ff-only dev
git push origin main dev
git switch dev
```

Ha a `--ff-only` merge elbukik (a `main` közben elmozdult): `git switch dev`,
`git merge main`, pre-commit gate, merge újra. Konfliktusnál **állj meg** — onnan
a *Fejlesztő* dönt.

Végül írd ki a mergelt commitok rövid SHA-ját.
