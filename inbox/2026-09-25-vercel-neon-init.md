---
date: 2026-09-25
source: varazskez
kind: skill
---

# vercel-init — Vercel + Neon projekt bekötése: ág-topológia, git connect, MCP-k

## Mi

Egy Vercel + Neon (Marketplace-integráció) projekt alapfelállása négy Neon-ággal
és git-kapcsolattal: **`main` = éles**, **`test` = automata tesztek**,
**`preview/<git-branch>` = feature-ág** (az integráció nyitja preview-deploynál),
**`dev` = lokális fejlesztés**; a kapcsolati adatok kizárólag az integráció
változóiból jönnek, a műveleteket a Neon-, Vercel- és GitHub-MCP-vel végzi az *AI*.

## Miért

Egy napnyi élő hibakeresés a varazskez projekten (hangfürdő app) mutatta meg,
hogy a vercel-neon plugin több szabálya **elavult** vagy hiányos, és a
Marketplace-integráció nem dokumentált módon viselkedik:

1. **A preview soha nem működött** — minden kérésre:
   `error: relation "events" does not exist` (`42P01`). Ok: a Neon-integráció
   preview-deploynál saját `preview/<git-branch>` ágat nyit, és a kapcsolati
   adatokat **deployment-szinten injektálja** (`DATABASE_URL`, `POSTGRES_URL`,
   `PG*` — a `vercel env ls`-ben NEM látszanak), ezzel **felülírja a kézzel
   felvett preview `DATABASE_URL`-t** is. Az injektált URL az integráció saját
   adatbázisára (`neondb`) mutatott, az app viszont egy másik nevű DB-ben
   (`varazskez`) élt.
2. **Az integráció az adatbázist AZONOSÍTÓ alapján követi, nem név alapján.**
   `varazskez` → `neondb` átnevezés után (a régi `neondb` → `nuxt_regi`) a
   preview-injektálás a régi objektum új nevére mutatott — diagnosztikai loggal
   mérve: `[db-diag] ep-…-pooler… /nuxt_regi env: preview`. A régi objektum
   törlése után is `/nuxt_regi`-t injektált. Rotáláskor ugyanez a production
   értékekkel is megtörténhet.
3. **Az integráció a régebbi telepítésnél csak `POSTGRES_*` / `PG*` neveket ír**
   (production/development targetre `DATABASE_URL` NINCS); a plugin `vercel-env`
   skillje („kézzel vedd fel a `DATABASE_URL`-t") emiatt kerülőutat írt elő,
   ami a preview-ban csendben felülíródott.
4. **`vercel env pull` = éles DB lokálisan.** Az integráció változói minden
   targeten ugyanazok (a `main`-re mutatnak), a Next.js a `.env.local`-t a
   `.env` elé sorolja → egy pull után a lokális fejlesztés észrevétlenül élesen fut.
5. **Driver**: a Neon hivatalos útmutatója (Connecting to Neon from Vercel)
   Fluid Compute-ra a **TCP-poolt** ajánlja (`pg` + `attachDatabasePool` +
   `drizzle-orm/node-postgres`), nem a `neon-http`-t; a plugin `neon-driver`
   skillje ebben elavult. Mérve: a két driver nyers `db.execute` eredményei
   bájtra azonosak (drizzle mindkettőben stringként hagyja a
   `timestamptz`/`date`/`interval`-t).
6. **Git-kapcsolat nélkül** (CLI-deploy) a preview Neon-ágak **nem takarítódnak**
   (egy júniusi preview-ág három hónapig ott maradt).
7. **Rossz framework a Vercel projekten**: a gyökérből indított deploy:
   `Error: Command "nuxt build" exited with 127` — a projekt egy régi kísérletből
   maradt `nuxtjs` beállítással, Root Directory nélkül.

## Hogyan alkalmazd

### Ág-topológia (Neon)

| Ág | Mire | Ki hozza létre | Frissítés |
| --- | --- | --- | --- |
| `main` | éles | a projekt | — |
| `test` | CI / e2e (Playwright) | kézzel (MCP `create_branch`) | minden futás után `reset_from_parent` |
| `preview/<git-branch>` | feature: preview-deploy **és** a feature lokális fejlesztése | a Vercel-integráció (vagy előre az *AI*) | a branch törlésével megszűnik |
| `dev` | lokális fejlesztés a `main`-en | kézzel | időnként `reset_from_parent` |

- **Adatbázisnév: maradjon az integráció alapértelmezettje (`neondb`)**, ne hozz
  létre saját nevű DB-t. Ha mégis átnevezés történt: a kliens az URL-ben rögzítse
  a nevet (`url.pathname = "/neondb"`).
- Több fejlesztőnél: fejlesztőnkénti ág (`dev/<név>`), GDPR miatt lehetőleg
  **séma-only ággal** + seed-adattal (a `main`-ből nyitott ág az éles személyes
  adatok másolata).

### Kapcsolat a kódban

- Kizárólag az integráció változói: `POSTGRES_URL` (pooled, futásidő),
  `POSTGRES_URL_NON_POOLING` (migráció). Kézi `DATABASE_URL` **ne legyen** —
  preview-ban úgyis felülíródik, élesben feleslegesen dupláz.
- Fluid Compute: `pg` `Pool` + `attachDatabasePool(pool)` +
  `drizzle-orm/node-postgres`; az URL-t `sslmode=verify-full`-ra írd (a pg 8 a
  `require`-re figyelmeztet, a pg 9-től gyengébb szemantikát kapna).
- A lokális `.env` a `dev` (vagy a feature) ágra mutat; **`vercel env pull`-t
  soha ne a `.env.local`-ba** (ha kell: `vercel env pull .env.vercel`).
- Egy Neon-ág a szülő **szerepköreit és jelszavait örökli** → egy másik ágra
  váltáshoz elég a host cseréje az URL-ben (új titok nem kell).

### Git connect (Vercel ↔ GitHub)

- Kösd be: Vercel dashboard vagy `vercel git connect`; monorepóban **Root
  Directory = az app mappája**, framework = a valós keretrendszer (különben pl.
  `nuxt build exited with 127`). GitHub-oldalon a Vercel app hozzáférése kell.
- Nyereség: minden push preview-deployt kap, a PR-be kerül a preview-link és a
  deploy-állapot, **a git branch törlésekor az integráció a Neon-ágat is törli**.
- **Preview-migráció a buildben**: preview-nál (`VERCEL_ENV=preview`) a build
  előtt `drizzle-kit migrate` a `POSTGRES_URL_NON_POOLING`-ra — így a feature
  sémája a preview-ágon naprakész. **Productionben soha**: az éles migráció kézi.
- **Merge = éles deploy** lesz. Ha az éles deployhoz jóváhagyás kell:
  `vercel.json` → `git.deploymentEnabled` a `main`-re `false`, és kézi promote;
  különben a merge maga a jóváhagyás — ezt projektenként dönteni kell.
- Két Vercel projekt ugyanazon a Neon projekten: egy branch pusholásakor mindkettő
  ugyanazt a `preview/<git-branch>` ágat akarná — **nincs kipróbálva**.

### Worktree-munkamenet (feature = git branch = worktree = Neon-ág)

A worktree-be **nem jön át**: `.env`, `.vercel/` link, `node_modules` (gitignorált).
Indításkor: `git worktree add` → Neon `create_branch preview/<git-branch>` a
`main`-ből → a worktree `.env`-je a fő `.env` másolata host-cserével → Vercel-link
másolása (git connect nélkül) → `npm ci`/`pnpm i` → migráció erre az ágra.
Lezáráskor: `git worktree remove` → Neon-ág törlése (git connectnél automatikus).
Nyitott: a Vercel egy **előre, nem általa** létrehozott ágat is újrahasznosít-e —
saját maga által létrehozottnál igen (mérve), előre létrehozottal nem próbáltuk.

### MCP-k szerepe

| Feladat | MCP |
| --- | --- |
| ág létrehozása / reset / törlés, snapshot, `compare_database_schema`, `pg_stat_database` mérés | Neon |
| deploy-állapot, runtime-log, env-kulcsok (értékek nélkül), projekt-beállítások | Vercel |
| PR, preview-link és deploy-állapot a PR-ben, merge | GitHub (vagy `gh`) |

- **Melyik ágra megy a forgalom?** A `vercel env ls` nem mutatja az injektált
  értéket. Mérés: `SELECT xact_commit FROM pg_stat_database WHERE datname=…` az
  ágon előtte/utána (ágankénti compute-számláló); vagy ideiglenes, nem
  commitolt diagnosztikai log a hostnévvel és az adatbázisnévvel (jelszó nélkül).
- A Neon fogyasztási statisztikái (`active_time_seconds`) **késve frissülnek**,
  ellenőrzésre nem jók. A Neon `query_logs` itt üres volt (telemetria nincs).
- Vercel-kezelt szervezet: új Neon projekt csak a Vercelen át; a `neonctl` csak
  `--api-key`-vel működik (böngészős belépés nem).
- A Claude Code jogosultság-szűrője az **éles deployt** és a **Vercel env-titok
  írását** letiltja (chat-jóváhagyás mellett is) — ezeket a *Fejlesztő* futtatja,
  vagy engedélyező szabályt vesz fel; a folyamatot erre kell tervezni.

### Éles DB-átállás kevés kieséssel

`vercel deploy --prod --skip-domain` (lebuildel, domain nélkül) → snapshot →
DB-művelet (pl. átnevezés, Neon API `update_postgres_database`) → azonnal
`vercel promote <url>`. A kiesés a két lépés közti néhány másodperc.

### A vercel-neon plugint frissíteni kell

- `neon-driver`: Fluid Compute-on a `pg` Pool az alap, nem a `neon-http`.
- `vercel-env`: nincs kézi `DATABASE_URL`; az integráció változói + a
  preview-injektálás + a DB-azonosító-követés csapdája + a `vercel env pull` veszélye.
- `neon-branching`: a `test` ág és a feature/preview-ág szerepe, a séma-only ág.
- `check` command: a „Preview-DB" pont a deployment-szintű injektálást mérje
  (`pg_stat_database`), ne csak a `DATABASE_URL` preview-bejegyzést keresse.
