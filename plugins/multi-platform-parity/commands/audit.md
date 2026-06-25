---
description: Multi-platform parity audit — felderíti a repo kliens-platformjait, és a multi-platform-parity skill 5 dimenziója mentén drift-et/réseket keres (verzió-skew, shared core szivárgás, séma-duplikáció, feature-parity hiány, PARITY.md elavulás). Read-only riport; mutáció csak megerősítéssel.
---

# Multi-platform parity — Audit

A repo cross-platform **parity-állapotát** auditálja a [multi-platform-parity skill](../skills/multi-platform-parity/SKILL.md) 5 dimenziója mentén. **Read-only**: felderít, elemez, riportál — mutáció csak megerősítéssel (Workflow 5).

## Argumentum (`$ARGUMENTS`, opcionális)

- üres → teljes audit minden platformra, minden dimenzióra.
- platform-név (`ios`, `android`, `pwa`, `watch`, …) → csak az adott platformot érintő réseket riportálja.
- feature-név → csak arra a feature-re szűkít (megvan-e minden platformon, dokumentált-e az eltérés).
- `--fix` → riport után **felajánlja** a biztonságos remediációkat (lásd Workflow 5), nem alkalmazza automatikusan.

## Workflow

1. **Platform-felderítés**. Detektáld a kliens-platformokat manifestek alapján:
   - **PWA/web**: `manifest.webmanifest`/`manifest.json` (`display` mező), service worker (`sw.js`, `workbox`, `vite-plugin-pwa`), `package.json`.
   - **iOS / iPad / watchOS**: `*.xcodeproj`, `*.xcworkspace`, `project.yml` (XcodeGen), `Info.plist`, `Package.swift`; `TARGETED_DEVICE_FAMILY` (`1` iPhone, `2` iPad, `4` watch), watch-target / `*.appex`.
   - **Android**: `build.gradle(.kts)`, `AndroidManifest.xml`, `settings.gradle`.
   - **Desktop**: `electron`, `tauri.conf.json`.
   - **Cross-platform keret** (egy kódbázis, több target): Flutter `pubspec.yaml`, Expo/RN `app.json`+`metro.config.js`, Capacitor `capacitor.config.*` → a feature-parity nagyrészt inherens, de a **verzió/store-skew** dimenzió így is él.
   - Eszköz: `Glob`/`grep`; struktúra-megértéshez SocratiCode `codebase_search`.
   - **Soft-stop**: ha < 2 platform → „Egyetlen platformot látok (`X`) — nincs mit parity-auditálni."

2. **Forrás-beolvasás**. Platformonként gyűjtsd be: marketing-verzió, `PARITY.md` (gyökér), API-séma forrás, shared core mappák, feature-flag mechanizmus, teszt-mappák.
   - **Ha nincs `PARITY.md`** → `AskUserQuestion`: „Nincs PARITY.md (a parity-állapot forrása). Létrehozzam?"
      - **igen** → futtasd a [multi-platform-parity:init](./init.md)-et (a már felderített platformokkal), majd a generált fájllal folytasd.
      - **nem** → 🚨 találat (5. dimenzió), folytasd read-only.

3. **Elemzés** a lenti 5 dimenzió mentén — **mind**, egyben (ne állj meg az első találatnál). A platformfüggetlen tényt (verzió, séma, mappa) **olvasd ki** (`grep`/`Read`/SocratiCode), ne találgass.

4. **Riport** chatben, a lenti severity-formátumban. Minden találat: mi, hol (`file:line` link), miért parity-kockázat, javasolt fix. **Ennyi**, ha nincs `--fix`.

5. **Remediáció** (csak `--fix`, vagy ha a user kéri). `AskUserQuestion`-nel ajánld fel a biztonságosakat, és csak jóváhagyás után alkalmazd:
   - `PARITY.md` létrehozása → a [multi-platform-parity:init](./init.md) command (ha még hiányzik; lásd Workflow 2).
   - Verzió single-source bevezetésének konkrét diffje.
   - Duplikált logika core-ba emelésének terve (kódmozgatás → user dönt).
   - Visszafordíthatatlan/kifelé ható lépést (deploy, store, commit) **soha** — azt a user csinálja.

## Mit ellenőriz (5 dimenzió)

A SKILL 5 dimenziója audit-checkekre fordítva (kérdés + severity):

**1. Verzió- és release-koordináció**
- Ugyanaz a marketing-verzió minden platformon? (iOS `MARKETING_VERSION`/`CFBundleShortVersionString`, Android `versionName`, PWA `package.json`+`manifest` `version`, Flutter `pubspec` `version`.) Eltérés → 🚨/⚠️.
- Van **single-source** a verzióra (root verzió-fájl / generált), vagy platformonként kézzel hardkódolt? Utóbbi → ⚠️.
- Backend `minSupportedVersion` / forced-update gate létezik? Hiánya régi-kliens kockázat → ⚠️.
- PWA: verzió-bélyegzett service worker + explicit frissítési stratégia? Cache-busting hiánya → ⚠️.

**2. Shared core**
- Üzleti logika / validáció (`zod`) / állapotgép / formázás **duplikálva** több platform-mappában a közös core helyett? (Heurisztika: ugyanaz a szabály `ios/` ÉS `android/` ÉS `apps/web` alatt.) → ⚠️.
- Van-e közös core (`packages/`/`shared/`/`core/`), és minden platform **ugyanazt a verziót/SHA-t** pinneli? Eltérő pin → 🚨 (rejtett drift).

**3. API/séma single-source + backward compat**
- Séma single source (`zod`/OpenAPI/proto) + **generált** kliens-típusok, vagy kézzel duplikált DTO-k platformonként? Duplikáció → ⚠️.
- API-verziózás (`/v1`,`/v2`) vagy mezőszintű kompat a nem-frissíthető régi kliensekért? Hiánya breaking-kockázat → ⚠️.
- Generált fájl kézzel módosítva (drift a sémától)? → 🚨.

**4. Feature/UX parity**
- Feature-leltár platformonként (route/screen/nav alapján, SocratiCode `codebase_search`), és **diff**: mi van meg az egyiken, a másikon nem? A `PARITY.md`-ben **dokumentálatlan** aszimmetria → ⚠️ (bizonytalan → ℹ️, jelöld hogy emberi megerősítés kell).
- Feature-flag a core-ban, remote-vezérelt — vagy build-time/platform-fork (`#if`, `BuildConfig`)? Build-time flag → ℹ️/⚠️.

**5. PARITY.md, DoD, divergencia-napló**
- `PARITY.md` létezik a gyökérben? Hiánya → 🚨 (nincs forrás a parity-állapotra); az audit felajánlja a létrehozását az `init`-tel (Workflow 2).
- A mátrix **egyezik a valósággal**? Cella `✅`, de a feature kódban hiányzik (vagy fordítva) → ⚠️.
- Minden eltérésnél ott a **MIÉRT**? Indoklatlan `❌`/`➖` → ⚠️. Store-csúszás `➖`-ként jelölve `🗓️` helyett → ℹ️.
- Per-platform teszt + közös fixtures / contract teszt a séma ellen? Hiányos teszt-parity → ℹ️.

## Output formátum

Severity-rendezve, dimenziónként csoportosítva:

```
## 1. Verzió-koordináció
   🚨 iOS 1.2.0 vs Android 1.1.3 — eltérő marketing-verzió. [project.yml:14](...) — vezess be verzió single-source-ot.
   ⚠️ Nincs minSupportedVersion gate a backendben — régi kliens töri a /v2 választ.

## 4. Feature parity
   ⚠️ "Export PDF" megvan iOS-en, hiányzik Androidon, PARITY.md-ben nincs dokumentálva.
   ℹ️ watchOS "Settings" — valószínűleg szándékos kihagyás, erősítsd meg.
```

**Severity**:
- 🚨 **Critical**: verzió-skew, eltérő core-pin, sémától driftelt generált fájl, hiányzó `PARITY.md`.
- ⚠️ **Warning**: hardkódolt verzió, duplikált logika/DTO, dokumentálatlan feature-aszimmetria, hiányzó backward-compat gate, valótlan PARITY.md-cella.
- ℹ️ **Info**: build-time flag, bizonytalan (emberi megerősítést igénylő) aszimmetria, teszt-parity rés, fogalmazási finomítás.

Záró sor: **összesítés** (platformok száma, találatok severity szerint), és ha nincs 🚨/⚠️ → „Parity OK a vizsgált dimenziókban."

## Mit NEM csinál

- **Alapból nem mutál** — nem ír fájlt, nem commitol, nem deploy-ol. Csak `--fix`/kérésre, megerősítéssel.
- **Nem dönt szándékos divergenciáról** — a dokumentálatlan eltérést jelzi; hogy bug vagy szándékos, azt a user mondja meg (`AskUserQuestion`), és a `PARITY.md`-be kerül.
- **Nem hajt végre store/deploy lépést** — kifelé ható, visszafordíthatatlan → user.
