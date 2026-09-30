---
name: merge-dev
description: A dev ág lokális fast-forward mergelése a mainbe PR nélkül, zöld CI után, majd push. Csak a /merge és a láncok hívják, a dev ágon, PR nélkül.
user-invocable: false
allowed-tools: Bash(git branch --show-current), Bash(git status *), Bash(gh run list *), Bash(gh run watch *)
---

## Kontextus

- Ág: !`git branch --show-current`
- Munkakönyvtár: !`git status --porcelain`

A command meghívása maga a merge-engedély — de csak akkor, ha a lépések
hibátlanul lefutnak. A `main` pusholása nem deploy — kiadás csak `/release`-szel.
`--force` tilos.

**Előfeltételek** a Kontextusból — ha bármelyik nem teljesül, **állj meg**:

- **A `dev`-en állsz** — ez a fix-jellegű munka útja (→ `~/.claude/rules/workflow.md`).
- **Tiszta munkakönyvtár** (a **Munkakönyvtár** sor üres) — commitolatlan változás nem
  kerül a `main`-re; előbb `/commit`.
- **Zöld CI**:
  - Ha a `dev` HEAD-jén futott CI (`gh run list --branch dev --commit <sha>`; 
  üres → nincs CI), mindnek zöldnek kell lennie.
  - Még fut → `gh run watch <id>`, várd meg.
  - Piros →  mutasd a hibás futást.

## Merge

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
