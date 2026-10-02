---
date: 2026-10-02
source: git-graph
kind: skill
---

# A PR merge-e rebase legyen, ha lehetséges

## Mi

A feature-ág PR-je a `main`-be rebase-szel kerüljön (`gh pr merge --rebase`),
ne merge committal; merge commit csak akkor, ha a rebase nem lehetséges.

## Miért

- A *Fejlesztő* kérése (git-graph, a `refactor/artifact-skill` ág lezárása
  előtt): „a merge rebase legyen, ha lehetséges”.
- Ma a `/merge-pr` mindig merge commitot csinál:
  `gh pr merge --merge --body-file <leírás>` (`commands/merge-pr.md:78`),
  előtte próba-merge: `git merge --no-commit --no-ff origin/main` (`:39`).
- A merge commit **viszi a worklogokat**: a `/pull-request` szerint „A
  `/merge-pr` ezt a merge commitba viszi, a `/release` onnan gyűjti”
  (`commands/pull-request.md:41`). Rebase-nél nincs merge commit → a worklogok
  gyűjtése máshonnan kell (pl. a `.worklog/` fájlokból a legutóbbi `v*` tag
  óta, vagy a PR leírásából `gh pr list --state merged`-del).

## Hogyan alkalmazd

- `/merge-pr`: a próba-merge helyett próba-rebase (`git rebase origin/main` a
  feature-ágon; ütközésnél `git rebase --abort`), majd
  `gh pr merge --rebase`.
- **Ha lehetséges** = nincs rebase-ütközés, és a repóban engedélyezett a
  rebase merge (`gh repo view --json rebaseMergeAllowed`). Különben a mostani
  út: `gh pr merge --merge`.
- A rebase-elt ág pusholása force-pusht kívánna, de a `push --force` tilos
  (`rules/git.md`) — ezért a rebase-t a GitHub végezze (`gh pr merge --rebase`),
  a lokális próba-rebase csak ellenőrzés legyen, push nélkül.
- Igazítandó: `commands/merge-pr.md` (lépések, `allowed-tools`, a záró sor
  „merge commit rövid SHA-ja”), `commands/pull-request.md:41`,
  `commands/release.md` (honnan gyűjti a worklogokat), `rules/workflow.md`
  („csak a PR merge-e fésüli össze”, ütközésnél `git merge origin/main`).
- Nyitott kérdés a `/curate`-nek: a `/merge-dev` (dev → main, PR nélkül) már
  `--ff-only`, azt nem érinti.
