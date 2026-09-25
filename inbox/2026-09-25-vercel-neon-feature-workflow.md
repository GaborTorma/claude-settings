---
date: 2026-09-25
source: varazskez
kind: skill
---

# Feature-workflow Vercel + Neon projektben (worktree, preview-ág, test-kapu)

## Mi

Minden nem-`main` git-ághoz egy `preview/<git-ág>` Neon-ág tartozik, ezen dolgozik
a lokális worktree és a Vercel-preview is. Merge előtt a feature egy `test` Vercel
Custom Environmenten megy át, egy friss éles másolaton (`test` Neon-ág), hogy a
migráció valódi adatokon is lefusson.

## Miért

- A Vercel-integráció az **előre létrehozott** `preview/<git-ág>` Neon-ágat
  újrahasznosítja (mérve: az ág `pg_stat_database.xact_commit` értéke nőtt a
  preview-kérésekre). A lokális fejlesztés és a preview így ugyanazt a DB-t látja,
  már az első commit előtt is. Üres git-ágra az integráció nem nyit Neon-ágat,
  csak az első commitos pushra.
- A preview-ág a feature indulásakor másolódik a `main`-ből, merge-kor tehát elavult:
  nem tartalmazza az azóta érkezett éles adatokat és a többi feature migrációit.
  A migrációt ezért egy friss másolaton kell kipróbálni.
- A Vercel által kezelt Neon-integráció a git-ág törlésekor **nem** törli a
  Neon-ágat. Csak akkor törli, ha az utolsó hozzá tartozó deployment is törlődik,
  ami a megőrzési szabály miatt hónapokig tarthat. A takarítást ezért a
  workflow-nak kell elvégeznie. (A Neon által kezelt integráció a git-ág
  törlésekor töröl.)
- A `vercel env pull` az integráció projekt-szintű változóit adja, ezek minden
  targeten a `main`-re mutatnak. A preview-ág értékeit az integráció deploymentenként
  injektálja, ezért a `vercel env pull --git-branch` nem használható. A lokális
  `.env`-et a Neon felől kell előállítani.
- Az éles másolaton futó nem-éles környezet (preview, `test`, lokális) valódi
  ügyfeleknek küldhet levelet, ha az SMTP ott is be van állítva.

## Hogyan alkalmazd

**Topológia**

| Git | Vercel | Neon-ág |
|---|---|---|
| `main` | Production | `main` |
| `dev` (apró, séma nélküli javítások) | Preview | `preview/dev` |
| `feat/<slug>` (saját worktree) | Preview | `preview/feat/<slug>` (a `main`-ből) |
| a merge előtt álló feature | `test` Custom Environment (Pro csomag) | `test` (minden kör előtt reset a `main`-ből) |

**Előfeltételek**
- Verziózott migrációk: `drizzle-kit generate` és `migrate`. A `push` csak a saját
  feature-ágon, iterálás közben megengedett. Ha a DB korábban `push`-sal épült,
  kell egy alapmigráció, és azt az éles ágon lefutottként kell bejegyezni.
- Nem-éles levél-átirányítás (pl. `MAIL_REDIRECT_TO`) a preview, `test` és
  lokális környezetekre, valamint Stripe teszt-kulcs.
- `neonctl` és `NEON_API_KEY` a keychainben. A Vercel által kezelt szervezetben a
  `neonctl` csak `--api-key`-vel működik.

**`feature-start <slug>`**
1. `git worktree add ../<repo>-<slug> -b feat/<slug> origin/main`
2. Neon-ág `preview/feat/<slug>` a `main`-ből (Neon MCP `create_branch` vagy
   `neonctl branches create --parent main`).
3. A worktree `.env`-je: a nem-DB változók a fő checkoutból, a DB-URL-ek az új
   ágra. A `neonctl env pull` `DATABASE_URL`/`DATABASE_URL_UNPOOLED` néven ír; ha a
   kód más nevet olvas (pl. `POSTGRES_URL`), a script írja be a kapcsolati stringet
   (`neonctl connection-string <ág> --pooled`). Az ágak öröklik a szerepkört és a
   jelszót, ezért elég a hostot kicserélni.
4. `npm ci`. Az első commit a spec, a push után a preview ugyanerre az ágra megy.

**`feature-test <ág>`** (merge előtt)
1. `reset_from_parent` a `test` Neon-ágon, hogy friss éles másolat legyen.
2. `migrate` a `test` ágon.
3. `vercel deploy --target=test` a feature commitjából.
4. E2E és kézi próba az állandó `test` URL-en. Egyszerre egy feature lehet a
   `test`-en, ez a staging-kapu természetes sora.

**A `test` környezet beállításakor** a Neon Marketplace-erőforrás **ne legyen**
a `test` környezethez kapcsolva. Ha kapcsolódik, a `main`-re mutató változóit
injektálja, és azok felülírják a kézi DB-URL-t. A Neon dokumentációja a Custom
Environment támogatást csak a Neon által kezelt integrációnál írja le. Ezért
az első deploy után mérd: az `xact_commit` a `test` ágon nőjön, a `main`-en ne.

**Élesítés** (a *Fejlesztő* futtatja; a Claude Code szűrője a prod deployt tiltja)
1. Snapshot a `main` Neon-ágról.
2. `migrate` a `main`-en.
3. `vercel deploy --prod` (vagy `--skip-domain` és utána `vercel promote`).

A migráció visszafelé kompatibilis legyen (expand/contract): a régi kód még fut
alatta, a régi oszlop csak egy későbbi kiadásban esik ki.

**`feature-finish`** a merge után: a worktree, a git-ág és a
`preview/feat/<slug>` Neon-ág törlése. A Neon-ág törlése visszafordíthatatlan,
ezért előtte kérdezz. A `preview/dev` ágat időnként resetelni kell a `main`-ből.

**Később (opcionális)**: GitHub Action PR-enként egy ideiglenes `ci/pr-<n>`
Neon-ággal a `main`-ből (`neondatabase/create-branch-action`, `expires_at`),
amelyen a `migrate`, a tesztek és a `schema-diff-action` fut, a végén
`delete-branch-action`. Ez párhuzamosan is biztonságos automatikus ellenőrzés,
de a kézi `test`-kaput nem váltja ki.

**Nyitott**: a személyes adatok miatt a fejlesztői ágak alapja lehetne egy
anonimizált ág (Neon `branch_anonymized`). Ez még béta, és reset sem működik
rajta.
