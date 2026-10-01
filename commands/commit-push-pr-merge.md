---
name: commit-push-pr-merge
description: Commit + worklog + push + PR + merge a mainbe + takarítás egy menetben. Használd amikor a Fejlesztő /commit-push-pr-merge-öt ír, vagy egy kész feature-ág munkáját azonnal a mainbe akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
allowed-tools: Skill(commit-push-pr *), Skill(merge-pr *)
---

Sorban — ha egy lépés megállt, **itt is állj meg**:

1. `/commit-push-pr` (a *Fejlesztő* argumentumát add át `args`-ként)
2. `/merge-pr`

Minden lépés válaszát a lépés saját formájában írd ki: az egysorosat azonnal, amint
a lépés kész; a többsorosat a lánc végén, a többivel együtt sorrendben.
Más köztes szöveg nincs.
