---
name: park
description: Új tétel felvétele a projekt .parked.md parkolójába. Használd amikor a Fejlesztő /park-ot ír, vagy menet közben egy témát parkolni kell (→ focus.md).
argument-hint: "a parkolandó téma (opcionális)"
allowed-tools: Bash(cat .parked.md *), Bash(grep *), Bash(git rev-parse *), Bash(dirname *), Bash(git remote get-url *), Write(.parked.md), Edit(.parked.md), Write(.gitignore), Edit(.gitignore), Bash(git add .gitignore), Bash(git commit *), Skill(issue *)
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
- **Jelölés**, kinek a szándéka:
  - *Fejlesztő* (kérte, vagy az ő félbemaradt munkája)
  - *AI* (magától vette észre).

## 2. Parkoló vagy issue?

Issue-jellegű, ha **mind** igaz: tartós projektmunka (bug, feature, technikai adósság,
ami napok múlva is aktuális), önállóan elvégezhető (nem a mostani munka kérdése vagy
mellékszála), és van remote (a Kontextus **Remote** sora nem `NINCS`).

- **Egyértelműen issue-jellegű** → `AskUserQuestion`, header: `Hova`: **Issue**
  (`description`: `Javasolt — …`) / **Parkoló**. Issue → `/issue <szöveg>`, és itt kész.
- **Egyébként** (döntés, kérdés, rövid emlékeztető, bizonytalan ötlet, nincs remote) →
  kérdés nélkül parkol.

## 3. Mentés

**Hova**: a checkout gyökerében lévő `.parked.md`. Worktree-ben (a `git rev-parse
--show-toplevel` nem a fő checkout: `dirname "$(git rev-parse --path-format=absolute
--git-common-dir)"`) kérdezd meg `AskUserQuestion`-nel: a worktree-é vagy a fő checkouté
legyen. A worktree tételeiről a `/worktree-close` kérdez.

A fájl formája — tételenként egy bekezdés (köztük üres sor), a végén a számláló
(ha nincs fájl, hozd létre így):

```markdown
**P01** · <tétel> — *Fejlesztő* | *AI* · <YYYY-MM-DD>

`<!-- next id: P02 -->`
```

A dátum a parkolás napja — a `/parked` ebből látja, mi parkol régóta.

**ID**: `P` + kétjegyű szám (`P01`, 99 fölött háromjegyű), a számláló értéke; az új
tétel a számláló elé kerül, a számláló eggyel nő. Az ID
sosem ismétlődik, a kivett tételeké sem. A számláló mindig a **fő checkout** fájljában
él — worktree-be parkolásnál is onnan veszed és ott növeled, így az ID-k egyediek.
Kivétel: `/unpark <ID>`.

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
