---
name: commit-push-pr-merge-deploy
description: Commit + push + PR + merge a mainbe + production deploy egy menetben. Használd amikor a Fejlesztő /commit-push-pr-merge-deploy-t ír, vagy egy kész branch munkáját azonnal élesíteni akarja.
argument-hint: "PR cím vagy kontextus (opcionális)"
---

A `commit-push-pr-merge` folyamata, utána production deploy a friss `main`-ről.
A command meghívása maga a deploy-engedély — de csak akkor, ha az előző lépések
hibátlanul lefutottak.

## 1. Merge

Hívd a `commit-push-pr-merge` commandot a `Skill` toollal; ha a *Fejlesztő*
adott argumentumot, add át `args`-ként.

Ha bármelyik lépése megállt (elbukott gate, nem mergelhető PR), **itt is állj
meg** — deploy nincs. Siker után jegyezd fel a merge commit SHA-ját:

```bash
git rev-parse HEAD
```

## 2. Deploy-mód felderítése

Az első találat nyer:

1. **Projekt `CLAUDE.md`** deploy parancsot ír → azt futtasd.
2. **`package.json` `deploy` script** → a lockfile szerinti package managerrel
   (`pnpm`/`yarn`/`bun`/`npm run deploy`). **`Makefile` `deploy` target** → `make deploy`.
3. **Vercel** (`.vercel/project.json` vagy `vercel.json`) → lásd 3. lépés.
4. **PM2** (`ecosystem.config.js` `deploy` szekcióval) →
   `pm2 deploy ecosystem.config.js production`.
5. **Egyik sem** → **állj meg**, kérdezd meg a *Fejlesztő*t, mivel deployol.
   Ne találj ki deploy-módot.

## 3. Vercel

Ha a projekt Git-integrációval van bekötve, a merge a `main`-re **már elindította**
a production deployt — ne indíts másodikat. Keresd meg a merge SHA-hoz tartozót
(max. ~2 percig ismételve, mert a webhook késhet):

```bash
vercel ls --environment production --meta githubCommitSha=<SHA>
```

- **Van találat** → várd ki: `vercel inspect <url> --wait --timeout 15m`
- **Nincs találat** (nincs Git-integráció) → `vercel deploy --prod`

## 4. Ellenőrzés és lezárás

- **Sikeres** deploy → írd ki: PR szám + URL, merge SHA, deploy URL és státusz.
- **Elbukott** deploy → mutasd a build logot (Vercelnél
  `vercel inspect <url> --logs`), és **állj meg**. Rollbacket (`vercel rollback`,
  `git revert`) csak a *Fejlesztő* jóváhagyásával — a merge ekkor már a `main`-en van.
