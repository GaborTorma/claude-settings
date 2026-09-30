---
name: commit-push-merge
description: Commit + worklog + lokális merge a mainbe + push, PR nélkül. Használd amikor a Fejlesztő /commit-push-merge-öt ír, vagy a dev ágon kész, fix-jellegű munkát a mainbe akarja vinni.
argument-hint: "commit üzenet vagy kontextus (opcionális)"
---

A `dev` ág munkája a `main`-be, PR nélkül. Sorban — ha egy lépés megállt, **itt is
állj meg**:

1. `/commit` (a *Fejlesztő* argumentumát add át `args`-ként)
2. `/worklog`
3. `/merge-dev`

Minden lépés válaszát a lépés saját formájában írd ki: az egysorosat azonnal, amint
a lépés kész; a többsorosat a lánc végén, a többivel együtt sorrendben.
Más köztes szöveg nincs.
