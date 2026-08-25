---
allowed-tools: Bash(gg:*), Bash(git:*), Artifact
description: Az aktuális repó commit-gráfját Git Graph stílusú Artifact oldalként publikálja — meglévőt frissít, nem hoz létre duplikátumot.
argument-hint: "[commit-limit, alap: a teljes history]"
---

## Kontextus (előre lefuttatva)

- **Friss gráf generálva** (a `gg` írja a repón belüli stabil helyre):
  !`gg`

- **Repó neve** (ebből jön az Artifact címe):
  !`basename "$(git rev-parse --show-toplevel)"`

- **Ág és push-állapot**:
  !`git status -sb | head -1`

## Feladat

Publikáld a fenti HTML fájlt Artifactként, **a meglévőt frissítve**.

### 1. Ha a Fejlesztő adott commit-limitet

Ha a `$ARGUMENTS` egy szám, generáld újra ezzel: `gg --limit <szám>`. Ha üres,
a fenti (teljes history) kimenet marad — ne futtasd újra feleslegesen.

### 2. Keresd meg a meglévő Artifactot

A cím **mindig** `<repónév> Git Graph` (pontosan ezt írja a `gg` a `<title>`-be).
Hívd az Artifact eszközt `action: "list"`-tel, és keress erre a címre.

- **Van találat** → publikálj a talált **URL-lel** (`url` paraméter) ÉS a `gg`
  kiírta fájlútvonallal. Így ugyanaz az oldal frissül, a link nem változik.
- **Nincs találat** → publikálj `url` nélkül, ez létrehozza az elsőt.

Mindkét esetben:
- `file_path`: amit a `gg` kiírt (a `✓` utáni abszolút út)
- `favicon`: `🔀` — **soha ne változtasd**, ez azonosítja a lapot a galériában
- `description`: egy mondat, mi ez a repó és mekkora a history

> A `label` paraméterbe tedd a commitszámot (pl. `122 commit`) — a verzió-
> választóban ez különbözteti meg a korábbi publikálásoktól.

### 3. Jelentsd vissza

Egy rövid mondat + a link. Mondd meg, **frissítés** volt-e vagy új oldal, és
hány commit került rá. Ha a repóban pusholatlan commit van (a `git status -sb`
`ahead` értéke), azt is említsd egy tagmondatban — a gráfon látszik, a
távolin még nincs ott.

Ne írj hosszú összegzést a gráf tartalmáról: az oldal magáért beszél.
