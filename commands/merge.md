---
name: merge
description: Az aktuális ág mergelése a mainbe — nyitott PR-nél /merge-pr, a dev ágon PR nélkül /merge-dev. Használd amikor a Fejlesztő /merge-et ír, vagy egy kész ágat a mainbe akar vinni.
allowed-tools: Bash(git branch --show-current), Bash(gh pr view *), Skill(merge-pr *), Skill(merge-dev *)
---

## Kontextus

- Ág: !`git branch --show-current`
- PR: !`gh pr view --json number,url,state 2>/dev/null || echo "NINCS"`

A Kontextus alapján, az argumentumot továbbadva (`args`); a válasz a hívott commandé:

- **`main`** → **állj meg — ez hiba**.
- **Van nyitott PR** (`state: OPEN`) → `/merge-pr`.
- **`dev`, PR nélkül** → `/merge-dev`.
- **Más ág, PR nélkül** → **állj meg**: előbb `/pull-request` kell, de kérdezz rá.
