---
name: check
description: A projekt ellenőrzései (lint, typecheck, test, format) az aktuális állapoton. Használd amikor a Fejlesztő /check-et ír, vagy egy command/skill ellenőrzést kér.
---

Az aktuális munkakönyvtár állapotán le kell futtatni a releváns ellenőrzéseket
(**lint, typecheck, unit/e2e tests, format**). Ha a projektben létezik az adott eszköz,
**kötelező** futtatni — ha hiányzik, kihagyható.

## 1. Detektálás

Elsőként a projekt `CLAUDE.md`-je (**Check** sor). Ha ott nincs, `package.json` scripts,
`pyproject.toml`, `Makefile` alapján — vagy ha nem egyértelmű, kérdezd meg egyszer —,
és az eredményt írd be egy sorban a projekt `CLAUDE.md`-jébe
(`- **Check**: <parancsok>`; a régi nevű sort erre nevezd át).

## 2. Futtatás

Mindegyiket, sorban. Ha egy elbukik, a többit nem kell futtatni.

## 3. Válasz

Siker:

```markdown
Check: lint ✓ · typecheck ✓ · test ✓ · format ✓
```

Bukás:

```markdown
Check: <ellenőrzés> ✗

Hiba: <röviden a hiba lényege>
```

- **Check-sor**: csak a ténylegesen lefutott ellenőrzések.
- **Nem futott semmi** (nincs eszköz a projektben): csak ennyi — `Check: nincs ellenőrzés.`
- **Másik commandból hívva**: a hívó a saját válaszába teszi a Check-sort (→ annak
  Válasz-formája), külön nem írod ki. Bukásnál a hívó **megáll**.
