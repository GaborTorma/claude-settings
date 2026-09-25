---
date: 2026-09-25
source: varazskez
kind: skill
---

# Vercel + Neon: init, driver, feat, deploy (összesítés)

**Mi**: egy helyre gyűjtve minden Vercel + Neon tény a mai sessionből, a
`../inbox` Vercel/Neon fájljaiból (`vercel-neon-init`, `-lifecycle`,
`-feature-workflow`) és a `vercel-neon` pluginból. **ELAVULT** jelöli, ahol a
plugin vagy egy korábbi inbox a mai mérésnek ellentmond.

**Miért**: a tudás öt skillben és három inboxban szórva van, és ezek részben
ellentmondanak egymásnak. A `/curate` ebből frissítse a `vercel-neon` plugint.

**Hogyan alkalmazd**: Vercel + Neon munka előtt ezt a listát nézd át, és a
jelzett ellentmondásoknál a mért tény az irányadó.

## Topológia, init
- Egy app = egy Vercel-projekt = egy Neon-projekt, azonos névvel. A párosítást a
  Vercel-env `NEON_PROJECT_ID` változója mondja meg, nem a név.
- Régió: Vercelen `fra1` (a `vercel.json` `regions` és a projekt
  `serverlessFunctionRegion` beállítása is), Neonon `aws-eu-central-1`. A Neon
  régiója utólag nem módosítható.
- Neon létrehozása: `vercel integration add neon --metadata region=fra1`
  (Vercel-régiónévvel).
- Vercel által kezelt Neon-szervezetben:
  - a Neon MCP `create_project` hívása elutasítva: „organization is managed by Vercel”;
  - a `create_branch` működik;
  - a `neonctl` csak `--api-key`-vel megy, böngészős auth nincs.
- Monorepo:
  - a Root Directory az app mappája;
  - a CLI-deploy a repó **gyökeréből** fut, almappából ez a hiba jön: `The specified Root Directory "<dir>" does not exist`;
  - rossz framework-beállításnál rossz eszközzel buildel: `Command "nuxt build" exited with 127`.
- Git connect: `vercel git connect`, előtte a Vercel GitHub-appnak hozzáférés kell.
  - A `vercel.json` `git.deploymentEnabled.main: false` beállítása mellett a merge nem deployol élesre.
- Két MCP azonos nevű eszközökkel (`list_projects`, `describe_project`, …): a teljes
  eszköznév alapján válassz. Az azonosítók alakja is elárulja az oldalt:
  - Vercel: `prj_`, `team_`, `dpl_`;
  - Neon: `br-`, `ep-`, `szó-szó-szám` alakú projekt-id.

## Neon-integráció viselkedése (mérve)
- A `preview/<git-ág>` Neon-ág az **első commitos** pushra jön létre, kb. 3 s
  alatt. Üres git-ágra nem.
- A Vercel az **előre létrehozott** `preview/<git-ág>` ágat újrahasznosítja.
- A kapcsolati adatokat deploymentenként injektálja (`DATABASE_URL`,
  `POSTGRES_URL`, `PG*`):
  - a `vercel env ls` nem mutatja őket;
  - az azonos nevű kézi változót felülírják;
  - **ELAVULT**: a plugin `vercel-env` skillje, amely kézi preview-`DATABASE_URL`-t ír elő.
- A projekt-szintű integrációs változók minden targeten a `main`-re mutatnak. Ezért:
  - a `vercel env pull` éles DB-t ad;
  - a `.env.local`-ba pullolni tilos, mert a Next.js a `.env.local`-t a `.env` előtt tölti;
  - **ELAVULT**: a plugin, amely a `vercel env pull` → `.env.local` utat javasolja.
- Az integráció az adatbázist **azonosító** alapján követi, nem név alapján.
  Átnevezés után a régi DB felé injektált (`42P01 relation "…" does not exist`).
  Megoldás: a kliens rögzíti a DB-nevet (`url.pathname = "/neondb"`).
- Saját DB-t ne hozz létre, maradjon az alapértelmezett `neondb`.
- Takarítás:
  - a Vercel által kezelt integráció akkor törli a preview-ágat, ha az utolsó hozzá tartozó deployment is törlődik (a megőrzési szabály miatt ez hónapokig tarthat);
  - a Neon által kezelt integráció a git-ág törlésekor töröl;
  - **ELAVULT**: a `vercel-neon-init` inbox szerint „A branch törlésével a Neon-ág is megszűnik”.
- Változónevek:
  - a Neon dokumentációja szerint a `DATABASE_URL` / `DATABASE_URL_UNPOOLED` az ajánlott név, a `POSTGRES_*` a Vercel Postgres-kompatibilitás;
  - régebbi telepítés projekt-szinten csak a `POSTGRES_*` változókat tárolja;
  - a kód egyetlen névkészletet olvasson, amelyet az MCP-vel ellenőriztél.
- A `test` Custom Environmenthez (Pro csomag) a Neon-erőforrás **ne** kapcsolódjon,
  különben a `main` adataival felülírja a kézi DB-URL-t. Az első deploy után mérd meg.

## Neon-ágak
- Az ág copy-on-write, saját endpointtal. A szerepkört és a jelszót a szülőtől
  örökli, ezért ágváltáshoz elég a hostot kicserélni.
- A `run_sql` alapból a default (éles) ágra fut: írás előtt mondd ki, melyik ágon dolgozol.
- `reset_from_parent`: az ág tartalma elvész, és újra a szülőből másolódik.
  Visszafordíthatatlan, előtte kérdezz.
- Point-in-time visszaállítás csak a `history_retention` ablakon belül lehet;
  ezen túl snapshot kell. Kockázatos lépés előtt `create_snapshot`.
- Az inaktív ág archiválódik, az első kapcsolódás felébreszti.
- `prepare_database_migration` → `complete_database_migration`: kézi éles DDL
  ideiglenes ágon ellenőrizve. A drizzle-t nem váltja ki.
- `neonctl link` / `checkout <ág>` / `env pull [--branch] [--file]`:
  - `DATABASE_URL`, `DATABASE_URL_UNPOOLED` és `NEON_BRANCH` változókat ír;
  - a `.env`-be ír, ha az létezik, különben a `.env.local`-ba;
  - a fájl többi sorát megőrzi.
- Anonimizált ág (`branch_anonymized`, masking rules): béta, reset nem megy rajta.
  Schema-only ág: `neonctl branches create --schema-only`.
- GitHub Actions:
  - `neondatabase/create-branch-action` (`expires_at`-tal);
  - `delete-branch-action`;
  - `reset-branch-action`;
  - `schema-diff-action`, amely PR-kommentben mutatja a sémaváltozást.

## Compute, költség
- A számla compute-idő alapján megy: egyetlen lekérdezés is legalább egy
  suspend-ablaknyi (pl. 300 s) számlázott időt jelent. Az ébresztő forrásokat kell
  ritkítani: cron, polling, uptime-monitor.
- Cold start 0,25 CU-n kb. 4× a meleg válaszidő (~794 ms vs ~200 ms). A CU-emelés
  a cold startot nem gyorsítja.
- A publikus tartalom menjen edge-cache-ből. Seed után deploy kell, mert az
  invalidáció maga a deploy.
- Az új ágak compute-alapértéke a projekt `default_endpoint_settings`
  beállításából jön. Neon MCP `update_project` 0,25–0,25 CU-ra: az új preview-ágak
  0,25 CU-val indulnak.
- Launch csomag: 10 ág benne van, felette $1,50/ág/hó (óránként arányosítva);
  compute $0,106/CU-óra; a tárhely copy-on-write.
- `active_time_seconds` ≠ `cpu_used_sec`: az ébren töltött időt fizeted. Az
  elfelejtett ágak önállóan fogyasztanak.

## Driver
- Fluid Compute-on: `pg` Pool + `attachDatabasePool` (`@vercel/functions`) +
  `drizzle-orm/node-postgres`. Ez a Neon ajánlása Fluidra, és így interaktív
  tranzakció is lehetséges.
  - **ELAVULT**: a plugin `neon-driver` skillje, amely a `neon-http`-t teszi alappá.
- `attachDatabasePool` nélkül a felfüggesztett függvény kapcsolatai bennragadnak,
  és jön a „too many connections” hiba.
- Futásidőben a pooled (`-pooler`) host, DDL-hez és `drizzle-kit`-hez az
  unpooled. A pooled host a DDL-t töri.
- `sslmode=verify-full`: a `pg` 8 a `require`-re figyelmeztet.
- A `timestamptz`, `date` és `interval` mindkét driverben nyers stringként jön vissza.
- Build közben importált kliens lusta legyen, `getDb()` függvénnyel, ne `Proxy`-val.
- A `drizzle-kit` nem olvas `.env.local`-t: a betöltés a futtatóé
  (`process.loadEnvFile` / `dotenv -e`).

## Env, biztonság
- Env-változás csak új deploymentre hat.
- A cron publikus URL: a kódban ellenőrizd a `Bearer $CRON_SECRET` fejlécet. A
  titok csak productionben legyen. A Vercel Cron csak a production deploymenten fut.
- `NEXT_PUBLIC_` előtaggal titok soha.
- Az SSO-védett preview-hoz hitelesített kérés kell (`vercel curl`); a védelmet ne kapcsold ki.
- Rotálás után minden kézi DB-URL-t frissíteni kell, targetenként, majd redeploy.
- Éles másolaton futó nem-éles környezet (preview, `test`, lokális): a levélküldést
  át kell irányítani, mert valódi ügyfeleknek menne. Stripe-ból teszt-kulcs kell.
- Env-értéket és connection stringet ne írj ki a beszélgetésbe. A
  `get_connection_string` és a decrypt csak kifejezett kérésre.
- A Claude Code szűrője tiltja az éles deployt és a Vercel titok-env írását. Ezeket
  a *Fejlesztő* futtatja, ne kerüld meg.
- A destruktív Neon-műveletet (DB drop, branch delete, reset) a *Fejlesztő* hagyja jóvá vagy futtatja.

## Séma, migráció
- Értékes adatnál `drizzle-kit generate` + `migrate`, verziózott SQL a repóban.
  - `push` csak a saját feature-ágon, iterálás közben;
  - `push` éles DB ellen soha.
- `push`-ról váltáskor kell egy alapmigráció, és azt az éles ágon lefutottként kell bejegyezni.
- Expand/contract: a migráció a régi kóddal is működjön, az eldobás egy későbbi kiadásban jön.
- Élesítés sorrendje: snapshot → `migrate` a `main`-en → deploy.

## Feat-workflow
| Git | Vercel | Neon |
|---|---|---|
| `main` | Production | `main` |
| `dev` (apró, séma nélküli) | Preview | `preview/dev` |
| `feat/<slug>` (worktree) | Preview | `preview/feat/<slug>` (a `main`-ből, előre létrehozva) |
| a merge előtt álló feature | `test` Custom Env | `test` (minden kör előtt reset a `main`-ből) |

- `feature-start`:
  - worktree és ág az `origin/main`-ből;
  - Neon-ág;
  - worktree `.env`: a nem-DB változók a fő checkoutból, a DB-URL host-cserével vagy a `neonctl connection-string` kimenetéből;
  - `npm ci`;
  - az első commit a spec.
- A worktree-be a `.env`, a `.vercel/` és a `node_modules` nem jön át magától.
- `feature-test`: reset a `test` ágon → `migrate` → `vercel deploy --target=test`
  → e2e és kézi próba. Egyszerre egy feature lehet a `test`-en.
- `feature-finish`: worktree, git-ág és Neon-ág törlése. A Neon-ágat a workflow
  törli, mert az integráció nem teszi meg.
- A `preview/dev` ágat időnként resetelni kell a `main`-ből.
- Opcionális CI: PR-enként ideiglenes `ci/pr-<n>` ág a `main`-ből, rajta
  `migrate`, tesztek és schema-diff, a végén törlés. Párhuzamosan is biztonságos,
  a `test`-kaput nem váltja ki.

## Deploy
- `vercel deploy --prod --skip-domain` → DB-művelet → azonnal `vercel promote`:
  közel állásidő nélküli átállás.
- Ha a git-integráció deployol, a deploymentet a commit alapján keresd meg:
  `vercel ls --environment production --meta githubCommitSha=<SHA>` +
  `vercel inspect --wait`. Bukáskor `vercel inspect --logs`. Rollback csak jóváhagyással.
- Ideiglenes éles env-teszt négy lépés: add → deploy → rm → deploy.
- A preview-DB mérése: `pg_stat_database.xact_commit` a célágon a kérés előtt és után.
