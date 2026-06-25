---
description: Intent-Driven Planning Phase 1 — Intent (probléma, cél, NEM-célok). Iteratív review.
---

# Intent-Driven Planning — Intent (Phase 1)

Ez a command előállítja az `Intent` szakaszt — cél-formálás: motiváció + cél + sikerkritérium + NEM-célok. **Nem viselkedés-leírás, nem implementáció, nem fájl-/rész-lista.** Iteratív review a Plan harness-en keresztül.

## Mit NE tegyél az Intent-be

Iteráció során a próza tendenciózusan hízik, és részletek szivárognak be a következő fázisokból. Az alábbiak **Spec / Plan-anyag**, akármilyen relevánsnak tűnnek:

- **Érintett részek / fájlok listája, érintési mintázatok** → **Plan** (`Tervezett változtatások` szakasz).
- **Per-eset szétosztási / döntési logika** → **Spec** (megfigyelhető szabály) + **Plan** (kód-szintű hely).
- **Schema / adatreprezentáció érvelése** → **Spec** (megfigyelhető szemantika).
- **Mechanizmus-szintű edge-case részletek** → **Spec** (invariáns) + **Plan** (kezelés).
- **"Miért így és nem úgy" magyarázat**, ha az olvasónak az érv nem kell az Intent megértéséhez → **Spec** / **Plan**.
- **Bullet két mondatra nyúlik / "és" tagmondatlánc** → valószínűleg részlet csúszott bele; rövidítsd egy mondatra, és a részletet vidd a következő fázisba vagy bontsd fel 2 pontra.

## Workflow

1. **Re-invokálás detektálása — downstream draft eldobása**: ha a beszélgetésben már van élő `Spec` vagy `Plan` draft korábbi `intent-driven-planning:spec` / `intent-driven-planning:plan` futtatásból, **kérdezz rá `AskUserQuestion`-nel** az eldobásukra.
   - **Ha a Fejlesztő megerősíti**: a Spec/Plan draftokat tekintsd érvénytelennek, és csak az új `Intent`-tel haladj tovább.
   - **Ha elutasítja**: állj le, és egyeztess a Fejlesztővel, a folytatásról.

2. **Orientáció**:
   - **Branch** — current branch (`git branch --show-current`); ha `<prefix>/<slug>` konvenciót követ, a slug a step 4 fájlnév-javaslat alapja.
   - **Korábbi Spec-ek** — ha van `.spec/`, listázd és olvasd a relevánsakat (átfedő terület/réteg/feature-család, vagy átfedő `Célok` / `NEM-célok` / `Későbbi megvalósítás`).
   - **Kódbázis** — célzott kutatás: érintett modul/réteg/függvény azonosítása (SocratiCode `codebase_search` / `ctx_search` / `Glob`), kulcs-fájlok `map` / `signatures` módban.
   - **Konkurencia-elemzés** event-vezérelt vagy aszinkron érintség esetén.

3. **`Intent` tervezete** az első prompt + orientáció alapján: Probléma + Célok + NEM-célok + Későbbi megvalósítás.

4. **Slug + fájlnév egyeztetés**: javasold a slug-ot és — ha indokolt — az opcionális almappát; a Fejlesztő vagy elfogadja, vagy ad másikat.
   A javasolt **Spec-fájl** útvonal rögzítendő a beszélgetésben.

5. **`ExitPlanMode` hívás** review-hoz: a tervezet kizárólag `Intent` tartalommal megy.
   Nyitott kérdés ne maradjon — a review előtt rendezd (`AskUserQuestion`).
   Visszajelzés → iteráció → újra `ExitPlanMode`.

6. **STOP — itt véget ér.** Várj a Fejlesztő következő parancsára (`intent-driven-planning:spec`).

---

## Sablon

A skeleton, amivel az `Intent` szakaszt tölti ki; a fel nem használt opcionális alszakaszokat töröld.

```markdown
# <Spec-fájl címe — röviden a feature / feladat>

> **Spec-fájl**: `.spec/<slug>.md`

_Készítve: <YYYY-MM-DD — az `intent` futtatás napja>_

## Intent

### Kapcsolódó Spec-fájlok

<!-- Opcionális — csak ha az orientációban van releváns korábbi Spec-fájl. -->

- [.spec/<group>/<other-slug>.md](.spec/<group>/<other-slug>.md) — <1 mondat: miért releváns (átfedő réteg / NEM-cél / Későbbi megvalósítás / korábbi döntés).>

### Probléma

<2-4 mondat: mi a jelenlegi helyzet, mi a tünet, hol látható. Konkrét kód-evidence megengedett, ha tömör.>

### Célok

<1-2 mondat magas szintű cél; ha van mérhető siker vagy invariáns, fűzd hozzá sub-bulletekben:>

- <a id="GL-01"></a>**GL-01** — <invariáns / megfigyelhető siker #1>

### NEM-célok

- <a id="NG-01"></a>**NG-01** — <Amit explicit nem csinálunk meg — sosem.>

### Későbbi megvalósítás

- <a id="LI-01"></a>**LI-01** — <Amit később lehet, de most nem csinálunk meg. Nem fejtjük ki bővebben, de egy tervezési döntésnél, ha nem bonyolítja el az aktuális megvalósítást, figyelembe vehető.>
```
