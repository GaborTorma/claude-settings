---
description: Intent-Driven Planning Phase 2 — Spec (viselkedési követelmények és elfogadási kritériumok). Iteratív review.
---

# Intent-Driven Planning — Spec (Phase 2)

Ez a command az elfogadott `Intent`-re építve előállítja a viselkedési kontraktust — input → output, observable behavior, funkcionális + nem-funkcionális követelmények, mérhető elfogadási kritériumok. **Nem implementáció.** Iteratív review a Plan harness-en keresztül.

## Előfeltétel

A beszélgetésben legyen véglegesített `Intent`. Ha hiányzik, **kérdezz vissza** vagy küldd vissza a usert az előző fázisra.

## Workflow

1. **Re-invokálás detektálása — downstream draft eldobása**: ha a beszélgetésben már van élő `Plan` draft korábbi `intent-driven-planning:plan` futtatásból, **kérdezz rá `AskUserQuestion`-nel** az eldobására.
   - **Ha a user megerősíti**: a `Plan` draftot tekintsd érvénytelennek, és csak az új `Spec`-kel haladj tovább.
   - **Ha elutasítja**: állj le, és egyeztess a userrel a folytásról.

2. **`Spec` tervezete** az elfogadott `Intent` alapján: Funkcionális követelmények (kötelező) + Nem-funkcionális követelmények (opcionális) + Elfogadási kritériumok (kötelező).

3. **`ExitPlanMode` hívás** review-hoz: a tervezet `Intent` + `Spec` tartalommal megy.
   Nyitott kérdés ne maradjon — a review előtt rendezd (`AskUserQuestion`). Ha a válasz az `Intent`-et is érinti, jelezd a usernek, hogy vissza kell propagálni.
   Visszajelzés → iteráció → újra `ExitPlanMode`.

4. **STOP — itt véget ér.** Várj a user következő parancsára (`intent-driven-planning:plan`).

## Szabályok

### FR vs. AC megkülönböztetés

- **FR** = mit kell tennie a rendszernek (deklaratív viselkedés).
- **AC** = hogyan ellenőrizzük, hogy a rendszer ezt teszi — megfigyelhető feltétel konkrét forgatókönyvben, megfigyelhető kimenettel: log-bejegyzés, DB-állapot, event, fájl, exit-kód, HTTP response, UI-állapot, stb.

**Tilos** AC-t úgy írni, hogy 1:1 átfogalmazza az FR-t ("X történjen meg").

**Lefedettség**:

- Egy AC lefedhet több FR-t (end-to-end szekvencia).
- Egy FR-hez tartozhat több AC.
- 1:1 FR↔AC megfeleltetés **nem cél**, sőt anti-pattern.

**Minimális AC-kategóriák**, amiket végig kell gondolni minden Spec-nél (ha nem releváns, explicit kihagyható):

- happy path
- negatív eset / hibakezelés
- edge case / boundary (üres, max, race, timeout)
- megfigyelhetőség (mit látunk a rendszer kívülről — log, metric, állapot)

### AC szerkezete (3 sor, sorszám prefixxel)

Minden AC fejléce egy _dőlt_ egymondatos forgatókönyv-címke + `[FR-XX]` a kapcsolódó FR/NF-ekre, alatta **három sorszámozott al-pont** fix sorrendben — prefix (Given/When/Then) nem kell, a mondatok alakja hordozza a szerepet:

1. **Kiinduló állapot** — főnévi szerkezet, jelen idő: mi áll fenn a rendszerben. _("Egy `<állapot>` állapotú entitás `<feltétellel>`.")_
2. **Kiváltó esemény** — akció-ige, jelen idő: mi történik. _("Esemény érkezik / timer lejár / külső hívás történik.")_
3. **Megfigyelhető eredmény** — eredmény-ige, jelen idő: mit látunk kívülről. _("Új rekord / log-bejegyzés / API-válasz / állapot-mező megjelenik.")_

A három sor sorrendje **kötött**. Ha egy AC-hez 4+ sor kell, valószínűleg két különálló forgatókönyv keveredik — bontsd szét.

---

## Sablon

A `Spec` szakasz, amit az `Intent` mögé fűzünk:

```markdown
## Spec

### Funkcionális követelmények

- **FR-01** — <Megfigyelhető viselkedés #1 — input → output, fájl-független megfogalmazásban.>
- **FR-02** — <Megfigyelhető viselkedés #2.>

### Nem-funkcionális követelmények

- **NF-01** — <Performance: pl. p95 < 200ms, max memória, throughput.>
- **NF-02** — <Biztonság / adatvédelem: auth, secret-kezelés, PII.>
- **NF-03** — <Kompatibilitás: verziók, böngészők, runtime, OS.>
- **NF-04** — <Egyéb: a11y, i18n, observability, ha releváns.>

### Elfogadási kritériumok

- **AC-01** — _<Forgatókönyv egymondatos címkéje.>_ [FR-01, NF-02]
   1. <Mi áll fenn — előfeltétel főnévi szerkezettel.>
   2. <Mi történik — kiváltó esemény akció-igével.>
   3. <Mit látunk — megfigyelhető eredmény (log / DB / API / UI / állapot, stb...).>

- **AC-02** — _<Másik forgatókönyv címkéje.>_ [FR-03]
   1. <Mi áll fenn.>
   2. <Mi történik.>
   3. <Mit látunk.>
```
