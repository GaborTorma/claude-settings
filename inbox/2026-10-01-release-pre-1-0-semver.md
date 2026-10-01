---
date: 2026-10-01
source: claude-settings
kind: ?
---

# Kiadás 1.0 előtt: breaking is csak minor, GitHub Release mindig, és javaslat az 1.0-ra

## Mi

A `/release` minden kiadásnál GitHub Release-t is készít; amíg a verzió `0.x`, a
breaking change is csak **minor** léptetés; és a command javaslatot tesz, ha eljött
az ideje az `1.0.0`-nak.

## Miért

A *Fejlesztő* kérése (2026-10-01). A `0.x` a SemVer szerint az instabil szakasz: a
publikus API bármikor változhat, ezért a breaking change itt nem ér major-t — egy
korai projekt különben pár hét alatt `v7.0.0`-ra ugrana. Az `1.0.0` viszont döntés,
nem automatizmus: valakinek ki kell mondania, hogy az API stabil.

A mostani `/release` ennek ellentmond: a `git cliff --init` után beírt `cliff.toml`
`[bump]` blokkja `breaking_always_bump_major = true`, a szöveg pedig „breaking →
MAJOR”. A GitHub Release már benne van (`gh release create $next …`, a deploy és a
tag után) — ezt meg kell tartani.

## Hogyan alkalmazd

- **`cliff.toml`**: `breaking_always_bump_major = false` (vagy elhagyva) — a git-cliff
  `0.x`-ben a breaking-et alapból minorra lépteti, `1.0` fölött majorra.
  `features_always_bump_minor = true` marad.
- **A `/release` szövege**: „breaking → MAJOR” helyett: `0.x`-ben breaking → MINOR,
  `feat` → MINOR, a többi → PATCH; `1.0` fölött breaking → MAJOR.
- **GitHub Release**: minden sikeres kiadásnál, a worklogokból (marad, ahogy van).
- **1.0-javaslat** — a `/release` a verziószámítás után, `0.x`-ben, egy mondatban
  javasolja az `1.0.0`-t (a döntés a *Fejlesztő*é, `major` argumentummal), ha
  teljesül néhány jel, pl.:
  - a szoftver élesben fut, valódi *User*-ek használják;
  - mások építenek rá (más projekt, kliens, publikus API, plugin-felhasználók);
  - az utolsó néhány (pl. 3) kiadásban nem volt breaking change;
  - a *Fejlesztő* stabilnak tekinti az interfészt.
- Rokon, halasztott bejegyzés: `deferred/2026-09-22-versioning.md`.
