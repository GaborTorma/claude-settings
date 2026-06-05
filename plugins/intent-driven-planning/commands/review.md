---
description: Intent-Driven Planning review — a tervezés közbeni koherencia-ellenőrzés a beszélgetésben lévő `Intent`/`Spec`/`Plan` drafton. Adaptív (csak amit eddig megfogalmaztunk), report-only, nem mutál semmit.
---

# Intent-Driven Planning — Review

Ez a command a **tervezés közbeni** **Spec-fájl**-draftot ellenőrzi: anomáliákat, inkonzisztenciákat, lefedési réseket keres a `Intent` / `Spec` / `Plan` szakaszok között. **Pure dokumentum-ellenőrzés, kód nem érinti** — a `review` futáskor a kód még nem létezik, mert legkésőbb a `Plan` szakasz finomításakor fut.

## Soft-enforcement

Ha a beszélgetésben **nincs aktív Spec-draft** (sem előző `intent`/`spec`/`plan` futtatás eredménye, sem ExitPlanMode-prezentáció), válaszolj röviden és állj le:

> A `review` a tervezés közbeni Spec-draftot ellenőrzi — most nincs ilyen a beszélgetésben. Indíts előbb egy `intent`/`spec`/`plan` commandot, és onnan futtasd újra.

Ha viszont van draft, folytasd a check-kel.

## Mit elemez (adaptív)

A draft állapotához igazodva, kumulatívan: minden szekció hozzáadja a saját check-jeit az előzőhöz.

### Közös (minden fázis)

- **Hivatkozás-konvenció** (lásd `methodology.Hivatkozások`): a kódbeli hivatkozások relatív linkek (a Spec-fájl helyéhez képest)? Létező symbol-ra hivatkozó link tartalmaz `#LNN` sor-anchor-t a target-ben, de a szövegben **nincs** sor-szám? Nem-létező (tervezett) symbol-ra nincs link, csak inline backtick?

### Csak `Intent`

- A draft kötelező szakaszai megvannak? `Készítve` dátum kitöltve?
- Title-line, `> **Spec-fájl**: ...` path és `Probléma` szakasz konkrét tartalmú (nem `<...>` placeholder)?
- Az `Intent`-en belül van-e logikai ütközés `Célok` (`GL-NN`) és `NEM-célok` (`NG-NN`) között?
- `Későbbi megvalósítás` (`LI-NN`, opcionális): ha jelen, nem ütközik `Célok` / `NEM-célok`-kal?
- Az `Intent.Nyitott kérdések` szakaszában maradt megválaszolatlan tétel?
- Bármelyik szakaszban van `TODO` / `TBD` / `?` marker?
- `Intent.Kapcsolódó Spec-fájlok` (opcionális): ha jelen, minden bejegyzés `[path](path) — <1 mondat indoklás>` formátum?
- Ugyanaz a komponens-név / fogalom mindenütt?
- Van-e olyan rész, ami **rövidebb, lényegre törőbb** megfogalmazással kifejezhető az értelem elvesztése nélkül?
- Tartalmi **duplikáció**? Felesleges töltelékszó, redundáns minősítő ("nyilvánvalóan fontos", "általában szükséges"), feleslegesen ismételt magyarázat?

### `+ Spec`

- Az `Intent.Célok` (`GL-NN`) minden eleméhez tartozik legalább egy követelmény a `Spec`-ben?
- Van-e `Spec`-követelmény, ami egyik célhoz sem köthető?
- A `Spec` ír-e olyat, amit az `Intent.NEM-célok` explicit kizár?
- A `Spec.Nyitott kérdések` szakaszában maradt megválaszolatlan tétel?
- Minden `FR-NN` megfigyelhető viselkedés (input → output formában)? `AC-NN` mind mérhető?
- Minden `AC-NN` `(Ref: FR-XX)` formában hivatkozik legalább egy `FR-NN`-re?
- NFR-ben említett metrika konkretizálva van-e az elfogadási kritériumokban?

### `+ Plan`

- A `Branch` sor konkrét név (nem placeholder)?
- `Előfeltételek` további tételei (dep, env var, migration, feature flag, fixtures, mcp) konkrétak, nem placeholderek?
- Minden `Spec.Elfogadási kritérium` köthető legalább egy `Plan`-lépés `Verify`-jéhez vagy a hozzá tartozó `MV-XX` / `GV-XX`-hez?
- Van-e `Plan`-lépés, ami egyetlen Spec-követelményt sem szolgál?
- A `Plan` ír-e olyat, amit az `Intent.NEM-célok` explicit kizár?
- `Implementációs lépések`: pontosan **egy** alak (Flat `IS-XX` **vagy** Multi-stage `MS-XX` / `MS-XX:IS-YY`) van használatban, a másik blokk törölve?
- Minden `#### IS-NN` / `#### MS-NN` / `##### MS-XX:IS-YY` heading-en megvan a `[ ]` (vagy `[x]`) checkbox?
- Minden `IS-NN` (vagy `MS-XX:IS-YY`) lépésnél kitöltve `Művelet` / `Implementáció` / `Commit`? `Failing test` és `Verify` kitöltve **vagy** `—` explicit `MV-XX` / `GV-XX` cross-reference-szel?
- Multi-stage alak: minden `MS-XX` milestone-hoz tartozik legalább egy `MV-XX` blokk és egy `Milestone summary` blokk (plan-időben placeholder skeleton, `Commit` mezővel)? Flat alak: van `Globális summary` blokk?
- `Tervezett változtatások` (`CM-NN` / `CA-NN` / `CD-NN`) bulletjei `<hely> — <mit>` formátumban, tömören?
- Minden Plan-mező megfelel a [Mező-szemantika](./plan.md#mező-szemantika) szabályainak (tilalmas frázisok, kötelező cross-reference-ek, `Commit` `[IS-XX]` / `[MS-XX:IS-YY]` ref)?

## Output formátum

Three-tier severity:

```
   1. 🚨 Mit, hol, miért anomália — Javasolt megoldás
   2. ⚠️ ...
   3. ℹ️ ...
```

**Severity-besorolás**:

- **Critical** 🚨: strukturális hiány, NEM-célok ütközés, megválaszolatlan kérdés Plan-jóváhagyás előtt, üres kötelező placeholder, nem konkrét/futtatható `MV-XX` / `GV-XX`
- **Warning** ⚠️: Spec ↔ Plan lefedés-rés, terminológiai eltérés, hiányos Plan-lépés mező, [Mező szemantika](./plan.md#mező-szemantika) megsértése
- **Info** ℹ️: redundancia, fogalmazási finomítás, opcionális mező nincs kitöltve

## Workflow

1. **Olvas**: az utolsó `ExitPlanMode`-ban prezentált draft, vagy a beszélgetésben legfrissebb Intent/Spec/Plan-tervezet. Ha nincs ilyen → soft-enforcement leállás.

2. **Elemez**: az aktuális draft-állapotnak megfelelő aktív kategóriák **mind**, egyben (nem áll meg az első critical-nél).

3. **Riportál**: chatben a fenti formátumban. **Ennyi.**

## Mit NEM csinál

- **Nem nyúl semmihez** — nem írja át a draftot, nem ír fájlt, nem hív `ExitPlanMode`-ot
- **Nem fut tesztet, nem olvas kódot, nem nézi a git-et** — a draft önmagával vett konzisztenciáját elemzi
- **Nem blokkol semmit** — a user dönti el, mit kezd a találatokkal (manuálisan finomít a `intent`/`spec`/`plan` újrafuttatásával)
