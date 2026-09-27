---
date: 2026-09-27
source: pakkly (package-monitor)
kind: rule
---

## Mi

Új függőség verzióját mindig a registry adja (`pnpm add <pkg>` vagy
`npm view <pkg> version`), soha nem a tréning-memória — a manifestbe kézzel
beírt verzió-range tilos.

## Miért

A pakkly bootstrapjánál (2026-09-20, `7d4a0a9`) az *AI* a `package.json`-t
heredoc-kal írta (`cat > … <<'EOF'`), kézzel beírt range-ekkel:
`"ai": "^6.0.0"`, `"@openrouter/ai-sdk-provider": "^2.0.0"`. A registry
`latest` aznap `ai@7.0.107` és `@openrouter/ai-sdk-provider@3.1.0` volt (az
`ai@7.0.0` stabil 2026-06-25 óta). A modell tudás-határán (2026 május) még a
6.x volt a legutolsó stabil, a 7 csak beta — ezt írta be.

A Context7-et lekérdezte, de csak az OpenRouter-providerre; az AI SDK
verzióját semmi nem ellenőrizte. A két régi major konzisztens pár volt, ezért
semmi nem jelzett hibát, a `^6` caret range pedig majorra nem lép — a
lemaradás egy hétig csendben maradt. Egy új modell (Jev,
`experimental_evaluate`) bekötésénél derült ki, hogy az csak az AI SDK 7-ben
érhető el.

A meglévő `context7.md` szabály („előbb olvasd ki a projekt verzióját")
meglévő projektre szól; bootstrapkor nincs mit kiolvasni, ezért nem fogta meg.

## Hogyan alkalmazd

- Új projektnél és új függőségnél a telepítés `pnpm add <pkg>` (`-D`) —
  ez a registry `latest`-jét írja a manifestbe. Ne írj `package.json`-t
  kézzel verziókkal.
- Ha a manifestet mégis kézzel kell összeállítani (pl. monorepo-skeleton),
  előtte `npm view <pkg> version` minden csomagra, és azt írd be.
- A docs-lekérdezés (Context7) után ellenőrizd, hogy a docs verziója egyezik-e
  a telepítettel — a Context7 a legfrissebb docs-ot adja.
- Lehetséges hely: a `context7.md` kiegészítése egy bootstrap-sorral, vagy a
  `stack.md` „Függőségek" pontja.
