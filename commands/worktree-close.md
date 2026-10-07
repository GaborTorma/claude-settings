---
name: worktree-close
description: A feature-worktree lezárása — kilépés a fő checkoutba (dev), a worktree és az ág törlése helyben és a remote-on; mergeletlen munkánál rákérdez. Használd amikor a Fejlesztő /worktree-close-t ír, vagy egy feature-t lezárna vagy eldobna.
allowed-tools: Bash(git branch --show-current), Bash(gh pr view *), Bash(gh pr close *), Bash(git rev-parse *), Bash(git worktree remove *), Bash(cat .parked.md *), Bash(git status *), Bash(git log *), Bash(git fetch *), Bash(git merge-base *), Bash(git merge --ff-only origin/main), Bash(git branch -d *), ExitWorktree, mcp__ccd_directory__change_directory
---

## Kontextus

- Ág: !`git branch --show-current`
- PR: !`gh pr view --json number,url,state 2>&1 || true`
  — `no pull requests found` = nincs PR; más hiba → mutasd, és **állj meg**.
- Parkoló: !`cat .parked.md 2>/dev/null || echo "NINCS"`
- Git közös mappa: !`git rev-parse --path-format=absolute --git-common-dir`
  — a **Fő checkout** ennek a szülője (a `/.git` nélkül).

Ha nem worktree-ben vagy (az ág `dev` vagy `main`), **állj meg**: nincs mit lezárni.
Jegyezd fel az ág nevét — a kilépés után már nem ez az aktuális ág.

## 1. Mergelve van?

```bash
git fetch
git merge-base --is-ancestor HEAD origin/main   # 0: mergelve
```

Mergelt az is, ha a Kontextus szerint a PR `MERGED`.

**Nincs mergelve** → mutasd, mi veszne el (`git status --short`,
`git log --oneline origin/main..HEAD`), és kérdezd meg az `AskUserQuestion`-nel:

- **Megtartom** → `ExitWorktree`, `action: keep`, majd a **6. Az app cwd-je** — és kész;
  az ág és a worktree marad.
- **Eldobom** → a lenti lépések, `discard_changes: true`-val és `git branch -D`-vel;
  a nyitott PR-t `gh pr close`.

## 2. Parkoló tételek

Ha a Kontextus **Parkoló** sora szerint a worktree `.parked.md`-jében van tétel (`NINCS`
→ nincs): mutasd, és kérdezd meg az
`AskUserQuestion`-nel (`multiSelect: true`, a `label` pontosan a tétel sora), melyek
kerüljenek át a fő checkout `.parked.md`-jébe (a számláló elé, az ID marad). A többi a
worktree-vel együtt törlődik.

## 3. Kilépés

`ExitWorktree`, `action: remove`. A session visszakerül a fő checkoutba, a `dev`-re.

Ha a tool a worktree-t nem távolítja el (korábbi sessionben nyitották, vagy
`path`-szal léptünk be): `ExitWorktree`, `action: keep`, majd a fő checkoutból
`git worktree remove .claude/worktrees/<slug>`.

## 4. Ág törlése

```bash
git branch -d <ág>                 # ha megmaradt; eldobásnál -D
git push origin --delete <ág>      # ha a remote-on létezik
```

## 5. A `dev` utoléri a `main`-t

```bash
git fetch
git merge --ff-only origin/main
```

Ha nem fast-forward (a `dev`-en mergeletlen munka van): egyeztess a *Fejlesztő*vel.

## 6. Az app cwd-je

Csak a Claude desktop appban (ha a `mcp__ccd_directory__change_directory` elérhető).
Utolsó lépésként: `mcp__ccd_directory__change_directory` a **Fő checkout** útjára — az
app session-fájlja (`cwd`) különben a törölt worktree-re mutatna; erre épül pl. a
git-graph „saját” worktree-je. Ártalmatlan, ha a session már a fő checkoutban van. A kör
végén hat.

A **play gomb** a terminál panel *Fejlesztő* nyitotta tabjába gépel; a `/worktree-open`
`cd`-je után az a törölt worktree-ben maradna — a válasz végén adj egy blokkot, és kérd a
*Fejlesztő*t, hogy egyszer nyomja meg:

```bash
cd <a fő checkout abszolút útja>
```

Végül írd ki, mi törlődött (worktree, helyi és remote ág), és hogy a session a
`dev`-en áll.
