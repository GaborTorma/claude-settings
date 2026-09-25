---
date: 2026-09-25
source: claude-settings
kind: skill
---

# Vercel + Neon projekt-életciklus — címszavakban

**Mi**: egy webes app teljes útja egy helyen: Vercel init → Neon init → driver →
feat → deploy.

**Miért**: a részletek szét vannak szórva (`vercel-neon` plugin 5 skillje,
hivatalos `vercel` plugin, `/commit-push-pr-merge-deploy`), a sorrend és az
átmenetek sehol nincsenek egyben. Jelölt: a `vercel-neon` router-skill
bővítése, vagy a deferred `ship` plugin (lásd `deferred/2026-09-22-pm2.md`).

**Hogyan alkalmazd**: új projekt vagy új app-mappa bekötésekor ezen a listán
végigmenni, lépésenként a hivatkozott skillre ugrani.

## 0. Stack-döntés

- stack-döntés előbb (`rules/stack.md`: nincs default, 2–3 opció)

## 1. Vercel init

- `git init` → `.gitignore` + `.env.example` az első commitban
- `vercel link --scope <team>` — app-mappánként, monorepóban több `.vercel/`
- régió **`fra1`**: `vercel.json` `"regions"` + projekt `serverlessFunctionRegion`
- egy app ↔ egy Vercel projekt ↔ egy Neon projekt, azonos név
- MCP-ellenőrzés: Vercel `list_projects` (azonosító: `prj_…`)

## 2. Neon init

- régió az **első** döntés, utólag nem változtatható → `aws-eu-central-1`
- `vercel integration add neon --metadata region=fra1` (Vercel-régiónév!)
- Neon MCP `create_project` **nem megy** („organization is managed by Vercel")
- ellenőrzés: Neon `list_projects` — régió, `NEON_PROJECT_ID` a Vercel env-ben
- branchek: `main` (éles) · `dev` (kézzel) · `test` · `preview/<git-branch>` (Vercel hozza)
- `neondb` ≠ feltétlenül a mi DB-nk

## 3. Env

- integráció írja: `POSTGRES_URL`, `POSTGRES_URL_NON_POOLING`, `NEON_PROJECT_ID` — nem nyúlunk hozzá
- kézzel: `DATABASE_URL` (pooled), `DATABASE_URL_UNPOOLED` (direct)
- preview ≠ production: `vercel env add DATABASE_URL preview [--git-branch=…]`
- development → `dev` Neon branch; `vercel env pull` → `.env.local`
- egy névkészlet projektenként, `.env.example` mondja ki
- env csak új deploymentre hat

## 4. Driver

- alap: `@neondatabase/serverless` + `drizzle-orm/neon-http`
- interaktív tranzakció → `neon-serverless` (WebSocket), útvonalanként
- `node-postgres` Pool → csak indokolva, `attachDatabasePool`-lal
- futásidő = pooled (`-pooler`), DDL / `drizzle-kit` = unpooled
- build-time import → lusta `getDb()`, nem `Proxy`
- env-betöltés a futtatóé: `drizzle-kit` nem olvas `.env.local`-t → `process.loadEnvFile`

## 5. Séma / migráció

- stílus projektenként: `drizzle-kit push` (kis app) **vagy** `generate` + `migrate` (értékes adat)
- `push` éles ellen soha
- kockázatos változás előtt `create_snapshot`
- kézi éles SQL: `prepare_database_migration` → `complete_database_migration`
- `run_sql` alapból `main`-re megy — írás előtt branch kimondva

## 6. Feat

- branch a `main`-ről, preview deploy PR-onként
- preview DB = `preview/<git-branch>` Neon ág, env bekötve
- SSO-védett preview → `vercel curl` / `access-protected-vercel-deployment`
- pre-commit gate: lint, typecheck, teszt
- cron → `CRON_SECRET` ellenőrzés kódban; `NEXT_PUBLIC_` soha titokkal

## 7. Deploy

- `/commit-push-pr-merge-deploy`: gate → PR → merge → deploy
- Git-integráció: merge már deployol → `vercel ls --environment production --meta githubCommitSha=<SHA>` + `vercel inspect --wait`
- nincs integráció → `vercel deploy --prod`
- bukás → `vercel inspect --logs`, rollback csak jóváhagyással
- seed után redeploy, ha edge-cache van
- secret-rotálás: rotate → minden target kézi `DATABASE_URL` → `env pull` → redeploy
- ideiglenes env-teszt = 4 lépés (add → deploy → rm → deploy)
