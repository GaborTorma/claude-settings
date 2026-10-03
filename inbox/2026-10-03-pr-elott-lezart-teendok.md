---
date: 2026-10-03
source: git-graph
kind: skill
---

# PR előtt: lezár-e a munka nyitott issue-t vagy parkoló tételt?

**Mi**: a PR leírásának megírása előtt végig kell nézni a nyitott GitHub
issue-kat és a `.parked.md` tételeit, és megállapítani, melyiket teljesíti
(részben vagy egészben) az ágon elkészült munka.

**Miért**: a git-graph `feat/page-redesign` ágán a redesign közben mellékesen
elkészült a #14 (keresés a lapon) és a #16 (hash másolása ikonnal) is — egyik
sem a munka kiinduló issue-ja volt, ezért a `/pull-request` „Issue” szabálya
(„csak ha a munka issue-ból indult, vagy a Fejlesztő megnevezte”) nem vette
volna észre. Csak a Fejlesztő `/todos`-a után derült ki, hogy zárhatók. A
`Closes #N` nélkül a merge után nyitva maradtak volna, a parkoló tétel pedig a
`/parked`-ig elavultan ott ül.

**Hogyan alkalmazd**:

- A `/pull-request` (és a `/commit-push-pr*`) a leírás előtt: `gh issue list
  --state open` + a `.parked.md` tételei, összevetve az ág diffjével / worklogjaival.
- Teljesen teljesített issue → javaslat `Closes #N`-re; részben teljesített →
  jelezni, mi hiányzik (pl. táblázat: kérés / megvan), és a *Fejlesztő* dönt:
  lezárás, szűkített leírással nyitva tartás, vagy új issue.
- Teljesített parkoló tétel → `/unpark` javaslat.
- Kitalálni nem szabad: csak az kerül a PR-be, amit a *Fejlesztő* jóváhagy
  (a meglévő szabály — „ne találd ki” — érvényes marad, ez csak a javaslatot
  kötelezővé teszi).
