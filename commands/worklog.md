---
name: worklog
description: Worklog-bejegyzés(ek) a .worklog/ mappába arról, mi történt az ágon a main-ről való leválása óta — témánként külön fájl, egy commitban. Használd amikor a Fejlesztő /worklog-ot ír.
allowed-tools: Bash(git branch --show-current), Bash(git log *), Bash(git diff *), Bash(git remote get-url *), Write(.worklog/**), Bash(git add .worklog/), Bash(git commit *)
---

## Kontextus

- Ág: !`git branch --show-current`
- Remote: !`git remote get-url origin 2>/dev/null || echo "NINCS"`
- Commitok az ág leválása óta: !`git log --reverse --abbrev=8 --format='%h %H %cd %s' --date=format-local:%Y-%m-%d-%H%M origin/main..HEAD 2>/dev/null || echo "NINCS"`

Egyszerűen értelmezhető szöveg arról, mi történt. Olvasója a *Fejlesztő* és a
későbbi *AI*-sessionök.

Ha a Kontextus szerint a `main`-en állsz, vagy nincs commit, **állj meg**: nincs mit
összefoglalni. A commitlista `NINCS`: nincs `origin/main` — **állj meg**, és jelezd.

## 1. Hatókör

Minden, ami az ág `main`-ről való leválása óta történt — nem csak az ág eredeti
célja: a Kontextus commitlistája. Ha a listában már van `docs(worklog):` commit
(egy korábbi futásból), csak az utolsó ilyen **utáni** commitok számítanak; ha
utána nincs commit, **állj meg** — nincs új összefoglalnivaló, ez nem hiba. A tartalmukhoz:

```bash
git diff origin/main...HEAD
```

A commitolatlan változás nem tartozik bele — előbb commitolj.

## 2. Témák

Csoportosítsd a változásokat témák szerint. Egy téma = egy fájl: ha az ágra
egymástól független dolgok is bekerültek, mindegyik külön fájlt kap. Vegyes commit
mindegyik témájához.

Témát az a változás ad, ami a *User* vagy a *Fejlesztő* szemszögéből történetet
hordoz. Kiindulás a commit típusa:

| Típus | Worklog |
| --- | --- |
| `feat`, `fix`, `perf`, `refactor`, `revert`, `deploy`, bármely `!` | **téma**: saját fájl, szöveggel |
| `docs`, `test`, `build` | **csak lista**: a legközelebbi téma commitlistájába, szöveg nélkül |
| `style`, `chore`, `docs(worklog)` | **kimarad** |

- **Felfelé**: ha egy „csak lista” vagy „kimarad” típus az ág fő munkája (pl. egy
  docs-repó tartalma, build-rendszer csere), az téma.
- **Lefelé**: a történet nélküli „téma” típusú commit (elírás-`fix`, egysoros
  `refactor`) csak a listába kerül.
- Ha nem marad téma, **állj meg** — nincs érdemi összefoglalnivaló, ez nem hiba.

## 3. Fájlok

- **Hely**: `.worklog/` a repó gyökerében, verziókövetve.
- **Név**: `YYYY-MM-DD-HHMM-<téma>.md`: a téma legutolsó commitjának időpontja (a
  Kontextus commitlistájának dátum-oszlopa, helyi idő) + a téma
  rövid neve (angol, ASCII kebab-case, 2–4 szó), a tartalomból — nem az ág nevéből.
- **Nyelv**: magyar.
- **Tartalom** — minta:

  ```markdown
  # Google-fiókos bejelentkezés

  A bejelentkezési oldalra bekerült a Google-fiókos belépés; az új *User* egy
  kattintással regisztrál, a meglévő fiók az e-mail-cím alapján kapcsolódik.

  Eddig csak e-mail + jelszó volt, és a regisztrációk jó része a jelszó-megerősítésnél
  elakadt.

  Kész auth-könyvtár helyett saját callback-route lett: a meglévő session-kezeléshez
  így nem kellett hozzányúlni.

  Nyitva maradt: az Apple-belépés, és mi legyen, ha két fiók ugyanazzal az e-maillel
  jön.

  - [`[94c9d32a]`](https://github.com/<owner>/<repo>/commit/<teljes SHA>) · feat(auth): add google oauth provider
  - [`[62ad1820]`](https://github.com/<owner>/<repo>/commit/<teljes SHA>) · test(auth): cover oauth callback
  ```

  - Bekezdések sorrendje: mi történt → miért → döntések (ha volt) → mi maradt
    nyitva (ha van). Folyó szöveg, alcímek nélkül; ahogy egy kollégának elmondanád.
  - Commitlista a szöveg után, címsor nélkül: a témához tartozó commitok (a „csak lista” commitokkal együtt),
    időrendben. A link alapja a Kontextus **Remote** sorából: `git@github.com:<owner>/<repo>.git`
    vagy `https://github.com/<owner>/<repo>.git` → `https://github.com/<owner>/<repo>`. Nem
    GitHub-remote vagy `NINCS` → link nélkül.

**Nem ez**: changelog. A szöveg ne fájl- vagy commitlista legyen — a commitok csak a
végén, hivatkozásként.

## 4. Commit

Az összes fájl egy commitban, push nélkül:

```bash
git add .worklog/
git commit -m "docs(worklog): <téma>[, <téma>…]"
```

Végül írd ki a létrejött fájlok nevét.
