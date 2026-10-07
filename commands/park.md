---
name: park
description: Új tétel felvétele a projekt .parked.md parkolójába. Használd amikor a Fejlesztő /park-ot ír, vagy menet közben egy témát parkolni kell (→ focus.md).
argument-hint: "a parkolandó téma (opcionális)"
allowed-tools: Bash(cat .parked.md *), Bash(grep *), Bash(git remote get-url *), Write(.parked.md), Edit(.parked.md), Write(.gitignore), Edit(.gitignore), Bash(git add .gitignore), Bash(git commit *), Skill(issue *)
---

## Kontextus

- Argumentum: $ARGUMENTS
- Parkoló: !`cat .parked.md 2>/dev/null || echo "NINCS"`
- A `.gitignore`-ban: !`grep -qxF .parked.md .gitignore 2>/dev/null && echo igen || echo nem`
- Remote: !`git remote get-url origin 2>/dev/null || echo "NINCS"`

## 1. A tétel

- **Szöveg**: az **Argumentum** sor, a *Fejlesztő* szavaival; ha üres, a beszélgetésből a
  legutóbb félretett téma. Ha nem egyértelmű, melyik: kérdezz rá.
- **Egy sor**, később is érthetően: mi a téma, és ha kell, mi van vele hátra.
- **Hossz**: a tétel szövege (ID, jelölés és dátum nélkül) optimálisan 100–150 karakter,
  legfeljebb 200.
- **Jelölés**, kinek a szándéka:
  - *Fejlesztő* (kérte, vagy az ő félbemaradt munkája)
  - *AI* (magától vette észre).

## 2. Parkoló vagy issue?

A parkoló csak a nagyon kis dolgoké, amik az aktuális sessionhöz kapcsolódnak, oda
tartozhatnak: rövid emlékeztető, kérdés, apró döntés. **Issue lesz**, ha **bármelyik**
igaz:

- 200 karakterbe nem fér bele;
- bonyolultabb: több lépés, több döntés, vagy kontextus kell hozzá;
- független az aktuális sessiontől.

Issue → `/issue <szöveg>` kérdés nélkül, és itt kész.

**4 tétel a határ**. Ha az új tétellel 4-nél több lenne, `AskUserQuestion`, header:
`Issue`, kérdés: „Melyikből legyen issue?”: **Az új tétel** / **Egy parkoló tétel**. Az
új → `/issue <szöveg>`, és itt kész. Parkoló → második kérdés (header: `Melyik`), az
opciók a parkoló tételek, a `label` pontosan a tétel sora; a választottra `/issue <ID>`,
utána az új tétel parkol.

Ha nincs remote (a Kontextus **Remote** sora `NINCS`) és issue kellene: **állj meg**,
jelezd, miért nem parkolható.

## 3. Mentés

**Hova**: a checkout gyökerében lévő `.parked.md`.

A fájl formája — tételenként egy bekezdés (köztük üres sor), a végén a számláló
(ha nincs fájl, hozd létre így):

```markdown
**P01** · <tétel> — *Fejlesztő* | *AI* · <YYYY-MM-DD>

`<!-- next id: P02 -->`
```

A dátum a parkolás napja — a `/parked` ebből látja, mi parkol régóta.

A `/pick`-elt tétel az ID-je mögött `▶` jelet kap (`**P01** ▶ · <tétel> …`): a munka
lezárásáig a parkolóban marad, és a 4-es határba beleszámít.

**ID**: `P` + kétjegyű szám (`P01`, 99 fölött háromjegyű), a számláló értéke; az új
tétel a számláló elé kerül, a számláló eggyel nő. Az ID
sosem ismétlődik, a kivett tételeké sem. Kivétel: `/unpark <ID>`.

A `.parked.md`-t nem commitolod. Ha a Kontextus szerint nincs a `.gitignore`-ban
(`nem`), a létrehozásakor vedd fel egy `.parked.md` sorral (ha nincs `.gitignore`, hozd
létre), és commitold külön, csak ezt a fájlt — a többi, már stage-elt változás kimarad:

```bash
git add .gitignore
git commit -m "chore: ignore the parked list" -- .gitignore
```

Ha a Kontextus szerint már van ugyanilyen tétel, ne vedd fel újra — jelezd.

## 4. Válasz

```markdown
Parkolva:
**<ID>** · <tétel> — *Fejlesztő* | *AI*
```
