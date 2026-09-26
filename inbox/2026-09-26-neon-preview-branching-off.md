---
date: 2026-09-26
source: vercel-neon-test (összevetve: varazskez)
kind: skill
---

## Mi

Ha a Vercel ↔ Neon kapcsolaton ki van kapcsolva a preview-branchelés, a preview deployok csendben az **éles `main`** Neon-ágat kapják — ezt csak a Neon ág-listája mutatja meg, a `vercel env ls` nem.

## Miért

- A `vercel-neon-test`-en egy `chore/pnpm-12` ág commitos pushára (Vercel preview: Ready) a Neonban **nem jött létre** `preview/chore/pnpm-12` ág — `list_branches` `include_deleted: true`, `search: "preview"` → `[]`. A preview build így az éles DB-ből olvasott (itt csak `generateStaticParams`, adat nem sérült; egy migráció, seed, űrlap vagy cron viszont élesbe írt volna, még merge előtt).
- Ugyanez a varazskez-ben működik: a `chore/pnpm` pushára azonnal megjelent a `preview/chore/pnpm` ág `"creation_source": "vercel"`-lel. A különbség tehát projekt-kapcsolatonkénti beállítás, nem az integráció hibája.
- **Félrevezető jel**: a `vercel env ls` mindkét projektben ugyanazt mutatja — a DB-változók egy sorban, `Production, Preview` targettel, `Config` típussal. A deploymentenkénti injektálást nem látja, ezért ebből **nem** dönthető el, hogy a preview melyik ágra megy (a `vercel-neon:vercel-env` skill is ezt írja). Első körben ebből tévesen következtettem.
- A beállításra nincs eszköz se a Vercel MCP-ben (`list_integration_configurations` nem adja vissza a kapcsolat deployment-konfigurációját), se a Vercel CLI-ben; a Vercel docs sem írja le a menüt.
- Vercel-kezelt integrációnál a `preview/<git-ág>` Neon-ág a git-ág törlésekor **nem** törlődik — csak az utolsó hozzá tartozó deployment törlésekor, ami hónapokig tarthat.

## Hogyan alkalmazd

- **Ellenőrzés** (a `/vercel-neon:check`-be való): egy commitos push után egy nem-`main` git-ágra Neon `list_branches` (`search: "preview"`, `include_deleted: true`). Ha a Vercel preview Ready, de nincs `preview/<git-ág>` ág `creation_source: vercel`-lel → a preview az éles DB-n fut. Ne a `vercel env ls`-ből következtess.
- **Javítás** (dashboard, a *Fejlesztő* kattintja; a pontos menünevek eltérhetnek): Vercel → **Storage** → a projekt Neon adatbázisa → **Projects** fül → a projekt sora **⋯** → Deployments Configuration → **Preview** bejelölve + **„Create database branch for deployment”**. Utána ismét push-teszt és `list_branches`.
- **Új projektnél** (`vercel-neon:init-workflow` 5. lépés): a bekötés után azonnal ez a push-teszt, ne csak a production-deploy ellenőrzése.
- **Takarítás**: git-ág merge/elvetés után a `preview/<git-ág>` Neon-ágat kézzel kell törölni (`delete_branch`, a *Fejlesztő* jóváhagyásával) — a git-ág törlése nem viszi magával.
