---
name: app-store-release
description: iOS app beküldése és kiadása az App Store-ra. Használd amikor a Fejlesztő App Store beküldésről/kiadásról, App Store Connect listingről, vagy App Privacy / Age Rating / Export Compliance / Copyright / Content Rights kérdésről beszél — akkor is, ha csak annyit mond, hogy "kiadom/beküldöm az appot". A folyamatot fázisokra bontja és kiemeli a tipikus blokkolókat.
---

# App Store beküldés és kiadás

A kiadás **második fele**: a build már fent van TestFlighten (lásd
[testflight](../testflight/SKILL.md)) — innen a listing, a kérdőívek, a beküldés és a
go-live. A screenshotok külön: [screenshots](../screenshots/SKILL.md). A mezőnkénti
listing-részletek (limitek, kérdőív-válaszok):
[references/appstoreconnect-checklist.md](references/appstoreconnect-checklist.md).

## Mit NE te csinálj

**Fejlesztő**: a **Submit / Release gombok** és a kérdőívek **véglegesítése
(Publish / Submit)** — te a helyes értékeket adod, a kattintás az övé. **Te**:
listing-szövegek, Privacy/Support oldalak, a teljes checklist előkészítése.

## Fázis 1 — Kötelező URL-ek

**Privacy Policy** + **Support URL**, mindkettő **elérhető** (HTTP 200).
Legegyszerűbb: már deploy-olt webappon `/privacy` és `/support`. A privacy szöveg
**fedje a tényleges adatkezelést** — on-device-only, sosem továbbított adat nem
„gyűjtés".

## Fázis 2 — Listing szövegek

Karakterlimit-érzékeny. Sablon: [assets/listing.template.md](assets/listing.template.md)
(HU+EN slot + limitek); mező-részletek a
[checklist referenciában](references/appstoreconnect-checklist.md). **Számold a
karaktereket** beillesztés előtt.

## Fázis 3 — Screenshotok

A kötelező screenshotok feltöltése (pontos ASC-méret, RGB alfa nélkül, egységes
nyelv) → külön skill: [screenshots](../screenshots/SKILL.md). Hiányzó/rossz méretű
screenshot blokkolja az „Add for Review"-t.

## Fázis 4 — App-szintű mezők (blokkolják az „Add for Review"-t)

- **Copyright** (kötelező, könnyű kifelejteni): `ÉV Jogtulajdonos` (© és a „Copyright"
  szó nélkül); a jogtulajdonos az app készítője.
- **Age Rating** kérdőív (4+/9+/13+/16+/18+).
- **App Privacy** kérdőív: app-szintű, **Admin** + **Publish**. On-device-only adat
  → „No, we do not collect data".
- **Content Rights**, **Pricing & Availability** (Free + országok).

## Fázis 5 — Beküldés (Fejlesztő)

A verzió-oldalon a feldolgozott **buildet** kiválasztani; **Version Release** =
**Manually** (ajánlott — te időzíted a go-live-ot); **Notes for Review** (ha nincs
login, írd le); **Add for Review → Submit**.

## Fázis 6 — Kiadás után

Jóváhagyás után (Manual esetén) „Release This Version". A megosztható link a
numerikus **Apple ID**-ből: `https://apps.apple.com/app/id<APPLE_ID>` (App Store
Connect → App Information → Apple ID). Propagáció akár pár óra. Jegyezd fel az Apple
ID-t a projekt CLAUDE.md-jébe.

## ⚠️ Védjegy / „nem hivatalos" kockázat

Ha az app harmadik fél márkájára/nevére épül → App Review **4.1(c) + 5.2.1**
(gyakori elutasítás). Mitigáció: **írásos engedély** a jogtulajdonostól a Review
Notes-ba (ez véd igazán) · **referenciális név** („Guide for X") + saját ikon ·
**disclaimer** a leírás első sorában, az appban és első-indításkori ablakban. A
puszta „unofficial" csökkent, de nem old fel.

## Checklist

1. [ ] Privacy + Support oldal él (200)
2. [ ] Listing szövegek HU/EN, limiten belül
3. [ ] Screenshotok feltöltve ([screenshots](../screenshots/SKILL.md))
4. [ ] Build kiválasztva (TestFlightről feldolgozva)
5. [ ] Copyright, Age Rating, App Privacy (Publish!), Content Rights, Pricing
6. [ ] Védjegy-kockázat rendezve, Notes for Review
7. [ ] Version Release = Manual, Submit
8. [ ] Release; Apple ID → link a CLAUDE.md-be
