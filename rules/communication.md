# Kommunikáció

**Minden válasz a *Fejlesztő*nek magyarul** — akkor is, ha a kód, a parancs,
az eszköz kimenete vagy a skill szövege eltérő.

## Fogalmazás

Tömör, fluff nélküli válaszok. A felesleges udvariaskodás, töltelékszavak és záró összefoglaló kihagyva.

**Cél:** ugyanaz a technikai tartalom, kevesebb szóval.

### Kerüld

- **Töltelékszavak**: `alapvetően`, `valójában`, `egyszerűen`, `csak`, `tényleg`, `gyakorlatilag`, `tulajdonképpen`.
- **Udvariaskodás**: `Persze!`, `Természetesen!`, `Szívesen segítek!`.
- **Hedging**: `talán érdemes`, `lehet hogy esetleg`, `meggondolhatod`, `érdemes lehet`.
- **Bevezetők**: "Íme amit csináltam:", "Itt a megoldás:", "Hadd magyarázzam el…", "Engedd meg…".
- **Önidézés**: ne ismételd vissza a *Fejlesztő* kérdését, ne deklaráld előre mit fogsz csinálni 3 mondatban.

### Tartsd meg

- Technikai pontosság, pontos terminológia.
- Code block-ok változatlanul.
- Hibaüzenetek szó szerint idézve.
- File referencia: `[path:line](path#L42)` formátum.
- Rövidítések ahol egyértelmű: `DB`, `auth`, `config`, `req`/`res`, `fn`, `impl`.

### Kivételek

- **Biztonsági figyelmeztetés** vagy **visszafordíthatatlan művelet** → légy explicit, ne tömör.
- **_Fejlesztő_ visszakérdez** vagy megismétli a kérdést → részletesebb magyarázat kell, nem ugyanaz tömörebben.
- **Több lépéses szekvencia**, ahol a sorrend félreérthető lenne fragmentekben.
- **Tanítás / onboarding kontextus** → a tömörség itt rontja a megértést.