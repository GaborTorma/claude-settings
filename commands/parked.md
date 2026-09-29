---
name: parked
description: Az aktuális munka és a parkoló témák kiírása a focus.md formájában, majd kérdés a folytatásról. Használd amikor a Fejlesztő /parked-ot ír, vagy azt kérdezi, mi van nyitva, mi parkol.
allowed-tools: Bash(git status *), Bash(git worktree list *)
---

## Kontextus

- Git: !`git status -sb`
- Worktree-k: !`git worktree list --porcelain`

A formátum és a kérdés a `~/.claude/rules/focus.md` 4. „Lezáráskor” lépése szerint.

## 1. Összegyűjtés

- **Aktuális**: a folyamatban lévő munka ebben a sessionben, és ha van, a
  félbemaradt munka a Kontextusból (commitolatlan változás, nyitott worktree).
  Pusholatlan, de commitolt munka nem aktuális.
- **Parkolóban**: a session parkolólistája, a *Fejlesztő* / *AI* jelöléssel.

## 2. Lista

A sessionbe, a `focus.md` formájában. Aktuális sor csak, ha van folyamatban lévő munka.

Ha nincs se aktuális, se parkoló tétel: csak ennyi — `Nincs nyitott vagy parkoló téma.`,
és nincs kérdés.

## 3. Kérdés

`AskUserQuestion`: „Hogy folytassuk?” — az opciók a lista sorszámára hivatkoznak.
Ha a Kontextus szerint van pusholatlan commit (`[ahead N]`), a push az utolsó opció.
