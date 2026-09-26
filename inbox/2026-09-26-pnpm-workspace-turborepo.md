---
date: 2026-09-26
source: claude-plugins (a Vercel-es projektek áttekintése: vercel-neon-test, package-monitor, Manas2026, MicrOasis2026, varazskez, Fertőszentmiklós, Torma.AI, nuxt-framework, super-test, varazskéz-hangfürdő)
kind: rule
---

## Mi

Vercel/Node projektben a csomagkezelő mindig pnpm, pinelt `packageManager` + `engines.node` mezővel. Monorepóhoz pnpm workspace kell; Turborepót csak konkrét ok esetén használunk.

## Miért

- A „pnpm vagy turborepo?” kérdés hamis dilemma: a pnpm csomagkezelő (és workspace), a Turborepo pedig task-runner/cache egy workspace *fölött*. A tényleges döntés: egy csomag → pnpm workspace → workspace + Turbo.
- 10 Vercel-es projekt áttekintése után egyiknél sem lett volna ideális a Turbo:
  - `package-monitor` (pakkly): pnpm workspace (`apps/api`, `apps/web`, `packages/core`) + Vercel Services, egy projekt, egy deploy. Build-lépése csak a `web`-nek van → a Turbónak nincs mit cache-elnie; a `pnpm -r` / `--filter` elég.
  - `Manas2026`, `MicrOasis2026`: `apple/` (Swift) + `pwa/` → a Turbo a Swift-részt nem látja, semmit nem nyerne.
- Két tényleges hiba derült ki:
  - 3 projekt npm-et használ (`varazskez/hangfurdo`, `Fertőszentmiklós/web`, `Torma.AI` — `package-lock.json`), holott az npm kizárt.
  - 5 pnpm-es projektből hiányzik a `packageManager` mező (`Manas2026/pwa`, `MicrOasis2026/pwa`, `nuxt-framework`, `super-test/nuxt-app`, `varazskéz-hangfürdő`) → a Vercel a lockfile-ból találgatja a pnpm verziót, a lokális és a build környezet elcsúszhat.
- Jó minta: `vercel-neon-test` (`"packageManager": "pnpm@11.1.3"`, `"engines": { "node": "24.x" }`).

## Hogyan alkalmazd

A `stack.md`-be (vagy a `vercel-neon` bootstrapbe) javasolt sorok:

```
- **Csomagkezelő**: pnpm, `packageManager` + `engines.node: "24.x"` mindig a package.json-ban.
- **Monorepo**: pnpm workspace, ha több deployolható rész vagy közös csomag van.
- **Turborepo**: csak ha (a) több Vercel projekt jön egy repóból (→ `turbo-ignore` az érintetlen deployok kihagyására), vagy (b) a build/test annyira lassú, hogy megéri a cache (lokális + Vercel Remote Cache). Addig `pnpm -r` / `--filter`.
```

- Új projekt bootstrapnél: `packageManager` és `engines.node` az első commitban.
- Meglévő projekt érintésekor: ha `package-lock.json` van, vagy hiányzik a `packageManager`, jelezd a *Fejlesztő*nek.
- Turbo 2.x-ben a `turbo.json` kulcsa `tasks` (az 1.x-es `pipeline` elavult) — a régi `WSL/turborepo` még `pipeline`-t használ.
