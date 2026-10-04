---
date: 2026-10-04
source: git-graph
kind: skill
---

# Kötött, specifikus commit-scope-ok és olvasható changelog

## Mi

A Conventional Commits scope-ja projektenként egy rögzített, specifikus
listából jöjjön (nem bővül magától menet közben), és a `git cliff` changelogja
a scope-ot normálisan, csoportosítva jelenítse meg — ne minden sor elé dőlt
`*(scope)*` előtagként.

## Miért

A git-graph v0.11.0 kiadásánál (`/release`) a `CHANGELOG.md` Features-szakasza
~80 sorból állt, szinte mind `- *(page)* …` kezdettel:

```
### 🚀 Features

- *(page)* Redesign the page in the Claude app's look
- *(page)* Add commit search and the new palette to the loader
- *(page)* Replace the native branch select with a menu in the app's style
…
```

Két ok:
- **A scope túl általános volt.** Egy UI-redesign ágon minden commit
  `feat(page)` / `fix(page)` / `style(page)` lett, mert a `/commit` a
  fájlútból (`page/`) vezette le a scope-ot, és nem volt rögzített lista.
  Így a scope semmit nem különböztetett meg (keresés, billentyűzet, lábléc,
  fájlikonok mind `page`).
- **A cliff-sablon** (`commit.scope` dőlt előtagként a sor elején) a
  sok egyforma scope-ot zajként ismétli, a changelog nehezen olvasható.

## Hogyan alkalmazd

- **Scope-lista a projekt `CLAUDE.md`-jében** (pl. `## Konvenciók` → `Scope`):
  a projekt funkcionális területei (pl. `search`, `keyboard`, `row`, `footer`,
  `icons`, `mcp`, `hook`), nem a mappanevek. A `/commit` ebből választ; ha
  egyik sem illik, **kérdez**, és a *Fejlesztő* dönt, bővül-e a lista — magától
  nem talál ki újat. Lista híján (új projekt) javasoljon egyet az első
  commitoknál.
- **A cliff-sablon** (`cliff.toml` `body`): a scope ne dőlt előtag legyen;
  csoportosítson scope szerint a típuscsoporton belül (alcím vagy félkövér
  csoportcím, alatta a sorok scope nélkül), vagy írja `**scope:** üzenet`
  formában. A scope nélküli commitok külön, „Egyéb” alatt.
- A `/release` a changelog generálása után nézze meg az eredményt: ha egy
  scope a sorok nagy többségén ismétlődik, jelezze, hogy a scope-lista túl
  durva.
