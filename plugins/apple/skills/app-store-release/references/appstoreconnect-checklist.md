# App Store Connect — mezőnkénti checklist

A SKILL.md fázisaihoz: karakterlimitek, kérdőív-válaszok, tipikus blokkolók. A
limitek 2026-os állapot; ha eltérést látsz, az ASC felülete az igazság.

## Listing szövegek (per lokalizáció)

| Mező | Limit | Megjegyzés |
|---|---|---|
| App Name | ≤ 30 | Indexelt (ASO). Lehet hosszabb, mint a `CFBundleDisplayName`. |
| Subtitle | ≤ 30 | Indexelt. |
| Keywords | ≤ 100 | Vesszővel, **szóköz nélkül**. Indexelt. |
| Description | ≤ 4000 | Nem indexelt. Nem hivatalos appnál az **első sor** a disclaimer. |
| Promotional Text | ≤ 170 | Új beküldés nélkül szerkeszthető. |
| What's New | ≤ 4000 | Update-nél kötelező, első verziónál opcionális. |

## App Information (app-szintű)

- **Primary / Secondary Category.**
- **Copyright** (kötelező): `ÉV Jogtulajdonos` — © jel és a „Copyright" szó nélkül; a
  jogtulajdonos az app készítője, nem a hivatkozott márka.
- **Content Rights**: harmadik fél tartalma? Saját tartalom → „No".
- **Age Rating**: kérdőív (4+/9+/13+/16+/18+); ártalmatlan appnál 4+.

## App Privacy kérdőív

App-szintű, **Admin/Account Holder** + **Publish** (különben blokkolja az „Add for
Review"-t). **On-device-only** adat (sosem hagyja el az eszközt) Apple szerint
**nem** „collection" → **„No, we do not collect data from this app." → Save →
Publish.** Publikus adat behúzása (HTTPS) sem trigger; csak amit ténylegesen
elküldesz a készülékről, azt kell bevallani.

## Export Compliance

HTTPS/standard titkosítás → exempt: `ITSAppUsesNonExemptEncryption = false` az
Info.plistbe (a [testflight](../../testflight/SKILL.md) pre-flight része). Enélkül
„Missing Compliance" + minden beküldésnél kérdez.

## Beküldés és kiadás

- **Build**: a feldolgozott (Processing kész) buildet kell kiválasztani.
- **Version Release**: *Automatically* / *Scheduled* / **Manually** (ajánlott —
  „Pending Developer Release", te nyomsz „Release"-t).
- **Notes for Review**: login-info / kontextus; nem hivatalos appnál a magyarázat +
  engedély.

## Tipikus „Unable to Add for Review" okok

Hiányzó **Copyright** · nem publikált **App Privacy** · kitöltetlen **Age Rating** ·
rossz méretű/alfás **screenshot** · „Missing Compliance" · nincs kiválasztott **Build**.

## Screenshot

A pontos méret + alfa-strip + szimulátoros felvétel: külön skill,
[screenshots](../../screenshots/SKILL.md). Röviden: a méretet az **ASC feltöltője
írja ki**, PNG/JPEG, **RGB alfa nélkül**, pixel-pontos.

## Link

A numerikus **Apple ID** (App Information → Apple ID) → `https://apps.apple.com/app/id<APPLE_ID>`
(nem a bundle ID; régió-prefix opcionális). Badge/QR: tools.applemediaservices.com.
