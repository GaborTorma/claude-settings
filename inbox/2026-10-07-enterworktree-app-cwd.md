---
date: 2026-10-07
source: git-graph
kind: rule
---

# `EnterWorktree` után az app cwd-je a fő checkouton marad

## Mi

A Claude desktop appban az `EnterWorktree` csak a Claude Bash eszközét viszi át a
worktree-be. Az app session-cwd-je a fő checkouton marad, ezt a
`mcp__ccd_directory__change_directory` a worktree abszolút útjára állítva javítja.

## Miért

Mérve, 2026.10.06., a git-graph P08 vizsgálatakor. `EnterWorktree` után (`name` és
`path` változattal is):

| Mi | Hol fut / mit mutat |
| --- | --- |
| Claude Bash eszköze, Claude nyitotta terminál tab, `preview_start` | worktree ✅ |
| Run gomb a ```` ```bash ```` blokkon | fő checkout ❌ |
| App session-fájl (`~/Library/Application Support/Claude/claude-code-sessions/*/*/local_<id>.json`) | `cwd` = fő checkout, `worktreePath: null` ❌ |

Erre a `cwd`-re épül minden, ami kívülről nézi a sessiont (pl. a git-graph „saját”
worktree-je).

`change_directory` után, **a kör végén**: az app-fájl `cwd`-je a worktree.
Mellékhatás: az `originCwd` is átáll, a `gitAnchors` kiürül; a
`worktreePath` / `worktreeName` / `branch` `null` marad. Kilépéskor
`ExitWorktree` + `change_directory` vissza → `cwd`, `originCwd`, `gitAnchors`
visszaáll.

A Run gomb tartós shellje megőrzi a `cd`-t, de a munkakönyvtárát sem az
`EnterWorktree`, sem a `change_directory` nem állítja át — oda egy `cd` kell.

Gotcha: az `ExitWorktree` `action: remove` a `path`-szal belépett worktree-t nem
törli („not the owner”).

## Hogyan alkalmazd

- Worktree-be lépés után, a kör utolsó lépéseként: `change_directory` a worktree
  abszolút útjára; utána ebben a körben semmi, ami a cwd-re épül.
- Kilépés után: `change_directory` vissza a fő checkoutra.
- A Run gombhoz adj egy ```` ```bash ```` blokkot `cd <abszolút út>`-tal, és kérd a
  *Fejlesztő*t, hogy egyszer nyomja meg.
- `path`-szal belépett worktree eltávolítása: `ExitWorktree` `action: keep`, majd
  `git worktree remove <út>`.
- Már beépítve: `commands/worktree-open.md` 4. lépés, `commands/worktree-close.md`
  6. lépés (`26dbe0ed`).
