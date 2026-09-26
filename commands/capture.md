---
name: capture
description: Tanulság rögzítése a claude-settings inboxába — bárhonnan, a kurációig nem hat semmire. Használd amikor a Fejlesztő /capture-t ír, vagy egy munka során olyan általánosítható tanulság születik, amit a jövőbeli sessionöknek tudniuk kellene.
argument-hint: "mit tanultunk (üresen a beszélgetésből következtetek)"
---

A *Fejlesztő* egy tanulságot akar megőrizni a globális Claude Code környezet
számára. Ez **nem** azonnali szabály: az inboxba kerül, a sorsáról a `/curate`
dönt.

## 1. A repó megtalálása

```bash
REPO="$(dirname "$(readlink ~/.claude/rules)")"
```

Ha a symlink nem létezik, állj meg és szólj, hogy a claude-settings nincs
telepítve ezen a gépen.

## 2. A tanulság megfogalmazása

Ha a *Fejlesztő* adott argumentumot, abból indulj ki; ha nem, a beszélgetésből
következtess — de **csak arra, ami általánosítható**. Ami csak az aktuális
repóban igaz, az annak a projektnek a `CLAUDE.md`-jébe való, nem ide.

Három dolgot írj le, ebben a sorrendben:

- **Mi** — egy mondat, a lényeg
- **Miért** — mi vezetett ide; ez dönti el később, hogy rule vagy skill
- **Hogyan alkalmazd** — konkrétan, hogy egy jövőbeli session tudjon vele kezdeni valamit

Ha a tanulság konkrét hibából jött, idézd a hibaüzenetet vagy a parancsot szó
szerint — egy év múlva az lesz a legértékesebb része.

## 3. Mentés

A fájl: `$REPO/inbox/<YYYY-MM-DD>-<rövid-kebab-slug>.md`, ezzel a frontmatterrel:

```markdown
---
date: <YYYY-MM-DD>
source: <a projekt neve, ahonnan jött>
kind: rule | skill | ?
---
```

A `kind` a legjobb tipped; a `/curate` felülbírálhatja. Rövid, mindig igaz,
viselkedést állító tanulság → `rule`. Feltételes vagy lépésekből álló → `skill`.

Append-only: soha ne szerkessz meglévő inbox-fájlt, mindig újat írj.

## 4. Commit és push

```bash
cd "$REPO" && git add inbox/ && git commit -m "chore(inbox): <slug>" && git push
```

A push azért kell, mert a `sync.sh` csak shell-indításkor fut — enélkül a
tanulság ezen a gépen ragadna.

## 5. Visszajelzés

A válaszban a mentett fájlra **abszolút úttal** hivatkozz, markdown linkként:
`[<fájlnév>](/abszolút/út/inbox/<fájlnév>)`. Az inbox másik repóban van, mint
amiben a session fut, ezért a munkamappához mért relatív link nem nyílik meg.
A megnyitáshoz a `claude-settings` mappának a session mappái között kell
lennie: a `settings.user.json` → `permissions.additionalDirectories` ezt
adja.

Ne nyúlj a `rules/` mappához és a plugin-repóhoz: az a `/curate` dolga.
