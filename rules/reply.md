# Válasz-formátum

**Cél**: rövid, tagolt, lényegre törő válasz, a lehető legtöbb vizuális tartalommal. A
*Fejlesztő* egy pillantással lássa az eredményt és a teendőjét — olvasás nélkül.
A szóhasználat: → `communication.md`.

## Sablon

```markdown
✅ <egy sor: mi lett, működik-e, félkövér kiemeléssel a lényeg>

<vizuális rész: widget, diff-részlet — ami a lényeget mutatja>

- <legfeljebb ~5 tagolt pont, félkövér kiemeléssel a lényeg, csak ami a vizuális részből nem látszik>

> **❓ Döntés**
> 1. **<a helyzet lényege — ha a kérdés önmagában nem elég>** <rövid kontextus — ha a lényeg nem elég>. **<a kérdés>?**
>    - a. **<opció>** (ajánlott): <mi történik, ha ezt választod>
>    - b. **<opció>**: <mi történik, ha ezt választod>
>
> **⭕ Teendő**
> - <mit kell a *Fejlesztő*nek csinálni, hol>
```

## Státusz — az első karakter

Ha teszteltünk, kísérleteztünk, futtattunk, ellenőriztünk valamit, vagy a *Fejlesztő*
kért valamit, a válasz **első karaktere** az eredmény:

| Jel | Jelentés |
| --- | --- |
| ✅ | működik — ellenőrizve; vagy a kért módosítás megtörtént |
| ❌ | nem működik |
| ⚠️ | részben megy, vagy mellékhatással, vagy a kért módosítás csak részben történt meg |
| ❔ | nincs ellenőrizve (nem futott, nem lehetett tesztelni) |

- Több teszt → táblázat, soronként egy jellel (`| Teszt | ✅/❌ | Megjegyzés |`).
- ✅ működésre csak futtatott ellenőrzés után; ami ellenőrzést igényelne, de nem futott, az ⭕.
- ❌-nál a hibaüzenet (ha van) szó szerint, code blockban, utána megoldási javaslat.

## Vizuális tartalom

Ha a válasz lényege látvány — mutasd, ne írd le.

- **Mikor**: UI-variánsok összevetése (ikon, karakter, szín, betű, layout), mockup,
  diagram (architektúra, flow, állapotgép, git-ág), chart / adatsor, vizuális döntés.
- **Elsőként widget**: `mcp__visualize__show_widget` — inline, a válasz mellett. Előtte
  egyszer `mcp__visualize__read_me` a megfelelő modullal (`mockup`, `diagram`, `chart`,
  `elicitation`…); ezt ne narráld.
- **Valós méret**: az elem a widgetben pontosan akkora, mint a valóságban (px, font-size,
  font-name, ikonméret a projekt kódjából kiolvasva) — nem felnagyítva, nem kicsinyítve.
- **Minden változat**: ha több méretben használatos (pl. 16/24/32 px ikon, mobil/desktop),
  mindegyikben; ha az adott elem előfordul több színváltozatban, mindegyikben;
  ha van világos/sötét mód, mindkettőben.
- **Több verzió**: ha a *Fejlesztő* nem egy konkrét módosítást kér, akkor mindig több verziót
  mutass, amiből választhat.
- **Választás vizuális opciókból**: az opciók egymás mellett a widgetben, címkével (pl.
  Unicode kód); a döntést `sendPrompt`-tal vagy `AskUserQuestion`-nel kérd.
- **Ha a widget nem elég → dev preview**: a projekt valódi kódja, CSS-e, fontja,
  komponense kell, vagy futó app / több oldalas interakció →
  `mcp__Claude_Browser__preview_start` (`.claude/launch.json`).
- **Nagy grafikai változás → `/design`**: ha nem fér bele egy kis widgetbe (teljes oldal-
  vagy képernyőterv, új vizuális irány, design system, több képernyős flow) vagy várhatóan
  sok módosítást igényel, a `/design` commanddal készüljön.
- **Tervek összehasonlíthatósága**: ha `/design`-nal készítesz mockupot, és ezeken nagyobb
  módosítást kell végezni, akkor új verziót csinálj. Tehát ha van A, B, C verzió, a B
  alapvetően jó, de változtatni kell rajta, akkor csinálj D verziót, ne a B-t szerkeszd át.
- **Kisebb léptékben is**: táblázat felsorolás helyett, ha 2+ tulajdonságot vetsz össze;
  diff-részlet a változás leírása helyett.
- **Ne**: ASCII-rajz vagy hosszú szöveges leírás ott, ahol egy widget egyértelműbb.

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
- A blokk két része, a **Döntés** és a **Teendő**, külön címmel; amelyik üres, az elmarad.
- Ha egyik sincs, a blokk elmarad — üres blokkot ne írj.

## Kivétel

Magyarázat, tanítás, *Fejlesztő* visszakérdez → a sablon laza, a szöveg hosszabb lehet
(→ `communication.md` Kivételek). A státuszjel és a Döntés / Teendő blokk ilyenkor is marad.
