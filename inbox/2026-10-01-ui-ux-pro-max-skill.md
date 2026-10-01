---
date: 2026-10-01
source: claude-settings
kind: skill
---

# UI UX Pro Max skill — bevezetés vizsgálata

**Mi**: a [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)
(v2.15.0, 2026-08-13; ~132k ⭐) egy harmadik féltől származó design-skill: UI-stílusok,
színpaletták, font-párok, UX-szabályok kereshető adatbázisa, és egy „Design System
Generator”, ami a projekt típusából (pl. e-commerce, SaaS, spa/szolgáltatás) teljes
design systemet javasol. Vizsgáljuk meg, hogy bekerüljön-e a globális környezetbe.

**Miért**: a *Fejlesztő* jelölte meg (`/capture ui-ux-pro-max-skill`). Weboldalaknál
(pl. varazskez/hangfurdo, web/estimese) a vizuális irány minden projektnél nulláról
indul. A jelenleg telepített design-eszközök (`frontend-design`, `artifact-design`,
`design:*` plugin) irányelvet adnak, kereshető stílus-/paletta-adatbázist nem.

**Hogyan alkalmazd** (a `/curate` döntéséhez):

- **Telepítési módok** (a README szerint):
  - Plugin: `/plugin marketplace add nextlevelbuilder/ui-ux-pro-max-skill`, majd
    `/plugin install ui-ux-pro-max@ui-ux-pro-max-skill`.
  - CLI: `ui-ux-pro-max-cli` npm-csomag (`uipro init --ai claude --global` →
    `~/.claude/skills/`). A régi `uipro-cli` elavult, ne azt.
  - A keresőscript Python 3, csak standard library, hálózati hívás nélkül.
- **Mielőtt bekerül, ellenőrizd**:
  - Átfedés és ütközés a `frontend-design` skillel (mindkettő „distinctive UI”-ra
    triggerel) — melyik nyerjen, vagy a description szűkítése kell.
  - A `stack.md` szerint `npm` kizárt: a plugin-telepítés vagy `pnpm dlx` legyen,
    ne `npm install -g`.
  - Third-party skill: a teljes skill-tartalmat és a scripteket olvasd át
    telepítés előtt (prompt-injection, hálózat).
  - Egy valós projekten próbáld ki (design system generálás egy landing page-hez),
    és vesd össze a `frontend-design` kimenetével.
- **Lehetséges kimenet**: plugin-telepítés a `settings.user.json`-ba
  (`enabledPlugins` + marketplace), vagy elvetés, ha a `frontend-design` lefedi.
