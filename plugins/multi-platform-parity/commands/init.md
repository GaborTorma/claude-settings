---
description: Multi-platform parity init — létrehozza a PARITY.md-t a repo gyökerében a felderített platformokból (oszlop) és a feature-leltárból (sor). Bizonytalan cellát nem talál ki (❓), a fejléc jelzi a kötelező emberi ellenőrzést. Meglévő fájlt nem ír felül megerősítés nélkül.
---

# Multi-platform parity — Init

Kiírja a `PARITY.md`-t a repo gyökerébe: oszlop = felderített platform, sor = feature-leltár. **Bizonytalan cellát nem tippel** (`❓`); a fejléc jelzi, hogy a Fejlesztőnek a cellákat + eltérés-indokokat ellenőriznie/kitöltenie kell.

## Argumentum (`$ARGUMENTS`, opcionális)

- üres → gyökér `PARITY.md`.
- path → oda írja (pl. monorepo egyik al-appjának gyökere).

## Előfeltétel

Ha a célhelyen **már létezik `PARITY.md`** → **ne írd felül**. Jelezd, és ajánld a `multi-platform-parity:audit`-ot (az a meglévőt auditálja a valóság ellen). Felülírás csak explicit Fejlesztő-kérésre.

## Workflow

1. **Platform-felderítés** — az [audit](./audit.md) Workflow 1 szerint (manifest-alapú). **Soft-stop**, ha < 2 platform.
2. **Feature-leltár** — platformonként a top-szintű route/screen/nav/feature lista (SocratiCode `codebase_search`, `Glob`); mikro-interakciókat hagyd ki, bizonytalannál inkább vedd fel. A sorok a feature-ek **uniója** minden platformon.
3. **Cella-meghatározás** — feature × platform:
   - egyértelműen jelen → `✅`
   - egyértelműen hiányzik → `❌`
   - kódból nem eldönthető → `❓` (**ne tippelj**)
   - platformon értelmetlen (pl. complication watch nélkül) → `➖`
4. **Írd ki** a `PARITY.md`-t a sablonból (lásd lent).
5. **Riport** — hány platform, hány feature, **hány `❓` cella** vár kitöltésre. Ajánld: töltsd ki a `❓`-eket és minden nem-`✅` cellánál az eltérés **MIÉRT**-jét.

## Sablon

A scaffold: [../assets/PARITY.template.md](../assets/PARITY.template.md). Olvasd be; az `<feature>` placeholder-sort cseréld a feature-leltárra, az oszlopokat a felderített platformokra, a cellákat a 3. lépés szerint. Írd ki `PARITY.md`-ként a gyökérbe (vagy `$ARGUMENTS` path-ra).

## Mit NEM csinál

- **Nem ír felül** meglévő `PARITY.md`-t megerősítés nélkül.
- **Nem talál ki** cella-értéket — bizonytalan = `❓`.
- **Nem commitol, nem deploy-ol.**
