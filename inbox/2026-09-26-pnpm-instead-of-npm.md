---
date: 2026-09-26
source: claude-settings
kind: rule
---

# pnpm az npm helyett

**Mi:** Node/TypeScript projektekben a csomagkezelő a `pnpm`, nem az `npm`.

**Miért:** A *Fejlesztő* explicit preferenciája (`/capture use pnpm instead of npm`).
Konkrét hibából nem jött; a `rules/stack.md` jelenleg nem rögzít csomagkezelőt,
ezért a sessionök alapból `npm`-et használnak.

**Hogyan alkalmazd:**

- Új projektnél `pnpm init` / `pnpm create …`, függőség `pnpm add` (`-D` dev-hez),
  scriptek `pnpm <script>`, egyszeri futtatás `pnpm dlx` (nem `npx`).
- Lockfile: `pnpm-lock.yaml`; `package-lock.json` ne kerüljön a repóba.
- Meglévő projektnél a lockfile dönt: ha `package-lock.json` / `yarn.lock` van,
  ne válts csendben — kérdezd meg a *Fejlesztő*t, migráljunk-e.
- Vercel a `pnpm-lock.yaml`-ból magától felismeri a pnpm-et.
- Curate-jelölt helye: `rules/stack.md` Preferenciák / Kizárások (`npm` → kizárás?).
