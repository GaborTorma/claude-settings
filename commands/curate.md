---
name: curate
description: A claude-settings inbox feldolgozása — minden összegyűlt tanulságról eldől, hogy rule lesz, skill lesz, elvetjük, vagy halasztjuk. Használd amikor a Fejlesztő /curate-et ír, vagy az inboxban összegyűlt néhány bejegyzés.
---

Az `inbox/` a más projektekből érkezett tanulságok gyűjtőhelye. Ez a parancs
dönti el a sorsukat. Felderítéssel kezdj; mutáció csak a *Fejlesztő* jóváhagyása
után.

## 1. Leltár

```bash
REPO="$(dirname "$(readlink ~/.claude/rules)")"
ls "$REPO"/inbox/*.md "$REPO"/inbox/deferred/*.md
```

Ha csak a README van benne, mondd meg és állj meg. A `deferred/` fájljait
listázd külön, a `deferred:` dátumukkal — újra döntésre csak akkor kerülnek, ha
a *Fejlesztő* kéri.

Olvasd el mindet, és csoportosítsd téma szerint — két bejegyzés ugyanarról egy
helyre való, nem kettőbe.

## 2. Döntés bejegyzésenként

**rule** — rövid, mindig igaz, viselkedést állít. Minden session kontextusába
betöltődik, ezért drága: ha nem minden projektben igaz, nem rule.

**skill** — feltételesen kell, vagy hosszabb néhány bekezdésnél. Csak a
`description` van a kontextusban, a törzs invokáláskor töltődik. Ide tartozik
minden, aminek lépései vannak.

**elvetés** — egyszeri eset, a projekt saját `CLAUDE.md`-jébe való, vagy már
szerepel valahol.

**halasztás** — a *Fejlesztő* még nem tudja eldönteni (pl. nincs meg a célplugin).

Mutasd a javaslatodat bejegyzésenként egy sorban, és kérj jóváhagyást —
`AskUserQuestion`-nel, ha 2-4 közül kell választani.

## 3. Végrehajtás

**rule** → `$REPO/rules/<téma>.md`. Ha a téma már létezik, **abba** írd bele, ne
csinálj újat. Tartsd a meglévő fájlok hangnemét: tömör, felsorolásos.

**skill** → a plugin-repóba (`GaborTorma/claude-plugins`, a `torma-ai`
marketplace forrása), a témájához illő plugin `skills/` mappájába. Ha egyik
pluginhoz sem illik, kérdezd meg, legyen-e új plugin. Utána:

```bash
claude plugin validate <plugin> --strict
```

majd bump a plugin `plugin.json`-jában — patch, ha pontosítás; minor, ha új
képesség —, és kiadás:

```bash
claude plugin tag <plugin> --push
```

A verzió egyetlen forrása a `plugin.json`; a marketplace-bejegyzés nem ismétli.

**elvetés** → töröld a fájlt, de a commit üzenetben írd le, miért.

**halasztás** → `git mv` az `inbox/deferred/`-be; a frontmatterbe
`deferred: <YYYY-MM-DD>`, a törzs elejére egy **Miért halasztva** bekezdés —
mi hiányzik a döntéshez.

## 4. Lezárás

A feldolgozott inbox-fájlokat töröld (a halasztottak a `deferred/`-ben maradnak) — az inbox nem archívum, arra a git history
való. Commitolj mindkét érintett repóban.
