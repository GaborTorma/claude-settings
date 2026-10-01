---
date: 2026-10-01
source: git-graph
kind: rule
---

# Worktree-izolált sessionből nem lehet a fő checkoutba írni

## Mi

Az `EnterWorktree` után a session a worktree-be van zárva: a fő checkout
útvonalára se fájlt írni, se git-parancsot futtatni nem tud. Ezért a
`.parked.md` (és bármi, ami a fő checkoutba menne) csak a worktree-n belül
jöhet létre.

## Miért

A `/park` a worktree-ben megkérdezte, hova menjen a tétel; a *Fejlesztő* a fő
checkoutot választotta, de az írás elbukott:

```
This session is isolated in the worktree /Users/tgc/Development/Claude/git-graph/.claude/worktrees/claude-plugin. Edit the worktree copy of this file instead of the shared-checkout path.
```

A fő checkout `git status`-a is tiltott:

```
This session is isolated in the worktree …, but this command names git more than once in a single command, which cannot be verified to stay inside the worktree. Refusing to run it — …
```

Mellékhatásként az őr minden olyan parancsot visszadob, amelyben a `git` szó
többször szerepel vagy nem egyértelmű helyen áll. Ide tartozik egy `git-graph`
nevű **fájl** is (`git mv git-graph bin/`, `python3 -m py_compile bin/git-graph`,
`sed … git-graph | node --check -`), és a `$(…)`-val számolt argumentum is.

A worktree-ben levő más repók (pl. a `claude-settings` mint additional
directory) írhatók maradnak — csak a saját repó megosztott checkoutja zárt.

## Hogyan alkalmazd

- `/park` worktree-ben: ne kérdezz rá a fő checkoutra, a tétel a worktree
  `.parked.md`-jébe megy. A „számláló mindig a fő checkoutban él” szabály itt
  nem tartható: a fő checkout fájlja legfeljebb olvasható (ha az is) —
  ID-ütközés ellen a `/worktree-close` átvezetéskor számozza újra.
- Ami a fő checkoutba tartozik (a `dev` ág fájljai, `git status` a rooton):
  vagy a *Fejlesztő* futtatja a saját termináljában, vagy `ExitWorktree`
  (`keep`) után.
- A worktree-őr megkerülése: egy parancs = egy `git` hívás; `git -C <worktree>`
  helyett sima, worktree-ből futó parancs; `git`-et tartalmazó fájlnévre
  aliassal/symlinkkel hivatkozz (pl. `bin/gg`), vagy `mv` + `git add -A`.
