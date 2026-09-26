---
name: commit-push-install
description: Plugin-repóban commit + push, majd a módosult pluginek frissítése a lokális Claude Code-ban. Használd amikor a Fejlesztő /commit-push-install-t ír, vagy egy plugin-marketplace repóban végzett változtatást azonnal használni akar.
argument-hint: "commit üzenet vagy kontextus (opcionális)"
---

A marketplace a git remote-ból húz, ezért a lokális szerkesztés csak push után
hat, a telepített plugin pedig csak **verzióváltáskor** frissül. Ez a command a
teljes kört végigviszi: validálás → bump → commit + push → install.

## 1. Repó és marketplace

A munkakönyvtár gyökerében kell lennie `.claude-plugin/marketplace.json`-nak —
ha nincs, **állj meg**: ez nem plugin-marketplace repó. A marketplace neve a
fájl `name` mezője (pl. `torma-ai`).

## 2. Érintett pluginek

A módosult fájlok: a working tree (`git status --porcelain`) és a még nem
pusholt commitok (`git diff --name-only @{u}...HEAD`). Ezek első
útvonal-szegmense azon pluginek listája, amelyek szerepelnek a
`marketplace.json` `plugins[].source` mezőjében.

Ha egyik plugin sem érintett (pl. csak a README változott), a 3–4. lépés
kimarad, a 6. lépésben csak a marketplace frissül.

## 3. Pre-commit gate

Pluginenként:

```bash
claude plugin validate <plugin> --strict
```

Ami elbukik, ott **állj meg** és mutasd a hibát — ne commitolj.

## 4. Verzió-bump

Pluginenként hasonlítsd össze a `<plugin>/.claude-plugin/plugin.json`
`version` mezőjét a remote-on lévővel:

```bash
git show @{u}:<plugin>/.claude-plugin/plugin.json
```

Ha azonos, bump nélkül a `claude plugin update` nem hoz le semmit. Bumpolj:
**patch**, ha pontosítás/javítás; **minor**, ha új képesség (új skill, command,
agent). A verzió egyetlen forrása a `plugin.json` — a `marketplace.json`-ba ne
írd be.

## 5. Commit és push

Hívd a `commit-push` commandot a `Skill` toollal; ha a *Fejlesztő* adott
argumentumot, add át `args`-ként.

## 6. Install

```bash
claude plugin marketplace update <marketplace>
claude plugin update <plugin>@<marketplace>
```

Az `update` pluginenként fut. Ha egy plugin még nincs telepítve, `update`
helyett `claude plugin install <plugin>@<marketplace>`.

Ha a CLI marketplace által deklarált parancs megerősítését kéri, **ne** add
meg `-y`-nal: mutasd a *Fejlesztő*nek, és ő dönt.

## 7. Lezárás

Ellenőrizd a telepített verziót:

```bash
claude plugin list
```

Írd ki pluginenként a régi → új verziót és a pusholt commit rövid SHA-ját. A
frissítés a **következő sessionben** lép életbe — ezt mondd ki.
