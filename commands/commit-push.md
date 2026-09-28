---
name: commit-push
description: Commit + push egy menetben, PR nélkül. Használd amikor a Fejlesztő /commit-push-t ír, vagy a kész munkát csak fel akarja tolni a remote-ra.
argument-hint: "commit üzenet vagy kontextus (opcionális)"
---

`/commit` (az argumentumot add át `args`-ként), majd `/push`.
Ha a `/commit` megállt, a `/push` elmarad.
