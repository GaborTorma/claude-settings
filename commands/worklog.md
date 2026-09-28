---
name: worklog
description: Worklog-bejegyzés(ek) a .worklog/ mappába arról, mi történt az ágon a main-ről való leválása óta — témánként külön fájl, egy commitban. Használd amikor a Fejlesztő /worklog-ot ír.
allowed-tools: Bash(git branch --show-current), Bash(git log *), Bash(gh repo view *)
---

## Kontextus

- Ág: !`git branch --show-current`
- Repó URL: !`gh repo view --json url -q .url`
- Commitok az ág leválása óta: !`git log --reverse --abbrev=8 --format='%h %H %s' origin/main..HEAD`

Egyszerűen értelmezhető szöveg arról, mi történt. Olvasója a *Fejlesztő* és a
későbbi *AI*-sessionök.

Ha a Kontextus szerint a `main`-en állsz, vagy nincs commit, **állj meg**: nincs mit
összefoglalni.

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
egymástól független dolgok is bekerültek, mindegyik külön fájlt kap. Minden
commit legalább egy témához tartozik; vegyes commit mindegyikhez.

## 3. Fájlok

- **Hely**: `.worklog/` a repó gyökerében, verziókövetve.
- **Név**: `YYYY-MM-DD-HHMM-<téma>.md`: a mostani időpont (helyi idő) + a téma
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

  ## Commitok

  - [[94c9d32a]](https://github.com/<owner>/<repo>/commit/<teljes SHA>) feat(auth): add google oauth provider
  - [[62ad1820]](https://github.com/<owner>/<repo>/commit/<teljes SHA>) test(auth): cover oauth callback
  ```

  - Bekezdések sorrendje: mi történt → miért → döntések (ha volt) → mi maradt
    nyitva (ha van). Folyó szöveg, alcímek nélkül; ahogy egy kollégának elmondanád.
  - `## Commitok`: a témához tartozó összes commit, időrendben, 8 karakteres rövid
    SHA-val. GitHub-remote nélkül link nélkül: `` - `<rövid SHA>` <subject> ``.

**Nem ez**: changelog. A szöveg ne fájl- vagy commitlista legyen — a commitok csak a
végén, hivatkozásként.

## 4. Commit

Az összes fájl egy commitban, push nélkül:

```bash
git add .worklog/
git commit -m "docs(worklog): <téma>[, <téma>…]"
```

Végül írd ki a létrejött fájlok nevét.
