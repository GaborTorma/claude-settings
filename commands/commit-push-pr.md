---
name: commit-push-pr
description: Commit + PR (worklog, push, PR a worklogokkal). Használd amikor a Fejlesztő /commit-push-pr-t ír, vagy egy ág munkáját PR-ba akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
---

Sorban — ha egy lépés megállt, **itt is állj meg**:

1. `/commit` (a *Fejlesztő* argumentumát add át `args`-ként)
2. `/pull-request` (ugyanazzal az argumentummal)

Minden lépés válaszát a lépés saját formájában írd ki: az egysorosat azonnal, amint
a lépés kész; a többsorosat a lánc végén, a többivel együtt sorrendben.
Más köztes szöveg nincs.
