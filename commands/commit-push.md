---
name: commit-push
description: Commit + push egy menetben, PR nélkül. Használd amikor a Fejlesztő /commit-push-t ír, vagy a kész munkát csak fel akarja tolni a remote-ra.
argument-hint: "commit üzenet vagy kontextus (opcionális)"
allowed-tools: Skill(commit *), Skill(push *)
---

`/commit` (az argumentumot add át `args`-ként), majd `/push`.
Ha a `/commit` megállt, a `/push` elmarad.

Minden lépés válaszát a lépés saját formájában írd ki: az egysorosat azonnal, amint
a lépés kész; a többsorosat a lánc végén, a többivel együtt sorrendben.
Ha nem volt mit commitolni, a `/commit` válasza elmarad.
Más köztes szöveg nincs.
