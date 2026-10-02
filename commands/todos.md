---
name: todos
description: A projekt összes teendőjének listája — a .parked.md parkoló tételei és a nyitott GitHub issue-k egyben, kérdés nélkül. Használd amikor a Fejlesztő /todos-t ír, vagy azt kérdezi, milyen teendők vannak összesen.
allowed-tools: Bash(cat .parked.md *), Bash(gh issue list *)
---

## Kontextus

- Parkoló: !`cat .parked.md 2>/dev/null || echo "NINCS"`
- Issue-k: !`gh issue list --state open --limit 50 --json number,title,labels,url 2>&1 || echo "HIBA"`

## Lista

A sessionbe, két blokkban. Csak lista — nincs `AskUserQuestion`, nincs folytatás;
indulni a `/pick`-kel lehet.

```markdown
**Parkolóban:**

- <ID> · <parkolt tétel> — *Fejlesztő* | *AI*

**Issue-k:**

- **feature**
   - [#<szám>](<URL>) · <cím>
- **fix**
   - [#<szám>](<URL>) · <cím>
```

- **Parkolóban**: tétel a `**PNN** · ` kezdetű sor, a `<!-- next id -->` számláló nem;
  a tétel végi dátum (`· <YYYY-MM-DD>`) nem jelenik meg.
- **Issue-k**: címke szerint (`feature`, `fix`, címke nélkül), a csoporton belül szám
  szerint; üres csoport kimarad. `HIBA` → a blokk helyén a fölötte lévő hiba egy sorban.
- **Üres blokk kimarad**: nincs parkoló tétel (`NINCS` vagy üres) → nincs Parkolóban
  blokk; nincs nyitott issue → nincs Issue-k blokk. Ha egyik sincs: csak ennyi —
  `Nincs teendő.`
