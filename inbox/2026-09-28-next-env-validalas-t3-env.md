---
date: 2026-09-28
source: claude-settings
kind: skill
---

# Next.js env-validálás: `@t3-oss/env-nextjs` + buildkori import

## Mi

Next.js projektben a `rules/enviroment.md` **Validálás** szabályát (kötelező
env-változók egy helyen, séma alapján, azonnali hibával) a `@t3-oss/env-nextjs`
valósítsa meg, és a `next.config.ts` importálja a `src/env.ts`-t, hogy már a
`next build` elbukjon hibás env-vel.

## Miért

- A sima zod-séma (`safeParse(process.env)` + `z.prettifyError`) szerveroldalon
  elég, de a `NEXT_PUBLIC_*` változók **buildkor beégnek** a kliens-bundle-be —
  ezeket külön kell kezelni. A `@t3-oss/env-nextjs` ugyanazt a zod-sémát
  `server` / `client` részre bontja, és kliensoldalon megakadályozza a
  szerver-titkok elérését.
- A buildkori import miatt Vercelen a hibás env-vel induló deploy **el sem
  készül** — a `/release` a build hibájánál megáll, élesre nem kerül semmi. Ez
  váltja ki a deploy-checklistet („állítsd be az új env-et”): a hiány hiba, nem
  emlékeztető.

## Hogyan alkalmazd

- Majd ha Next.js stack skill / plugin készül (pl. a `vercel-neon` mellé), ott
  legyen a bootstrap része: `src/env.ts` a `@t3-oss/env-nextjs` `createEnv`-vel
  (`server`, `client`, `runtimeEnv`), `next.config.ts`-ben `import "./src/env";`.
- A kód csak az `env` objektumot használja, a `process.env`-et közvetlenül nem.
- A `.env.example` ugyanazt a kulcslistát tartalmazza, placeholderrel.
- Implementáció előtt a `@t3-oss/env-nextjs` és a zod aktuális docsát Context7-ből
  (a zod v4-es API-t — pl. `z.stringbool()` — ellenőrizni kell).
