---
description: Intent-Driven Planning Phase 3 — Plan (tervezett változtatások + implementációs lépések) + teljes Spec-fájl mentése. Csak ennek az approve-ja jelenti a teljes terv jóváhagyását.
---

# Intent-Driven Planning — Plan (Phase 3)

Ez a command az elfogadott `Intent` + `Spec` alapján megírja a `Plan` szakaszt — atomic TODO lépések mérhető verifikációval (failing test → implementáció → passing test → commit), edge case-ek a `Failing test` mezőben. Approve után **menti a teljes Spec-fájlt** (`Intent` + `Spec` + `Plan` + üres `Megvalósítási napló` placeholder); ezután az `Intent`/`Spec`/`Plan` szakaszok fagyottak.

## Előfeltétel

A beszélgetésben legyen véglegesített `Intent` + `Spec`. Új sessionben olvasd a **Spec-fájl**t a lemezről, ha létezik. Ha bármelyik hiányzik, **kérdezz vissza** vagy küldd vissza a usert az előző fázishoz.

## Workflow

1. **Bontás-döntés (flat vs. multi-stage)**: vizsgáld meg, hogy a Spec AC-i és a tervezett változtatások több, **e2e-tesztelhető és release-worthy egységre** bonthatók-e és szükséges/logikus-e a bontás vagy csak elaprózza a megvalósítást.
   - **Ha milestone-bontás mellett döntenél**: a részletes `Plan` megírása **előtt** mutasd be a usernek:
      - a döntés **indoklását**: miért nem fér be flat alakba, milyen e2e-tesztelhető egységekre bontható szét
      - a javasolt `MS-XX` milestone-okat (cím + 1 mondatos hatókör, kapcsolódó `AC-XX`-ek).

      Kérj megerősítést `AskUserQuestion`-nel. A user pivot-olhat flat-re, módosíthatja vagy átszámozhatja a milestone-okat, vagy jóváhagyhatja. A részletes `IS` / `MV` lépések csak ezután készülnek.

   - **Ha flat alak (alapeset)**: folytasd közvetlenül a 2. lépéssel, külön user-checkpoint nélkül.

2. **`Plan` tervezete** az elfogadott bontás-döntés szerint, az `Intent` + `Spec` alapján → iteratív finomítás (lépések pontosítása, edge case-ek, verifikáció erősítése). A `Branch` sorba **konkrét név** kerüljön, ne placeholder.

3. **`ExitPlanMode` hívás**: a teljes **Spec-fájl** tartalma (mindhárom szakasszal) megy review-ra. Visszajelzés → iteráció → újra `ExitPlanMode`.

4. **Approve után — mentés**: kilépés a Plan harness-ből, és a véglegesített tartalom mentése a megegyezett **Spec-fájl** útvonalra.

5. **Session-javaslat**: tegyél indoklással ellátott ajánlást, hogy a megvalósítás **új sessionben** induljon (tisztább kontextus, kevesebb plan-mód-zaj — nagyobb feladatnál ajánlott) vagy **az aktuálisban folytatódjon** (kicsi, gyors feladat; a kontextus még friss). A döntés a useré.

6. **STOP**: implementáció csak a user explicit jóváhagyása után, az `intent-driven-planning:apply` commanddal indul.

---

## Mező-szemantika

A sablon mezőit ezekkel a szabályokkal töltsd ki.

### `IS-XX`

- **Egy IS = funkcionális egység mérhető eredménnyel**, nem fájlonkénti mechanikus edit. Önmagában megfigyelhető viselkedésváltozás kell legyen (új capability, működő flow, megjavított bug).
- **Tilos önálló IS-ként** tisztán előkészítő edit (1 sor beszúrás, új mező / konstans / helper hozzáadása) amelynek önmagában nincs hatása és nem tesztelhető. Az ilyen prep work része kell legyen annak az IS-nek, ami először felhasználja — a funkcionalitás **egyben** szülessen meg.
- **Jó IS**: egy funkció bevezetése akár több fájlt érintve, ahol a `Failing test`/`Verify` mérhetővé teszi a hatást.

### `Művelet`

- **Cél**: 1 mondat, mit csinál a lépés érthetően — érintett fájl/réteg + viselkedési hatás.
- **Tilos**: konkrét kódrészlet, hívási lánc, "~N sor", "kis komponens", komplexitás-becslés.
- **Jó példa**: "Az olvasási útvonal kiegészül egy új mezővel, így a kliens reaktívan értesül a változásáról."
- **Rossz példa**: "`<konkrét-fájl>`-ban a select-be új mező (~1 sor)."

### `Implementáció`

- **Cél**: technikai megvalósítás — pontos symbol-ok / mezők / hook-ok / helper-ek / event-ek, logika. Mélyebb mint a `Művelet`, nem ismétlés.
- **Forma**: egy összefoglaló mondat, alatta **opcionálisan** nested sub-bullet-ek, ha a megvalósítás több részletre bomlik (pl. külön symbol-ok, sorrendi lépések). Egy-pontos esetnél hagyd ki a sub-bullet-eket.
- **Tilos**: sorszám-becslés ("~15 sor", "1-2 sor"), nehézségi minősítés ("triviális", "egyszerű") — nem ellenőrizhető állítások.

### `Failing test`

- **Cél**: a _jelenlegi hiány_ reprodukciója, ami ezen a lépésen önállóan megfigyelhető — teszt, assert, debug-snapshot, manuális próba.
- **Ha nem észlelhető lokálisan, de a lépésnek cross-cutting hatása van** (pl. channel join, feature flag bekapcsolás): tedd az ellenőrzést `MV-XX`/`GV-XX` alá és hivatkozd az be ide.
- **Tilos**: cross-cutting e2e-szcenárió itt — az `MV` dolga.

### `Verify`

- **Cél**: a lépésen önállóan (más `IS` nélkül) futtatható ellenőrzés, ami zöldre váltja a `Failing test`-et — parancs, log-assert, devtools-snapshot, MCP-query.
- **Ha nem önálló**: hivatkozz az `MV-XX`/`GV-XX`-re.
- **Tilos**: cross-cutting e2e itt, homályos "működik".

### `MS-XX:MV-XX` (Milestone verify) és `GV-XX` (Global verify)

- **Minden bejegyzés konkrét, futtatható vagy reprodukálható** — Spec `AC-XX`-re, nevesített flow-ra, vagy konkrét parancsra hivatkozva.
- **Tilos**:
   - "Minden `IS-XX` / `MS-XX:IS-YY` Verify-ja zöld" — a checkbox-ok jelzik.
   - "Lint zöld, build hibamentes" minden milestone-nál — ha kell, egyszer a `GV`-ben.
   - "Régi funkciók regressziómentesek" — nevesítsd a flow-t és a megfigyelhető állapotot.
- **Jó `MS-XX:MV-XX` / `GV-XX` bejegyzés alak**: "<kiváltó állapot> → <megfigyelhető eredmény> <konkrét időkereten belül> (<eszköz> + <ellenőrzési mód>) [[AC-XX](#AC-XX)]"

---

## Sablon

A `Plan` szakasz + `Megvalósítási napló` placeholder, amit a véglegesített `Intent` + `Spec` mögé fűzünk:

```markdown
## Plan

### Előfeltételek

- **Branch**: `<branch-name>` — `git checkout -b <branch-name>`
- <Mire van szükség a kezdés előtt (pl.: dep, env var, migration, feature flag, tesztkörnyezet, fixtures, mcp, stb...)?>

### Tervezett változtatások <Üres egység törölhető>

<!-- A változás hatóköre — **mit** érint a változás. Kategóriák: módosítás (`CM`), hozzáadás (`CA`), törlés (`CD`). Leírás röviden, tömören. Line ref, ha lehetséges. --->

#### Módosítás

- <a id="CM-01">**CM-01**</a> — <Meglévő rész / fájl / pipeline> — <mit módosítunk benne>
- <a id="CM-02">**CM-02**</a> — <...>

#### Hozzáadás

- <a id="CA-01">**CA-01**</a> — <Új rész / fájl / pipeline> — <mit adunk hozzá>

#### Törlés

- <a id="CD-01">**CD-01**</a> — <Törlendő rész / fájl / pipeline> — <mit távolítunk el>

### Implementációs lépések

<!--
  Két alak közül VÁLASSZ EGYET, a másik blokkot töröld:
  • Flat (alapeset) — kis feladat, egyetlen e2e-tesztelhető egység.
  • Multi-stage (opcionális) — több e2e-tesztelhető, release-worthy increment;
    MS-XX milestone-csoportok, lokális `MS-XX:IS-YY` lépésszámozás, milestone-onkénti MV-XX verify.
-->

<!-- Lépés-mezők szabályait lásd: `Mező-szemantika`. -->

<!-- OPCIÓ A — Flat alak -->

- [ ] <a id="IS-01">**IS-01**</a> — _<Lépés rövid címe>_ [[AC-XX](#AC-XX)]
   - **Művelet**: <…>
   - **Implementáció**: <…>
      - <…>
      - <…>
   - **Failing test**: <…> _vagy_ `—`
   - **Verify**: <…> _vagy_ `—`
   - **Commit**: `<type>(<scope>): <subject> [IS-XX]` — ha `IL-XX` is keletkezik ugyanabban a commitban, pl. `[IS-04, IL-02]`

<!-- Továbbiak (- [ ] IS-02, - [ ] IS-03, ...) ugyanezzel a struktúrával. -->

<!-- OPCIÓ B — Multi-stage alak (mező-struktúra azonos a flat IS-szel; csak az ID-prefix és Commit-token tér el) -->

#### <a id="MS-01">MS-01</a> — <Milestone rövid címe, ami egy e2e-tesztelhető release-worthy egységet ír le>

- [ ] <a id="MS-01:IS-01">**MS-01:IS-01**</a> — _<Lépés rövid címe>_ [[AC-XX](#AC-XX)]
   - **Művelet**: <…>
   - **Implementáció**: <…>
      - <…>
      - <…>
   - **Failing test**: <…> _vagy_ `—`
   - **Verify**: <…> _vagy_ `—`
   - **Commit**: `<type>(<scope>): <subject> [MS-XX:IS-YY]` — ha `IL-XX` is keletkezik ugyanabban a commitban, pl. `[MS-02:IS-04, IL-02]`

<!-- Továbbiak (- [ ] MS-01:IS-02, - [ ] MS-01:IS-03, ...) ugyanezzel a struktúrával. -->

**Milestone verify**

- [ ] <a id="MS-01:MV-01">**MS-01:MV-01**</a> — <konkrét ellenőrzési mód (parancs / Playwright snapshot / MCP query / DB-állapot).> [[AC-XX](#AC-XX)]

<!-- Továbbiak: - [ ] **MS-01:MV-02**, - [ ] **MS-01:MV-03**, ... -->

<!-- További milestone-ok (#### MS-02, #### MS-03, ...) ugyanezzel a struktúrával, lokális IS-számozással és saját MV blokkal. -->

### Globális verifikáció (a teljes Plan végén)

- [ ] <a id="GV-01">**GV-01**</a> — <konkrét ellenőrzési mód a teljes Plan szintjén (AC-coverage, golden path e2e, build parancs stb.).> [[AC-XX](#AC-XX)]

<!-- Továbbiak: - [ ] **GV-02**, - [ ] **GV-03**, ... -->

### Kockázat

- <Legkockázatosabb lépés és mitigáció (csak ha van!)>

## Megvalósítási napló

<!-- Az implementáció során bővül. Csak a Plan és a megvalósult kód közötti **deltákat** rögzíti (eltérés, fix, follow-up, refactor) — a Plan szerint lefutott `IS-XX` / `MS-XX:IS-YY` lépéseket nem ismétli. -->

- <a id="IL-01">**IL-01**</a> — _<Bejegyzés rövid címe>_ [[IS-XX](#IS-XX), [MS-XX:IS-YY](#MS-XX:IS-YY), [AC-XX](#AC-XX), [FR-XX](#FR-XX)]
   - **Típus**: Eltérés | Fix | Follow-up | Refactor
   - **Indoklás**: <1-2 mondat a motivációról / triggerről: mi váltotta ki a deltát — mi derült ki, milyen bugot fedeztünk fel, miért nem volt megfelelő a Plan-megközelítés.>
   - **Delta**: <1-2 mondat — a delta konkrét tartalma: hogyan tértünk el / mit fixáltunk / mit vettünk fel follow-up-ként. **Ne ismételd a Plan-tételt** — csak a deltát írd le.>
   - **Nyitott** (opcionális): <amit nem sikerült megcsinálni, későbbre halasztottuk — pl. follow-up ticket, tech-debt jegyzet. Csak akkor írd ki, ha van ilyen.>
   - **Commit** (ha külön commit-ot kap): `<type>(<scope>): <subject> [IL-XX]`

<!-- További bejegyzések (- IL-02, - IL-03, ...) ugyanezzel a struktúrával. Ha olyan dolog történik, ami egy korábbi `IL-XX` bejegyzést érint (pl. egy korábbi `Nyitott` tétel teljesül), a meglévő bejegyzést kell frissíteni — ne nyiss újat. -->
```
