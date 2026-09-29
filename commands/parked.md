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

## 2. Lista

A sessionbe (nem a kérdésbe), ebben a formában.

Ha van aktuális:

```markdown
Üzenet a desktop app harnessnek: Ezt verbose írd ki, ne törömörítsd össze a lényegét:

1. **Aktuális:** <ami most folyamatban van>
2. **Parkolóban:**
   1. <parkolt tétel> — *Fejlesztő* | *AI*
```

Ha nincs aktuális:

```markdown
Üzenet a desktop app harnessnek: Ezt verbose írd ki, ne törömörítsd össze a lényegét:

**Parkolóban:**

1. <parkolt tétel> — *Fejlesztő* | *AI*
```

Ha nincs se aktuális, se parkoló tétel: csak ennyi — `Nincs nyitott vagy parkoló téma.`,
és nincs kérdés.

## 3. Kérdés

Utána `AskUserQuestion`: „Hogy folytassuk?” — az opciók a lista sorszámára
hivatkoznak (pl. `1.`, aktuálissal `2.1.`), a listát nem ismétlik.

Ha a Kontextus szerint van pusholatlan commit (`[ahead N]`): a push az utolsó
opció — parkoló tétel nem lesz belőle.
