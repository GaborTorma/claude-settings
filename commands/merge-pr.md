---
name: merge-pr
description: Feature-ág PR-jének mergelése a mainbe — próba-merge és check, zöld CI, merge commit a worklogokkal, majd takarítás. Csak nyitott PR esetén.
user-invocable: false
allowed-tools: Bash(git branch --show-current), Bash(git status *), Bash(gh pr list *), Bash(gh pr view *), Bash(gh pr checks *), Bash(git fetch *), Bash(git merge-base *), Bash(git merge --no-commit --no-ff origin/main), Bash(git merge --abort), Bash(git merge origin/main), Bash(git diff *), Skill(check *), Skill(worktree-close *)
---

## Kontextus

- Ág: !`git branch --show-current`
- PR: !`gh pr list --state all --head "$(git branch --show-current)" --limit 1 --json number,url,state 2>&1 || echo "HIBA"`
  — `[]` = nincs PR; a sor végén `HIBA` → mutasd a fölötte lévő hibát, és **állj meg**.
- Munkakönyvtár: !`git status --porcelain`

A command meghívása maga a merge-engedély — de csak akkor, ha a lépések
hibátlanul lefutnak. A `main` pusholása nem deploy — kiadás csak `/release`-szel.
`--force` és `--admin` tilos.

**Előfeltételek** a Kontextusból — ha bármelyik nem teljesül, **állj meg**:

- **Tiszta munkakönyvtár** (a **Munkakönyvtár** sor üres) — commitolatlan változás nem
  kerül a PR-be; előbb `/commit`.
- **Nyitott PR** (`state: OPEN`) — `[]` → előbb `/pull-request`; `MERGED` /
  `CLOSED` → nincs mit mergelni.
- **Zöld CI**:
  - ha a PR-en van check (`gh pr checks`; „no checks reported” → nincs CI),
  mindnek zöldnek kell lennie
  - Még fut → `gh pr checks --watch`, várd meg.
  - Piros → mutasd a hibás checket.

## 1. Próba-merge

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

- **`/check`** a próba-merge eredményén. Elbukik → `git merge --abort`,
  **állj meg**, mutasd a hibát.

Végül mindenképp: `git merge --abort` — az ág érintetlen marad.

## 2. Merge

A merge commit leírása egy ideiglenes fájlba kerül:

- első sor: `PR: <PR URL>` (a Kontextusból);
- alatta a PR leírásának `## Élesítés` szakasza változatlanul (`gh pr view --json body`),
  ha van — a `/release` innen gyűjti;
- alatta `## Worklog`, benne az ágon létrejött összes worklog-fájl teljes
  tartalma, időrendben:

  ```bash
  git diff --name-only --diff-filter=A origin/main...HEAD -- .worklog/
  ```

  Ha nincs worklog, a szakasz elmarad. A commit-üzenet nem markdown: a commitlista
  linkjei helyett csak a hash és a tárgysor — `` - [`[221fd4a8]`](<URL>) · <subject> ``
  helyett `- 221fd4a8 · <subject>`.

```bash
gh pr merge --merge --body-file <leírás>
```

A tárgysor a `gh` alapértelmezése marad (`Merge pull request #<szám> from …`).
Merge commit a `main`-en; `--delete-branch` nincs (a takarítás a 4. lépés). Ha a
`gh` szerint a PR nem mergelhető (kötelező review, blokkoló check), **állj meg**
és írd le, mi a blokkoló.

## 3. Ütközés

Tegyél javaslatot a megoldásra, folytatás csak a *Fejlesztő* jóváhagyásával.
A merge a feature-munka befejezése, ezért a feloldás az ágba kerül, a saját
worktree-jében.

```bash
git merge origin/main        # ütközések feloldása
```

Feloldás után `/commit-push` (benne a `/check`), majd újra `/merge-pr`.

## 4. Takarítás

`/worktree-close` — kilépés a fő checkoutba (`dev`), a worktree és az ág törlése,
a `dev` utoléri a `main`-t.

Végül írd ki a PR számát és URL-jét, valamint a merge commit rövid SHA-ját.

