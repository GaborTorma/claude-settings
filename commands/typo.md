---
name: typo
description: Elírás-ellenőrzés a commitolatlan változásokon — a teljesen egyértelmű elírást javítja, a kétest jelzi. Használd amikor a Fejlesztő /typo-t ír, vagy a /commit hívja.
argument-hint: "fájl(ok) (opcionális)"
allowed-tools: Bash(git rev-parse *), Bash(git diff *), Bash(git ls-files *), Read, Edit
---

## Kontextus

- Argumentum: $ARGUMENTS
- HEAD: !`git rev-parse -q --verify HEAD >/dev/null && echo "van" || echo "NINCS"`
- Új fájlok: !`git ls-files --others --exclude-standard`

## 1. Mit

- **Argumentum**: ha fájlokat nevez meg, csak azokat.
- Különben a commitolatlan változások:
  - módosított fájlok: `git diff HEAD` hozzáadott (`+`) sorai; **HEAD** `NINCS` (üres repó) →
    minden fájl új;
  - új fájlok: a Kontextus **Új fájlok** sora, a teljes tartalmuk.
- Nincs mit nézni → csak ennyi: `Typo: nincs változás.`

## 2. Ellenőrzés

Szöveg, komment, dokumentáció, azonosító, string — a nyelvtől függetlenül (magyar
ékezetek is).

- **Egyértelmű elírás** → javítsd a fájlban.
- **Kétes** (szándékos írásmód, szakszó, név, idegen szó, azonosító, amire máshol is
  hivatkoznak) → ne módosítsd, csak jelezd.

## 3. Válasz

```markdown
Typo: <fájl:sor> · <régi> → <új>
Typo?: <fájl:sor> · <szó>
```

- Soronként egy találat; javított (`Typo:`) elöl, kétes (`Typo?:`) utána.
- **Nincs találat**: csak ennyi — `Typo ✓`.
- **Másik commandból hívva**: a hívó a saját válaszába teszi a sorokat, külön nem írod ki.
  A `/typo` sosem bukik — a hívó nem áll meg miatta.
