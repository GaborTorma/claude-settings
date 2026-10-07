---
name: unpark
description: Tétel(ek) törlése a projekt .parked.md parkolójából ID alapján — elvetéskor, issue-vá léptetéskor, vagy amikor a pick-elt tétel munkája lezárult. Használd amikor a Fejlesztő /unpark-ot ír, vagy a /parked egy lezárt pick-elt tételt talál.
argument-hint: "P01 P03 …"
allowed-tools: Bash(cat .parked.md *), Edit(.parked.md)
---

## Kontextus

- Argumentum: $ARGUMENTS
- Parkoló: !`cat .parked.md 2>/dev/null || echo "NINCS"`

## 1. Mit

- **Argumentum**: egy vagy több ID (`P01`; a `P` és a vezető nulla elhagyható: `1`), szóközzel vagy vesszővel elválasztva.
- **Nincs argumentum**: `AskUserQuestion`, header: `Kivétel`, `multiSelect: true`, az
  opciók a parkoló tételek, a `label` pontosan a tétel sora.
- **Üres parkoló** (a Kontextus **Parkoló** sora `NINCS`, vagy nincs tétel): csak ennyi —
  `Nincs parkoló tétel.`

## 2. Törlés

A megadott ID-jű tételeket (a sort és az utána lévő üres sort) töröld a `.parked.md`-ből, a többi sor, a sorrend és a végén a
`<!-- next id -->` számláló marad. Az ID-ket ne számozod újra. Nem létező ID → a válaszban jelezd, a többit töröld.

## 3. Válasz

Soronként: `Törölve: <ID> · <tétel>`; nem létező ID-nél: `Nincs ilyen: <ID>`.
