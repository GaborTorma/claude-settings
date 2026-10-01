---
date: 2026-10-01
source: git-graph
kind: skill
---

# A merge-pr / worktree-close után a `dev` utoléri a `main`-t, az `origin/dev` nem

## Mi

A `/merge-pr` (és így a `/commit-push-pr-merge`) a takarításnál a
`/worktree-close`-t hívja, ami a fő checkoutban a `dev`-et fast-forwarddal a
`main`-re hozza (`git merge --ff-only origin/main`), de nem pusholja — az
`origin/dev` a régi helyén marad, a `dev` pedig minden kör után egyre többel
jár előrébb.

## Miért

A git-graph sessionben három feature-kör (PR #7, #8, #10) és két `/release`
után a `dev` sorra `[ahead 6]`, `[ahead 9]`, `[ahead 10]` volt
(`## dev...origin/dev [ahead 10]`) — minden alkalommal külön `/push` kellett.
A `/release` végén a „válts vissza az indulási ágra” lépés ugyanígy csak helyben
hozza utol a `dev`-et (a release-commit is így kerül rá). Közben a remote `dev`
elavult: aki onnan indulna (másik gép, CI, `git worktree add` az `origin/dev`-ről),
régi állapotot kap.

## Hogyan alkalmazd

- A `/worktree-close` „5. A `dev` utoléri a `main`-t” lépése a fast-forward után
  pusholja is a `dev`-et: `git push origin dev` (csak fast-forward volt, nincs
  benne új munka — megerősítés nem kell; `--force` továbbra is tilos).
- Ugyanez a `/release` végén, a `dev`-re való visszaváltás és fast-forward után.
- Ha a `dev`-en mergeletlen saját munka van (nem fast-forward), maradjon a mai
  viselkedés: egyeztetés a *Fejlesztő*vel, push nélkül.
