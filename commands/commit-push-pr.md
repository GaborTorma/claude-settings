---
name: commit-push-pr
description: Commit + PR (worklog, push, PR a worklogokkal). Használd amikor a Fejlesztő /commit-push-pr-t ír, vagy egy ág munkáját PR-ba akarja vinni.
argument-hint: "PR cím vagy kontextus (opcionális)"
allowed-tools: Skill(commit *), Skill(pull-request *)
---

Sorban — ha egy lépés megállt, **itt is állj meg**:

1. `/commit` (`args`: `$ARGUMENTS`)
2. `/pull-request` (`args`: `$ARGUMENTS`)

Minden lépés válaszát a lépés saját formájában írd ki: az egysorosat azonnal, amint
a lépés kész; a többsorosat a lánc végén, a többivel együtt sorrendben.
Más köztes szöveg nincs.
