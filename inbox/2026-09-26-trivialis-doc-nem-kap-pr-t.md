---
date: 2026-09-26
source: varazskez
kind: rule
---

## Mi

Triviális doksi-kiegészítés (egy döntésnapló-sor, egy deploy-azonosító, elírás)
nem kap saját branchet, PR-t és mergét.

## Miért

A varazskez pnpm-átállásánál (PR #6) a merge és a production deploy után a
`PROJECT.md` döntésnaplójából hiányzott az élesítés jelölése
(`**ÉLES 2026-09-26** (dpl_5931gkszUFPX1a4sDfqnzX7P6AK9, fra1)`). Az *AI* erre
az egy sorra külön `docs/pnpm-eles` branchet nyitott, pusholta, PR-t nyitott
(#7) és mergelte — a korábbi `docs/workflow-eles` (PR #5) mintáját követve.
A *Fejlesztő* reakciója: „most egy vacak doc fájl miatt csináltál egy külön
branchet, amit aztán mergeltél. ezt nagyon nem így kell”.

A költség aránytalan: egy sor miatt branch + push + PR + merge commit a
gráfon, és egy fölösleges Vercel preview-build (a branch-push minden
alkalommal buildel, Neon preview-ággal együtt).

## Hogyan alkalmazd

- Egy-két soros doksi-pótlásra **ne** indíts `git checkout -b` → PR → merge
  folyamatot, akkor sem, ha a repóban van rá korábbi példa.
- Az élesítés utáni „ÉLES + dpl ID” bejegyzés a feature PR-ral együtt
  készüljön, ahol csak lehet: a döntésnapló-bejegyzés már a feature branchen
  megszületik, a deploy utáni kiegészítés pedig a következő érdemi munka
  commitjával megy.
- Ha a pótlás nem várhat, kérdezd meg a *Fejlesztő*t, hogyan menjen fel
  (közvetlen commit a `main`-re, vagy a következő branch része) — ne a
  teljes PR-folyamatot válaszd alapból.
- **Nyitott kérdés a `/curate`-nek**: a *Fejlesztő* nem mondta ki, mi a
  helyes alternatíva (közvetlen `main`-commit vs. a következő branchbe
  csomagolás) — ezt a kurációnál érdemes vele tisztázni, mert a globális
  `git.md` szerint `main`-en állva branchet kell nyitni.
