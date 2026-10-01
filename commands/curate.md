---
name: curate
description: A claude-settings inbox feldolgozása — minden összegyűlt tanulságról eldől, hogy rule lesz, skill lesz, elvetjük, vagy halasztjuk. Használd amikor a Fejlesztő /curate-et ír, vagy az inboxban összegyűlt néhány bejegyzés.
allowed-tools: Bash(readlink ~/.claude/rules), Bash(ls *), Bash(git -C * add *), Bash(git -C * commit *), Bash(git -C * mv *), Bash(git -C * rm *), Bash(git -C * push), Bash(claude plugin *), Read, Write, Edit
---

## Kontextus

- Rules: !`readlink ~/.claude/rules || echo "NINCS"`

Az `inbox/` a más projektekből érkezett tanulságok gyűjtőhelye. Ez a parancs
dönti el a sorsukat. Felderítéssel kezdj; mutáció csak a *Fejlesztő* jóváhagyása
után.

## 1. Leltár

`$REPO` = a Kontextus **Rules** sorának szülőmappája; `$PLUGINS` = mellette a
`claude-plugins` (ha nincs ott, kérdezd meg, hol van). Ha a **Rules** sor `NINCS` (nincs
symlink), állj meg és szólj, hogy a claude-settings nincs telepítve ezen a gépen.

```bash
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

**skill** → a plugin-repóba (`$PLUGINS`, a `torma-ai` marketplace forrása), a
témájához illő plugin `skills/` mappájába. Ha egyik pluginhoz sem illik, kérdezd
meg, legyen-e új plugin. A verzió egyetlen forrása a `plugin.json`; a
marketplace-bejegyzés nem ismétli. Pluginenként:

```bash
claude plugin validate "$PLUGINS/<plugin>" --strict
# bump: <plugin>/.claude-plugin/plugin.json version — minor, ha új skill; patch, ha pontosítás
git -C "$PLUGINS" add <plugin>/
git -C "$PLUGINS" commit -m "feat(<plugin>): add <skill> skill"
#                       vagy: "docs(<plugin>): clarify <skill> <mit>"
git -C "$PLUGINS" push
(cd "$PLUGINS" && claude plugin tag <plugin> --push)
claude plugin marketplace update torma-ai
claude plugin update <plugin>@torma-ai
```

A `claude-plugins` a `main`-re commitol, PR nélkül. A frissített plugin a
**következő sessionben** lép életbe.

**elvetés** → töröld a fájlt, de a commit üzenetben írd le, miért.

**halasztás** → `git mv` az `inbox/deferred/`-be; a frontmatterbe
`deferred: <YYYY-MM-DD>`, a törzs elejére egy **Miért halasztva** bekezdés —
mi hiányzik a döntéshez.

## 4. Lezárás

A feldolgozott inbox-fájlokat töröld (a halasztottak a `deferred/`-ben maradnak) —
az inbox nem archívum, arra a git history való. A plugin-repó commitja (3. lépés)
már kész; a claude-settings egy commitot kap, közvetlenül a `main`-re:

```bash
git -C "$REPO" add -A rules/ inbox/
git -C "$REPO" commit -m "<subject>" -m "<body>"
git -C "$REPO" push
```

- **Subject**: ha rule változott `docs(rules): <mi került be>` (pl.
  `docs(rules): add worktree cleanup steps`), különben `chore(inbox): curate <n> entries`.
- **Body**: bejegyzésenként egy sor —
  `- <fájl>: rule → rules/<téma>.md` · `skill → <plugin>/<skill> (<verzió>)` ·
  `elvetve — <miért>` · `halasztva — <mi hiányzik>`.
