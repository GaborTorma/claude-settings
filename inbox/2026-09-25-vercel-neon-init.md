---
date: 2026-09-25
source: varazskez
kind: skill
---

# vercel-init — Vercel + Neon: ág-topológia, git connect, MCP-k

## Mi

Neon-ágak: **`main` = éles**, **`test` = CI/e2e**, **`preview/<git-branch>` =
feature** (az integráció nyitja), **`dev` = lokális fejlesztés**. A kapcsolat
kizárólag az integráció változóiból jön; a műveleteket az *AI* a Neon-, Vercel-
és GitHub-MCP-vel végzi.

## Miért

A Neon Marketplace-integráció nem dokumentált módon viselkedik, és a preview
emiatt csendben rossz adatbázisra mehet (`relation "…" does not exist`, `42P01`):
- preview-deploynál saját ágat nyit, és a kapcsolati adatokat
  **deployment-szinten injektálja** — a `vercel env ls` nem mutatja, és a kézzel
  felvett, azonos nevű DB-változót felülírja;
- az adatbázist **azonosító alapján követi**: átnevezés után a régi objektumra
  injektál, akár annak törlése után is;
- a változói minden targeten a `main`-re mutatnak, így a `vercel env pull` a
  `.env.local`-ba az **éles** DB-t hozza (a Next.js a `.env` elé sorolja);
- git connect nélkül a preview Neon-ágak nem takarítódnak;
- rossz framework vagy Root Directory a projekten: a build rossz eszközzel indul
  (`Error: Command "… build" exited with 127`).

## Hogyan alkalmazd

- **DB-név**: az integráció alapértelmezett `neondb`-je. Ha mégis más név kell,
  vagy átnevezés történt, a kliens rögzítse az URL-ben.
- **Kód**: `POSTGRES_URL` (futásidő) + `POSTGRES_URL_NON_POOLING` (migráció);
  saját, kézi DB-változó ne legyen. Fluid Compute-on `pg` Pool +
  `attachDatabasePool` (a Neon ajánlása), `sslmode=verify-full`.
- **Lokális**: a `.env` a `dev` ágra mutat; `vercel env pull` soha a
  `.env.local`-ba. Ág-váltáshoz elég a host cseréje (a szerepkör és a jelszó öröklődik).
- **`test`**: CI-hoz, minden futás után `reset_from_parent`. Csapatban
  fejlesztőnkénti, séma-only ág + seed (GDPR).
- **Git connect**: Root Directory = app mappa, helyes framework. Preview minden
  pushra, a Neon-ág a branch törlésével megszűnik. Preview-buildben migráció
  (csak `VERCEL_ENV=preview`). Dönteni kell: merge = éles deploy, vagy
  `git.deploymentEnabled: false` a `main`-re + kézi promote.
- **Worktree** = git branch = `preview/<git-branch>` Neon-ág. A `.env`, a
  `.vercel/` és a `node_modules` nem jön át: `.env` host-cserével, link másolása,
  install, migráció. Lezáráskor a Neon-ág törlése.
- **MCP-k**: Neon — ág, reset, snapshot, séma-összevetés; Vercel — deploy, log,
  env-kulcsok, projektbeállítás; GitHub — PR, preview-link, merge. Hogy melyik
  ágra megy a forgalom: `pg_stat_database.xact_commit` az ágon előtte/utána.
- **Éles DB-átállás**: `vercel deploy --prod --skip-domain` → snapshot →
  DB-művelet → azonnal `vercel promote`.
- A Claude Code szűrője az éles deployt és a Vercel env-titok írását letiltja: ezt
  a *Fejlesztő* futtatja.
- A vercel-neon plugin `neon-driver` és `vercel-env` skillje ezekben elavult.
- **Nincs kipróbálva**: előre létrehozott ágat újrahasznosít-e a Vercel; két
  Vercel projekt egy Neon projekten.
