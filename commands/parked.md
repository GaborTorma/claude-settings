---
name: parked
description: Az aktuális munka és a parkoló témák kiírása, majd kérdés a folytatásról. Használd lezáráskor (→ focus.md), amikor a Fejlesztő /parked-ot ír, vagy azt kérdezi, mi van nyitva, mi parkol.
allowed-tools: Bash(git status *), Bash(cat .parked.md *), Skill(pick *), Skill(unpark *), Skill(issue *), Skill(push *)
---

## Kontextus

- Git: !`git status -sb`
- Parkoló: !`cat .parked.md 2>/dev/null || echo "NINCS"`

## 1. Összegyűjtés

- **Aktuális**: ha van még teendő az aktuális témával — a folyamatban lévő munka
  ebben a sessionben, és a félbemaradt munka a Kontextusból (commitolatlan
  változás). Commitolt, de nem pusholt munka nem aktuális.
- **Parkolóban**: a Kontextus **Parkoló** sora — a `.parked.md` tételei; tétel a `**PNN** · ` vagy `**PNN** ▶ · ` kezdetű sor, a `<!-- next id -->` számláló nem; `NINCS` → üres.
- **Pick-elt** (`▶`) tétel: ha a munkája lezárult (commitolva, nincs vele teendő) →
  `/unpark <ID>`, és a listába már nem kerül be; ha még tart, ő az **Aktuális**.

Ha nincs se aktuális, se parkoló tétel: csak ennyi — `Nincs aktuális/parkoló téma.`,
és nincs kérdés.

## 2. Lista

A sessionbe, ebben a formában. A tétel végén lévő dátum (`· <YYYY-MM-DD>`) nem jelenik meg
se a listában, se az opciókban — csak a régi tételek jelzésére való (→ 3. Kérdés).

Ha van aktuális:

```markdown
- **Aktuális:** <ami most folyamatban van>
- **Parkolóban:**
   - <ID> · <parkolt tétel> — *Fejlesztő* | *AI*
```

Ha nincs aktuális:

```markdown
**Parkolóban:**

- <ID> · <parkolt tétel> — *Fejlesztő* | *AI*
```

## 3. Kérdés

Utána `AskUserQuestion`, header: `Folytatás`, kérdés: „Hogy folytassuk?”. A lista
tételei az opciók is: minden tétel egy opció, a `label` pontosan a tétel sora, ebben a
formában.

Ha van aktuális:

```text
Aktuális: <ami most folyamatban van>
<ID> · <parkolt tétel> — Fejlesztő | AI
<ID> · <parkolt tétel> — Fejlesztő | AI
```

Ha nincs aktuális:

```text
<ID> · <parkolt tétel> — Fejlesztő | AI
<ID> · <parkolt tétel> — Fejlesztő | AI
```

- **Sorrend**: a lista sorrendje; a `label` nem kap jelölést.
- **`description`**: egy rövid mondat, mi történik, ha ezt választja; a javasoltnál
  `Javasolt — ` kezdettel. 3 napnál régebben parkoló tételnél: `<N> napja parkol —
  issue-vá léptethető: /issue <ID>`.
- **Push**: ha a Kontextus szerint van pusholatlan commit (`[ahead N]`), `Push` az utolsó
  opció — parkoló tétel nem lesz belőle.
- **4 opció a határ**: ami nem fér bele (az Aktuális és a Push mellett), második
  kérdésbe kerül ugyanígy (header: `Folytatás 2`).

Ha a folytatás egy parkoló tétel: `/pick <ID>`.
