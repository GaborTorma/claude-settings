---
name: new-apple-project
description: Új Apple (iOS / iPadOS / watchOS / macOS) projekt bootstrap-ja. Használd amikor a Fejlesztő új Apple/iOS/Swift/SwiftUI/Xcode appot kezd, új Xcode/XcodeGen projektet hoz létre, vagy a kezdeti repó-/projekt-struktúráról, azonosítókról (Bundle ID, Team ID), signingről, .gitignore-ról beszél egy natív Apple appnál. A kiadás (TestFlight/App Store) későbbi fázis — arra külön skillek vannak.
---

# Új Apple projekt — bootstrap

A kezdeti, **egyszer beállítandó** dolgok egy natív Apple appnál: stack, azonosítók,
projekt-struktúra, signing-bekötés, `.gitignore`/`.env`. A kiadás külön:
[testflight](../testflight/SKILL.md) → [app-store-release](../app-store-release/SKILL.md),
screenshotok: [screenshots](../screenshots/SKILL.md).

## Mikor aktiválódj

A Fejlesztő **új** Apple appot kezd (üres repó, első Xcode/`project.yml`,
`Package.swift`, „új iOS app" kérés). Ekkor a setup-döntéseket **most** rögzítsd —
később drágább javítani (Bundle ID nem változtatható, signing átszövi a projektet).

## 1. Stack-döntés

Natív Apple → **Swift + SwiftUI** az alap. A konkrét választásoknál (min. iOS verzió,
SwiftData vs. Core Data vs. GRDB, dependency manager: SPM) **kérdezz és javasolj
2-3 opciót** trade-off-okkal — nincs néma default. A projekt-generálásra **XcodeGen**
(`project.yml`) javasolt: az `.xcodeproj` git-merge-konfliktusait kerüli.

## 2. Azonosítók (kezdéskor rögzítsd)

- **Bundle ID** (`PRODUCT_BUNDLE_IDENTIFIER`, reverse-DNS): **ne találd ki — mindig
  egyeztesd a Fejlesztővel** (állandó identitás, utólag nem változtatható).
- **Team ID** (10 char): signinghez `DEVELOPMENT_TEAM`. A Fejlesztő `~/.claude/.env`
  → **`APPLE_TEAM_ID`** kulcsról hozza.
- **On-device név** (`CFBundleDisplayName`): rövid (~12 char), külön a store-névtől.
- **Verzió**: SemVer marketing-verzió (`MARKETING_VERSION`) + külön `CURRENT_PROJECT_VERSION`
  build szám.

## 3. Projekt-struktúra (XcodeGen)

A `project.yml` a **forrás**; az `.xcodeproj` + Info.plist/entitlements **generált**
(`xcodegen generate` minden változás után). A `DEVELOPMENT_TEAM`-et és a Bundle ID-t
a `project.yml`-ben kösd be (a Team ID env-ből, ne hardkódold a repóba). Starter:
[assets/project.example.yml](assets/project.example.yml).

## 4. `.gitignore` + `.env` (a környezeti szabály szerint)

Másold be a két scaffoldot az első commit előtt:

- [assets/gitignore.apple](assets/gitignore.apple) → a repo gyökerébe `.gitignore`
  néven (env/secrets, build output, Xcode user state, XcodeGen-generált `.xcodeproj`).
- [assets/env.example](assets/env.example) → `.env.example` néven a commitba; a
  tényleges értékek (Team ID, ASC API kulcsok) a `.env`-be (gitignore-olt).

## 5. Info.plist alapok (kezdéskor)

- **Export compliance**: HTTPS-only → `ITSAppUsesNonExemptEncryption = false` (különben
  minden feltöltésnél „Missing Compliance").
- **Permission purpose stringek** (`NS…UsageDescription`) — a használt feature-höz.

## 6. ASC API key (csak ha CI-feltöltést tervezel)

Headless feltöltéshez `APPLE_ISSUER_ID` + `APPLE_KEY_ID` + `.p8` (`AuthKey_<KEYID>.p8`)
— App Store Connect → Users and Access → Integrations → App Store Connect API.

⚠️ **Az API kulcs / `.p8` éles feltöltést indít — használat előtt MINDIG kérdezd meg
a Fejlesztőt.** Bootstrap-kor csak bekötöd/dokumentálod; nem futtatsz vele.

## Checklist

1. [ ] Stack egyeztetve (min. iOS, persistence, SPM) — nem néma default
2. [ ] Bundle ID **egyeztetve** a Fejlesztővel, `project.yml`-be kötve
3. [ ] Team ID `APPLE_TEAM_ID`-ből → `DEVELOPMENT_TEAM`
4. [ ] `xcodegen generate` → build OK (sign nélkül is)
5. [ ] `.gitignore` (Apple minták + `.env`/`*.p8`) + `.env.example` az első commitban
6. [ ] Info.plist: export-compliance flag, display név, permission stringek
7. [ ] Kiadás-időben → [testflight](../testflight/SKILL.md)
