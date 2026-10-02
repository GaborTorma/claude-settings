# Helyi beállítások (locale)

Alapértelmezés minden projektben, ha a projekt mást nem ír elő: **magyar *User*, Magyarország**.

## Idő

- **Időzóna**: `Europe/Budapest` (CET/CEST, aktuális időszámítással).
- **Tárolás, API, log**: UTC, ISO 8601
- **Megjelenítés**: mindig explicit `timeZone: 'Europe/Budapest'`
- **Csak dátum** (születésnap, határidő): `date` típus, időzóna nélkül.

## Formátum a *User* felé

| Mi | Formátum | Példa |
| --- | --- | --- |
| Dátum | rövid / hosszú (csak önállóan, idő nélkül) | `2026.10.02.` / `2026. október 2.` |
| Idő | 24 órás | `19:12` |
| Dátum és idő | rövid dátum + 24 órás | `2026.10.02. 19:12` |
| Hét első napja | hétfő | |
| Szám | tizedesvessző, ezres tagolás szóközzel | `1 234 567,89` |
| Pénz | HUF, tizedes nélkül | `12 990 Ft` |
| Mértékegység | metrikus (SI) | `12,5 km`, `3 kg`, `1 l`, `22 °C`, `90 km/h` |

- **Nem törő szóköz** (U+00A0, HTML-ben `&nbsp;`): az ezres tagolásban, dátum-idő,
  valamint a szám és a mértékegység / pénznem között — a sortörés nem választhatja szét.
- **Rendezés**: az ékezetes betűk valós sorrendje szerint (`a < á < b`).
- **Telefonszám**: E.164-ben (`+36…`).

## *AI* kommunikáció

- Relatív dátum ("holnap", "jövő héten") → abszolút dátumra váltva, ha rögzítésre kerül.
- Időpont a *Fejlesztő*nek budapesti idő szerint, eltérésnél az időzóna megnevezve.
