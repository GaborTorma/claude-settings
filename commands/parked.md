---
name: parked
description: Az aktuális munka és a parkoló témák kiírása, majd kérdés a folytatásról. Használd lezáráskor (→ focus.md), amikor a Fejlesztő /parked-ot ír, vagy azt kérdezi, mi van nyitva, mi parkol.
allowed-tools: Bash(git status *)
---

## Kontextus

- Git: !`git status -sb`

## 1. Összegyűjtés

- **Aktuális**: ha van még teendő az aktuális témával — a folyamatban lévő munka
  ebben a sessionben, és a félbemaradt munka a Kontextusból (commitolatlan
  változás). Commitolt, de pusholatlan munka nem aktuális.
- **Parkolóban**: a session parkolólistája (→ `focus.md` 3. Parkolás), a
  *Fejlesztő* / *AI* jelöléssel.

Ha nincs se aktuális, se parkoló tétel: csak ennyi — `Nincs nyitott vagy parkoló téma.`,
és nincs kérdés.

## 2. Kérdés

`AskUserQuestion`, header: `Folytatás`, kérdés: „Hogy folytassuk?”. A lista maga az
opciók: minden tétel egy opció, a `label` pontosan a tétel sora, ebben a formában; a
sessionbe külön nem írod ki — a Desktop app a tool-hívások közti többsoros szöveget
összefoglalja, az opciókat nem.

Ha van aktuális:

```text
1. Aktuális: <ami most folyamatban van>
2.a) <parkolt tétel> — Fejlesztő | AI
2.b) <parkolt tétel> — Fejlesztő | AI
```

Ha nincs aktuális:

```text
a) <parkolt tétel> — Fejlesztő | AI
b) <parkolt tétel> — Fejlesztő | AI
```

- **Sorrend**: a lista sorrendje; a `label` nem kap jelölést.
- **`description`**: egy rövid mondat, mi történik, ha ezt választja; a javasoltnál
  `Javasolt — ` kezdettel.
- **Push**: ha a Kontextus szerint van pusholatlan commit (`[ahead N]`), `Push` az utolsó
  opció — parkoló tétel nem lesz belőle.
- **4 opció a határ**: ami nem fér bele, második kérdésbe kerül ugyanígy (header:
  `Folytatás 2`).

Ugyanabban a hívásban egy további kérdés, ha van parkoló tétel: „Mit vessünk el?”,
header: `Elvetés`, `multiSelect: true`. Az opciók a parkoló tételek, a `label` ugyanúgy
pontosan a tétel sora (az Aktuális és a Push nem). A kiválasztott tételek kikerülnek a
parkolólistából; ha semmit nem jelöl, minden marad.
