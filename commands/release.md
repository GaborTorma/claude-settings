---
name: release
description: Kiadás a main-ről — git-cliff verzió, CHANGELOG, release-commit, deploy, és csak sikeres deploy után tag, push és GitHub Release a worklogokból. Használd amikor a Fejlesztő /release-t ír, vagy élesíteni / új verziót kiadni akar.
argument-hint: "major | minor | patch (opcionális, felülírja a számított verziót)"
allowed-tools: Bash(git branch --show-current), Bash(git status *), Bash(git describe *)
---

## Kontextus

- Ág: !`git branch --show-current`
- Munkakönyvtár: !`git status --short`
- Utolsó kiadás: !`git describe --tags --abbrev=0 --match 'v*' || true`

A `main` állapotát adod ki. Az élesben lévő állapotot a legutóbbi `v*` tag jelzi;
ami utána jött, az kiadatlan — akárhány merge is. A command meghívása maga a
deploy-engedély — kivéve, ha élesítési teendő van (→ 4. Deploy).

## 1. Előfeltételek

Tiszta munkakönyvtár kell (Kontextus **Munkakönyvtár** sora üres); ha nem az,
**állj meg**. Az **Utolsó kiadás** hibája (`No names found`) azt jelenti: ez az
első kiadás.

```bash
git fetch --tags
git switch main
git pull --ff-only
```

- **`/check`** a `main`-en: végső ellenőrzés a merge-ek együttes eredményén, deploy előtt.
  Elbukik → **állj meg**, mutasd a hibát.
- Ha a `HEAD` egy pusholatlan `chore(release): …` commit (egy korábbi bukott
  kiadásból), azt használd újra: ugorj a **4. Deploy**-ra.
- Ha nincs `cliff.toml`: `git cliff --init`, és a végére:

  ```toml
  [bump]
  features_always_bump_minor = true
  breaking_always_bump_major = true
  initial_tag = "v0.1.0"
  ```

## 2. Verzió

```bash
last=$(git describe --tags --abbrev=0 --match 'v*' 2>/dev/null)
next=$(git cliff --bumped-version)
```

Ha a *Fejlesztő* adott argumentumot: `git cliff --bump <major|minor|patch> --bumped-version`.

Ha `next` = `last`: a legutóbbi tag óta nincs új commit — **állj meg**, nincs mit
kiadni. (Minden más commit léptet: breaking → MAJOR, `feat` → MINOR, a többi → PATCH.)

## 3. Release-commit

1. `CHANGELOG.md`: `git cliff --unreleased --tag $next --prepend CHANGELOG.md`
   (ha még nincs a fájl: `-o CHANGELOG.md`).
2. Verziófájlok a stack szerint (projekt `CLAUDE.md` vagy a stack skillje), pl.
   `package.json` `version`, `pyproject.toml`, Apple `MARKETING_VERSION`.
3. `git commit -m "chore(release): $next"` — **push nélkül**.

## 4. Deploy

**Élesítési teendők** a kiadandó merge-ek leírásából:

```bash
git log $last..main --merges --format=%B   # első kiadásnál: git log main --merges --format=%B
```

Ha valamelyikben van `## Élesítés` szakasz: a tételeket gyűjtsd egy listába, a
`PR:` sorból vett PR-számmal (`- #<szám> · <tétel>`), mutasd meg, és a deploy
előtt kérj megerősítést — a teendők egy része (pl. env beállítása) a deployt
megelőzi. Ha egyikben sincs, ez a lépés elmarad.

Deploy ebből a commitból, az első találat szerint:

1. **Projekt `CLAUDE.md`** vagy a **stack skillje** deploy-módot ír → azt.
2. **`package.json` `deploy` script** → a lockfile szerinti package managerrel;
   **`Makefile` `deploy` target** → `make deploy`.
3. **Egyik sem** → **állj meg**, kérdezd meg a *Fejlesztő*t. Ne találj ki deploy-módot.

Ha a hosting a `main` pusholására magától élesít, **állj meg** és jelezd: ez a
folyamat kikapcsolt auto-deployt feltételez.

**Bukás** → mutasd a hibát/logot és **állj meg**. Nincs tag, nincs push; a
release-commit helyben marad, a következő `/release` újrahasználja.

## 5. Siker után

```bash
git tag -a $next -m "$next"
git push origin main $next
```

**GitHub Release** a `last..$next` között létrejött worklogokból:

```bash
git diff --name-only --diff-filter=A $last..$next -- .worklog/   # első kiadásnál: minden .worklog/ fájl
gh release create $next --title "$next" --notes-file <notes>
```

A notes a *User*-nek szól, magyarul: a worklogok rövid, felhasználói szemszögű
összefoglalója (nem másolat, nem commitlista), alatta linkek a worklog-fájlokra.

Végül válts vissza az indulási ágra (tipikusan `dev`), és írd ki: verzió, deploy
URL / azonosító, a GitHub Release URL-je.
