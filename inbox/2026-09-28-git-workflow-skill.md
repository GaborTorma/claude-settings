---
date: 2026-09-28
source: claude-settings
kind: skill
---

# A git-munkafolyamat commandjai egy workflow-skillbe (plugin)

## Mi

A 2026-09-27/28-i session óta a git-munkafolyamat egy rule-ból és egy
commandcsaládból áll: `rules/workflow.md` + `/worktree-open`, `/worktree-close`,
`/commit`, `/worklog`, `/push`, `/pr`, `/merge`, `/release` és a láncaik
(`/commit-push`, `/commit-push-pr`, `/commit-push-pr-merge`, `/commit-push-merge`,
`/commit-push-pr-merge-deploy`). Ezek együtt egy munkafolyamat lépései —
később egy plugin workflow-skilljévé válhatnak.

## Miért

- Egy helyen verziózható és kiadható (`claude plugin tag`), nem symlinkelt
  fájlokként él.
- A skill mellé csomagolt `scripts/` mappa megoldja, hova kerüljenek a
  segédscriptek. Első jelölt: a `/worktree-open` „4. Include-fájlok” ciklusa
  (`git ls-files --others --ignored --exclude-from=.worktreeinclude` + `cp`) —
  scriptként egyetlen `Bash(<script> *)` engedéllyel futna, most minden
  futásnál engedélyt kérhet.
- A `rules/workflow.md` egy rövid hivatkozásra zsugorodhatna; a részletek csak
  a skill invokálásakor töltődnének be.

## Hogyan alkalmazd

- A `/curate`-nél döntsd el: új plugin (pl. `git-workflow`) vagy meglévőbe.
- Költözéskor kötelező rendbe tenni a `vercel-neon` plugint is: a
  `fix-workflow` és a `feature-workflow` még a régi modellt követi
  („push = deploy”, `main` auto-deploy). Az új modell: a `main` pusholása nem
  deploy (`git.deploymentEnabled.main: false`), élesítés csak `/release`-szel,
  tag csak sikeres deploy után; feature mindig worktree-ben, PR-ral.
- Addig a script-kérdés nyitva marad: a ciklus inline a commandban.
