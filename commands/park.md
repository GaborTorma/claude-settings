---
name: park
description: Új tétel felvétele a projekt .parked.md parkolójába. Használd amikor a Fejlesztő /park-ot ír, vagy menet közben egy témát parkolni kell (→ focus.md).
argument-hint: "a parkolandó téma (opcionális)"
allowed-tools: Bash(cat .parked.md), Bash(git rev-parse *), Write(.parked.md), Edit(.parked.md)
---

## Kontextus

- Parkoló: !`cat .parked.md`

## 1. A tétel

- **Szöveg**: a *Fejlesztő* argumentuma, a szavaival; ha nincs, a beszélgetésből a
  legutóbb félretett téma. Ha nem egyértelmű, melyik: kérdezz rá.
- **Egy sor**, később is érthetően: mi a téma, és ha kell, mi van vele hátra.
- **Jelölés**, kinek a szándéka:
  - *Fejlesztő* (kérte, vagy az ő félbemaradt munkája)
  - *AI* (magától vette észre).

## 2. Mentés

**Hova**: a checkout gyökerében lévő `.parked.md`. Worktree-ben (a `git rev-parse
--show-toplevel` nem a fő checkout: `dirname "$(git rev-parse --path-format=absolute
--git-common-dir)"`) kérdezd meg `AskUserQuestion`-nel: a worktree-é vagy a fő checkouté
legyen. A worktree tételeiről a `/worktree-close` kérdez.

A fájl formája — tételenként egy bekezdés (köztük üres sor), a végén a számláló
(ha nincs fájl, hozd létre így):

```markdown
**P01** · <tétel> — *Fejlesztő* | *AI*

`<!-- next id: P02 -->`
```

**ID**: `P` + kétjegyű szám (`P01`, 99 fölött háromjegyű), a számláló értéke; az új
tétel a számláló elé kerül, a számláló eggyel nő. Az ID
sosem ismétlődik, a kivett tételeké sem. A számláló mindig a **fő checkout** fájljában
él — worktree-be parkolásnál is onnan veszed és ott növeled, így az ID-k egyediek.
Kivétel: `/unpark <ID>`.

A fájl globálisan gitignored (`~/.config/git/ignore`), nem commitolod. Ha a Kontextus
szerint már van ugyanilyen tétel, ne vedd fel újra — jelezd.

## 3. Válasz

```markdown
Parkolva:
**<ID>** · <tétel> — *Fejlesztő* | *AI*
```
