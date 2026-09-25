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

A varazskez preview-ja soha nem működött (`relation "events" does not exist`,
`42P01`), mert:
- az integráció preview-nál **deployment-szinten injektál** (`POSTGRES_URL`,
  `DATABASE_URL`, `PG*` — a `vercel env ls` nem mutatja), és felülírja a kézi
  `DATABASE_URL`-t;
- az adatbázist **azonosító alapján követi**: átnevezés után a régi objektumra
  injektált (`/nuxt_regi`);
- a `vercel env pull` a `.env.local`-ba az **éles** DB-t hozza (minden target a
  `main`-re mutat), és a Next.js a `.env` elé sorolja;
- git connect nélkül a preview Neon-ágak nem takarítódnak;
- rossz framework a projekten: `Error: Command "nuxt build" exited with 127`.

A vercel-neon plugin `neon-driver` és `vercel-env` skillje ezekben elavult.

## Hogyan alkalmazd

- **DB-név**: az integráció alapértelmezett `neondb`-je; ha átnevezés történt, a
  kliens rögzítse (`url.pathname = "/neondb"`).
- **Kód**: `POSTGRES_URL` (futásidő) + `POSTGRES_URL_NON_POOLING` (migráció),
  kézi `DATABASE_URL` nélkül. Fluid Compute-on `pg` Pool + `attachDatabasePool`
  (a Neon ajánlása), `sslmode=verify-full`.
- **Lokális**: a `.env` a `dev` ágra mutat; `vercel env pull` soha a
  `.env.local`-ba. Ág-váltáshoz elég a host cseréje (a szerepkör és a jelszó öröklődik).
- **`test`**: CI-hoz, minden futás után `reset_from_parent`. Csapatban
  fejlesztőnkénti, séma-only ág + seed (GDPR).
- **Git connect**: Root Directory = app mappa, helyes framework. Preview minden
  pushra, a Neon-ág a branch törlésével megszűnik. Preview-buildben
  `drizzle-kit migrate` (csak `VERCEL_ENV=preview`). Dönteni kell: merge = éles
  deploy, vagy `git.deploymentEnabled: false` a `main`-re + kézi promote.
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
- **Nincs kipróbálva**: előre létrehozott ágat újrahasznosít-e a Vercel; két
  Vercel projekt egy Neon projekten.
