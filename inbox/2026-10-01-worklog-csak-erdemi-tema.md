---
date: 2026-10-01
source: git-graph
kind: rule
---

# Worklog csak érdemi témáról — a háztartási commit nem kap saját fájlt

## Mi

A `/worklog` témánként egy fájlt ír, de a jelentéktelen karbantartó commit
(pl. egy `.gitignore`-sor) nem téma: nem kap saját worklog-fájlt.

## Miért

A `git-graph` `feat/claude-plugin` ágán két commit volt: a plugin (`feat!`) és
egy `chore: ignore the parked list` (`.parked.md` a `.gitignore`-ba). A
`/worklog` „egy téma = egy fájl” és „minden commit legalább egy témához
tartozik” szabálya miatt a `chore` külön fájlt kapott
(`2026-10-01-0920-ignore-parked-list.md`), saját bekezdésekkel — a *Fejlesztő*
szerint „ez semmi”, nem worklogba való. A worklog olvasója azt akarja látni, mi
történt érdemben; a zaj ezt hígítja (és a merge commitba, a release notes-ba
is átmegy).

## Hogyan alkalmazd

- Az a commit, ami a *User* vagy a *Fejlesztő* szemszögéből nem hordoz
  történetet (ignore-sor, formázás, elírás, verzió-bump, lockfile), **nem
  téma**. Nem kap fájlt, és a worklog szövege sem tér ki rá.
- A „minden commit legalább egy témához tartozik” szabályt ennek megfelelően
  lazítani kell: az ilyen commit vagy kimarad, vagy csak a legközelebbi érdemi
  téma commitlistájába kerül, szöveg nélkül.
- Ha az ágon **csak** ilyen commit van, nincs worklog (mint a „nincs mit
  összefoglalni” ágon).
- Érintett: a `/worklog` command 2. Témák lépése.
