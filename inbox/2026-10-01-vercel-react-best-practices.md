---
date: 2026-10-01
source: claude-settings
kind: ?
---

# Vercel React Best Practices skill — már megvan a `vercel` pluginben

**Mi**: a [claudecowork.im/resources/vercel-react-best-practices](https://claudecowork.im/resources/vercel-react-best-practices)
által ajánlott skill (forrás: `vercel-labs/agent-skills`, `skills/react-best-practices`)
**már telepítve van** a hivatalos `vercel` pluginnel `vercel:react-best-practices` néven.
Külön telepíteni nem kell; legfeljebb arról kell dönteni, hogy elég-e a plugin-változat.

**Miért**: a *Fejlesztő* jelölte meg (`/capture <url>`). Az oldal ezt a telepítést javasolja:
`npx skills add vercel-labs/agent-skills --skill vercel-react-best-practices --agent claude-code`.
Ez projektbe (`.claude/skills/`) telepít, és `npx`-et használ (a `stack.md` szerint az `npm` kizárt).
Duplikátumot hozna létre a pluginben lévő skill mellé.

A plugin-változat (`vercel` 0.50.0,
`~/.claude/plugins/cache/claude-plugins-official/vercel/0.50.0/skills/react-best-practices/`):

- A törzs és a `rules/` könyvtár az upstreamből jön: 64 szabály 8 kategóriában, hatás szerinti
  prioritással (`async-` waterfall és `bundle-` CRITICAL → `server-` HIGH → `client-` → `rerender-`
  → `rendering-` → `js-` → `advanced-`). Az `upstream/` alkönyvtárban az eredeti `SKILL.md` is ott van.
- **Eltérés az upstreamtől**: a frontmatter átírva. A description „TSX reviewer, több komponens
  szerkesztése után”. A `pathPatterns` csak `components/**`, `src/components/**`, `app/components/**`,
  `src/ui/**`, `lib/components/**` — az App Router `app/**/page.tsx`, `layout.tsx` fájljai és a
  route handlerek **nincsenek benne**, pedig a CRITICAL `async-`/`server-` szabályok főleg oda szólnak.
  Plusz `validate`/`chainTo`: CSS-in-JS / MUI / Chakra importnál a `shadcn` skillre terel.
- **Verzió-csúszás**: az upstream `rules/` mappában 2026-10-01-én 72 bejegyzés van, a pluginben 66
  (mindkettőben benne van a `_sections.md` és a `_template.md`) → a plugin pár szabállyal le van maradva.

**Hogyan alkalmazd** (a `/curate` döntéséhez):

- **Valószínű kimenet: rule-sor, nem új skill.** Pl. a stack-preferenciákhoz: „React/Next.js kód
  írásakor és review-jánál a `vercel:react-best-practices` skill szabályai (waterfall, bundle,
  server elsőként)”. Így az App Router fájlokra is betöltődik, nem csak a `components/**` alatt.
- A `npx skills add …` telepítést **ne** használd: duplikátum lenne, és `npx`.
- Ha a lemaradás számít: a hiányzó upstream szabályokat a
  `gh api repos/vercel-labs/agent-skills/contents/skills/react-best-practices/rules` listából
  lehet összevetni — de inkább a `vercel` plugin frissítését várjuk meg, mint hogy saját forkot tartsunk.
