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
- **AC** = hogyan ellenőrizzük, hogy a rendszer ezt teszi (megfigyelhető feltétel konkrét forgatókönyvben). Given … When … Then …" formára tagolható megfigyelhető kimenettel: log-bejegyzés, DB-állapot, event, fájl, exit-kód, HTTP response, UI-állapot, stb...

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

- **AC-01** — <Mérhető kritérium #1 — pl. "X teszt zöld">. (Ref: FR-01)
- **AC-02** — <Mérhető kritérium #2 — pl. "manual smoke: lépés A → B → C működik">. (Ref: FR-02)
- **AC-03** — <Mérhető kritérium #3.>
```
