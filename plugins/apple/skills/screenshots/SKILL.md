---
name: screenshots
description: App Store screenshotok generálása szimulátorból — pontos App Store Connect méret, RGB alfa nélkül, launch-argumentumos navigáció (defaults write helyett), többnyelvű batch YAML configból. Használd amikor a felhasználó App Store / TestFlight screenshot-méretekről, szimulátoros felvételről, vagy a screenshot-automatizálásról beszél. Eszköz: scripts/appstore_screenshots.py.
---

# App Store screenshotok ⚠️

A kiadás screenshot-fázisa — ez fogja meg a legtöbbet. A teljes folyamat:
[app-store-release](../app-store-release/SKILL.md) (beküldés) +
[testflight](../testflight/SKILL.md) (feltöltés). Eszköz:
[scripts/appstore_screenshots.py](scripts/appstore_screenshots.py).

## A buktatók

- **A pontos méretet az ASC feltöltője írja ki — ne feltételezd.** Formátum:
  PNG/JPEG, **RGB, alfa nélkül**, pixel-pontos. Gyakori iPhone méretek: 6.9"
  `1320×2868`, 6.5" `1284×2778` és `1242×2688`. **Trükk**: olyan szimulátort válassz,
  aminek a natív felbontása = a kért méret → nincs átméretezés (pl. a 6.5"-höz
  `iPhone 14 Plus`).
- **A navigáció a buktató**: a szimulátorban nem tudsz kattintani. A bevált minta:
  az app olvasson el pár **csak DEBUG-ban élő, release-ben no-op** felülíró kulcsot
  (melyik nézet/sheet nyíljon, idő/hely/nyelv/zoom, a debug-UI elrejtése, a
  first-launch ablak kihagyása), és ezeket **launch-argumentként** add át —
  **ne `defaults write`-tal**, mert azt a cfprefsd cache-eli és átfolyik a shotok
  közt. Lásd a screenshot-scriptet.
- **Egységes nyelv** + tiszta státuszsáv (9:41). iPad/Watch screenshot csak ha az a
  target be van kapcsolva (iPhone-only: `TARGETED_DEVICE_FAMILY: "1"`).

## Script-használat

[scripts/appstore_screenshots.py](scripts/appstore_screenshots.py) — három subcommand:

- `capture` — egy felvétel tiszta státuszsávval, launch-argumentumokkal.
- `convert` — alfa-strip + pontos méretre vágás (`--size 1284x2778`).
- `generate` — minden shot × minden nyelv egy YAML configból (ajánlott sok shothoz):
  `appstore_screenshots.py generate --config screenshots.yaml`. Egy YAML deklarálja a
  shotokat (eszköz, launch-argok), és minden nyelven legenerálja + a megadott méretre
  vágja. Dummy config: [assets/screenshots.example.yaml](assets/screenshots.example.yaml)
  (iOS = iPhone 14 Plus, watchOS = Apple Watch Ultra 3).

Igények: `xcrun simctl` (teljes Xcode — ha csak Command Line Tools aktív: `export
DEVELOPER_DIR=/Applications/Xcode.app/Contents/Developer`); `convert` → Pillow,
`generate` → PyYAML.

## Checklist

1. [ ] Az ASC kérte **pontos** méret(ek) lekérdezve a feltöltőből
2. [ ] Shotok RGB, alfa nélkül, pixel-pontosak
3. [ ] Egységes nyelv, tiszta státuszsáv (9:41)
4. [ ] Csak a bekapcsolt target-ekhez (iPhone / iPad / Watch)
5. [ ] Feltöltve → vissza a beküldéshez ([app-store-release](../app-store-release/SKILL.md))
