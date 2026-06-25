---
name: testflight
description: iOS (és opcionálisan beágyazott watchOS) app feltöltése TestFlightre. Használd amikor a felhasználó TestFlight feltöltésről, build feldolgozásról, beta-tesztelésről, vagy a feltöltés előtti repó-/Info.plist-előkészítésről (build szám bump, export compliance, on-device név, permission stringek, Archive + Upload) beszél.
---

# TestFlight feltöltés

A kiadás **első fele**: a build előkészítése és feltöltése. Az App Store listing +
beküldés a [app-store-release](../app-store-release/SKILL.md) skill; a screenshotok a
[screenshots](../screenshots/SKILL.md) skill.

## Mit NE te csinálj

Az **Apple credential / aláírás / archiválás / feltöltés** (Xcode → Archive →
Organizer) kizárólag a felhasználóé — ne próbáld helyette. Te a helyes értékeket
adod meg és a sign nélküli build-ellenőrzést végzed; a kattintás a felhasználóé.

## Fázis 0 — Pre-flight (repó)

1. **Build szám bump.** Minden feltöltéshez egyedi build szám kell (nem
   újrahasználható). Új publikus verzióhoz a marketing-verziót (semver) is bumpold.
2. **Export compliance.** HTTPS-only appnál `ITSAppUsesNonExemptEncryption = false`
   az Info.plistbe — különben a build „Missing Compliance"-ban ragad.
3. **On-device név** (`CFBundleDisplayName`): a home screen / app switcher / Safari
   „‹ vissza" gomb neve. Tartsd **rövidnek** (kb. 12 char felett truncál); ez külön
   az App Store listing névtől, ami lehet hosszabb.
4. **Permission purpose stringek** (pl. `NSLocationWhenInUseUsageDescription`) — ha
   a feature használja, kötelező.

## Azonosítók

- **Bundle ID** (`PRODUCT_BUNDLE_IDENTIFIER`): **ne találd ki** — `project.yml` /
  Info.plistből olvasd ki, vagy **egyeztesd a felhasználóval**.
- **Team ID** (10 char, signing → `DEVELOPMENT_TEAM`): a felhasználó env-fájlból
  hozza, `APPLE_TEAM_ID` kulcsról.
- **App Apple ID** (numerikus, store-link): az App Store Connect **generálja** az
  app létrehozásakor — feltöltés előtt még nincs.

### Headless/CI feltöltés — ASC API key

Csak ha nem Xcode Organizerből, hanem `notarytool` / `xcrun altool` / Fastlane
`pilot`-tal töltesz. Kell: **`APPLE_ISSUER_ID`** (UUID, account-szintű), **`APPLE_KEY_ID`**
(10 char), és a **`.p8`** privkulcs (`AuthKey_<KEYID>.p8`). Mind: App Store Connect →
Users and Access → Integrations → App Store Connect API.

⚠️ **Az API kulcs / `.p8` éles feltöltést indít — használat előtt MINDIG kérdezd meg
a felhasználót**, ne futtass vele upload-parancsot megerősítés nélkül. Titkok
`.gitignore`-olva: `.env`, `*.p8`.

## Fázis 1 — TestFlight feltöltés (felhasználó)

Xcode → **Product → Archive** → Organizer → **Distribute → App Store Connect →
Upload** (automatic signing). A build ~5–15 perc alatt feldolgozódik, utána
választható a verzió-oldalon (a beküldéshez lásd [app-store-release](../app-store-release/SKILL.md)).

## Stack-jegyzetek (Xcode / XcodeGen)

- **Headless build sign nélkül** (gyors ellenőrzés): `export
  DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer` (különben nincs
  `xcodebuild`), majd `xcodebuild … -destination 'platform=iOS Simulator,…' build
  CODE_SIGNING_ALLOWED=NO`.
- **XcodeGen**: az `.xcodeproj` + Info.plist/entitlements generált — a forrás a
  `project.yml`; minden változás után `xcodegen generate`.
- **App Group / widget-megosztás**: a megosztott container **csak aláírt buildnél él**
  (eszköz vagy Xcode-ból futtatott sim); automatic signing az első archiváláskor
  regisztrálja a groupot. Sign nélküli buildnél nem ellenőrizhető end-to-end.

## Checklist

1. [ ] Build szám bump, export-compliance flag, rövid on-device név → build OK
2. [ ] Permission purpose stringek megvannak a használt feature-ökhöz
3. [ ] Felhasználó: Archive + Upload, build feldolgozva (Processing kész)
4. [ ] Kész → tovább az App Store beküldésre ([app-store-release](../app-store-release/SKILL.md))
