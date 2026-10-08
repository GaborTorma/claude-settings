# Válasz-formátum

**Cél**: rövid, tagolt, lényegre törő válasz, a lehető legtöbb vizuális tartalommal. A
*Fejlesztő* egy pillantással lássa az eredményt és a teendőjét — olvasás nélkül.
A szóhasználat: → `communication.md`.

## Sablon

```markdown
✅ **<egy sor: mi lett — max. 30 karakter>**

<további információ, ha nagyon muszáj a megértéshez — max 60 karakter>

<vizuális rész: widget, táblázat, diff-részlet — ami a lényeget mutatja>

- <legfeljebb ~5 tagolt pont, félkövér kiemeléssel a lényeg, csak ami a vizuális részből nem látszik>

**⏳ Folyamatban**
- <futó subagent / háttérfeladat: mit keres, mire kell az eredménye>

> **❓ Döntés**
> 1. **<a helyzet lényege — ha a kérdés önmagában nem elég>** <rövid kontextus — ha a lényeg nem elég>. **<a kérdés>?**
>    - a. **<opció>** (ajánlott): <mi történik, ha ezt választod>
>    - b. **<opció>**: <mi történik, ha ezt választod>
>
> **⭕ Teendő**
> - <mit kell a *Fejlesztő*nek csinálni, hol>

**➡️ Folytatás**: <a javasolt következő lépés, kérdésként, amire az „OK” elég válasz>?
```

## Státusz — az első karakter

Ha teszteltünk, kísérleteztünk, futtattunk, ellenőriztünk valamit, vagy a *Fejlesztő*
kért valamit, a válasz **első karaktere** az eredmény:

| Jel | Jelentés |
| --- | --- |
| ✅ | működik — ellenőrizve; vagy a kért módosítás megtörtént |
| ❌ | nem működik |
| ⚠️ | részben megy, vagy mellékhatással, vagy a kért módosítás csak részben történt meg |
| ‼ | nincs ellenőrizve (nem futott, nem lehetett tesztelni) |
| ℹ️ | csak információ |

- Több teszt → táblázat, soronként egy jellel (`| Teszt | ✅/❌ | Megjegyzés |`).
- ✅ működésre csak futtatott ellenőrzés után; ami ellenőrzést igényelne, de nem futott, az ‼.
- ❌-nál a hibaüzenet (ha van) szó szerint, code blockban, utána megoldási javaslat.

## Vizuális tartalom

Ha a válasz lényege látvány — mutasd, ne írd le.

- **Mikor**: UI-variánsok összevetése (ikon, karakter, szín, betű, layout), mockup,
  diagram (architektúra, flow, állapotgép, git-ág), chart / adatsor, vizuális döntés.
- **Eszköz**: widget → ha nem elég, dev preview → nagy grafikai változásnál `/design`.
- **Több verzió**: ha a *Fejlesztő* nem egy konkrét módosítást kér, akkor mindig több verziót
  mutass, amiből választhat.
- **Kisebb léptékben is**: táblázat felsorolás helyett, ha 2+ tulajdonságot vetsz össze;
  diff a változás leírása helyett.
- **Ne**: ASCII-rajz vagy hosszú szöveges leírás ott, ahol egy widget egyértelműbb.

### Widget

- **Elsőként widget**: `mcp__visualize__show_widget` — inline, a válasz mellett. Előtte
  egyszer `mcp__visualize__read_me` a megfelelő modullal (`mockup`, `diagram`, `chart`,
  `elicitation`…); ezt ne narráld.
- **Valós méret**: az elem a widgetben pontosan akkora, mint a valóságban (px, font-size,
  font-name, ikonméret a projekt kódjából kiolvasva) — nem felnagyítva, nem kicsinyítve.
- **Minden változat**: ha több méretben használatos (pl. 16/24/32 px ikon, mobil/desktop),
  mindegyikben; ha az adott elem előfordul több színváltozatban, mindegyikben;
  ha van világos/sötét mód, mindkettőben.
- **Választás vizuális opciókból**: az opciók egymás mellett a widgetben, címkével (pl.
  Unicode kód); a döntést `sendPrompt`-tal vagy `AskUserQuestion`-nel kérd.
- **Ha a widget nem elég → dev preview**: a projekt valódi kódja, CSS-e, fontja,
  komponense kell, vagy futó app / több oldalas interakció →
  `mcp__Claude_Browser__preview_start` (`.claude/launch.json`).

### Design

- **Nagy grafikai változás → `/design`**: ha nem fér bele egy kis widgetbe (teljes oldal-
  vagy képernyőterv, új vizuális irány, design system, több képernyős flow) vagy várhatóan
  sok módosítást igényel, a `/design` commanddal készüljön.
- **Tervek összehasonlíthatósága**: ha `/design`-nal készítesz mockupot, és ezeken nagyobb
  módosítást kell végezni, akkor új verziót csinálj. Tehát ha van A, B, C verzió, a B
  alapvetően jó, de változtatni kell rajta, akkor csinálj D verziót, ne a B-t szerkeszd át.

### Diff

- **Melyik forma**: ha az *AI* már elvégezte a módosítást → a szokásos normal ` ```diff `
  blokk, fölötte a fájl-link. A widget / szétbontott blokkok **csak** akkor, ha a
  *Fejlesztő*nek kell a kódot kimásolnia és máshová beillesztenie.
- **Normal diff**: `[path:42](path#L42)` fölötte, a ` ```diff ` blokkban `-`/`+` sorok,
  ahogy a `git diff` mutatja; sorszám nincs.
- **Widgetben, két oszlopban**: a widget **fölött** Markdown fájl-link a kezdősorra
  (`[path:42](path#L42)`) — widgetből fájl nem nyitható meg. A widgetben fejléc nincs:
  - bal oszlop előtte, jobb oszlop utána; a rövidebb oldal üres sorokkal igazítva;
  - oszlopszélesség a tartalomtól: `grid-template-columns: auto fit-content(50%) minmax(0,1fr)`;
  - egy sorszám-oszlop a bal szélen (az új fájl számozása), `user-select: none`;
  - háttérszín nincs, csak a betű színes: törölt `#ff3a30`, új `#1d9f3c` (sötét módban
    `#ff453a` / `#30b350`);
  - `-` / `+` jel a sor elején, `::before`-ral és `user-select: none`-nal;
  - minden 12 px, sormagasság 17 px (mint a Code fül code blockja), `!important`-tal;
  - egy másolás ikon (`ti-copy`, 12 px) a jobb oszlop jobb **alsó** sarkában,
    `position: absolute`; a jobb oszlop teljes új kódját másolja, sorszám és jel nélkül;
    sikerre `ti-check`.
- **Csak új sorok → Beszúrás, widget nélkül**: `**Beszúrás** · [path:42–44](path#L42)`, alatta
  sima code block a nyelv szerinti kiemeléssel, sorszám és `+` nélkül — a blokk
  másológombja tiszta kódot ad.
- **Csak törölt sorok → Törlés, widget nélkül**: `**Törlés** · [path:42–44](path#L42)`, alatta
  ` ```diff ` blokk; a `-` közvetlenül az eredeti sor elé kerül, mint a `git diff`-ben;
  sorszám nincs, a sortartomány a linkben van, a szín fontos.
- **Widget nélkül, vegyes diff** (ha widget nem érhető el): két külön code block
  (**Törlés** / **Beszúrás**, a cím mellett a sortartomány linkje), sorszám nélkül — a
  Törlés ` ```diff ` blokk `-` jellel, mint egyoldalas esetben; a Beszúrás sima code block,
  `+` nélkül.

## Folyamatban — külön blokk

- A Döntés / Teendő blokk **fölött**, ha fut subagent vagy háttérfeladat: soronként mit
  keres vagy csinál, és melyik döntéshez kell az eredménye.
- Ha semmi nem fut, elmarad.

## Döntés és Teendő — külön blokk

- Minden, amit a *Fejlesztő*nek kell csinálnia vagy eldöntenie, **egyetlen** blokkban,
  a válasz **végén**; nem a szövegközben szétszórva.
- **Minden döntés önmagában érthető**: a kérdés és az opciók a fenti szöveg elolvasása
  nélkül is értelmesek — a szükséges kontextus (mi a gond, miért kell dönteni) a döntésben
  van, nem külön szakaszban.
- **Kiemelés a döntésben**: félkövér a helyzet lényege és maga a kérdés; az opcióknál a
  név félkövér, utána az esetleges `(ajánlott)`, majd kettősponttal a következménye.
- **Rövid válasz**: a kérdések számozva, az opciók betűvel (`- a.`, `- b.`), így a
  *Fejlesztő* kóddal válaszolhat (`1a`). A betű elé `- ` kell, különben a Markdown egy
  sorba vonja az opciókat.
- **Csak valódi alternatíva**: opció az, ami a munka célját másképp éri el. A cél feladása
  („marad így”, „nem csinálunk semmit”, „hagyjuk”) nem opció. Ha így egyetlen értelmes lépés
  marad — főleg ha amúgy is az az ajánlott —, az nem Döntés, hanem Folytatás.
- **Nincs nyitott gyűjtő-opció**: „keverék”, „egyéb”, „írd meg, mit szeretnél” nem opció —
  szabad szöveggel a *Fejlesztő* mindig válaszolhat.
- **Döntés csak teljes információval**: ha egy teendő vagy egy futó subagent eredménye
  kizárhat vagy átírhat opciókat, a döntés még nem kerül a blokkba — előbb az eredmény,
  utána a döntés. Addig a függőség a Folyamatban vagy a Teendő blokkban látszik.
- **Teendő csak valódi teendő**: ami a *Fejlesztő* nélkül nem megy (parancs a saját
  gépén, belépés, jóváhagyás egy külső felületen, adat, amit csak ő tud). Az *AI*
  munkájának átnézése nem teendő. A visszajelzés („utána szólj”, „írd meg”, „jelezd”) sem
  külön teendő és nem toldalék — magától értetődik; a teendő csak maga a művelet.
- **Commit, push nem döntés és nem teendő**: a *Fejlesztő* külön commanddal indítja
  (`/workflow:commit`, `/workflow:push`…); a blokkban nem kérdezel rá, és nem kéred.
- A blokk két része, a **Döntés** és a **Teendő**, külön címmel; amelyik üres, az elmarad.
- Ha egyik sincs, a blokk elmarad — üres blokkot ne írj.

## Folytatás

- Csak ha **nincs** Döntés és Teendő: a záró helyén egy sor a javasolt következő
  lépéssel.
- Kérdésként, amire az **OK** önmagában elég válasz (`Megírjam a teszteket a parserhez?`)
  — nem választás opciók között, az Döntés.
- Commit, push nem lehet a Folytatás (→ Döntés és Teendő).
- **Előfeltétel**: ha a lépés előtt a *Fejlesztő*nek kell valamit tennie (mentés, bezárás,
  belépés), új sorban közvetlenül a Folytatás alatt — nem külön Teendő blokkban.
- Ha nincs értelmes következő lépés, elmarad.

## Kivétel

Magyarázat, tanítás, *Fejlesztő* visszakérdez → a sablon laza, a szöveg hosszabb lehet
(→ `communication.md` Kivételek). A státuszjel és a Döntés / Teendő blokk ilyenkor is marad.
