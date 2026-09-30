---
name: issue
description: Teendő felvétele GitHub issue-ként — leírásból vagy egy parkoló tétel (P-ID) átléptetésével, fix/feature címkével. Használd amikor a Fejlesztő /issue-t ír, vagy egy teendőt tartósan, a projekt backlogjába akar felvenni.
argument-hint: "leírás vagy P-ID (opcionális)"
allowed-tools: Bash(gh issue list *), Bash(gh issue create *), Bash(gh label create *), Bash(git remote get-url *), Bash(cat .parked.md *)
---

## Kontextus

- Remote: !`git remote get-url origin || true`
- Parkoló: !`cat .parked.md || true`

A `.parked.md` a rövid távú, lokális parkoló; az issue a tartós, szinkronizált teendő.
Munka nem indul — csak felvétel.

Ha nincs remote (Kontextus-hiba): **állj meg** — issue nem vehető fel; ajánld a `/park`-ot.

## 1. Mi

- **P-ID** (`P04`, `4`): a parkoló tétele — a szövegből indulsz, a végén `/unpark <ID>`.
- **Szöveg**: a *Fejlesztő* argumentuma, a szavaival.
- **Nincs argumentum**: a beszélgetésből; ha nem egyértelmű, kérdezz.

## 2. Duplikátum

```bash
gh issue list --state open --search "<kulcsszavak>" --json number,title
```

Hasonló nyitott issue → mutasd, és kérdezd meg: új legyen, vagy a meglévőhöz tartozik.

## 3. Felvétel

- **Cím**: magyar, rövid, konkrét (nem Conventional Commits prefix).
- **Body**: magyar — mi a gond vagy a cél, miért, és ha van: reprodukció, hibaüzenet szó
  szerint, érintett fájlok.
- **Címke**: `~/.claude/rules/workflow.md` útválasztása szerint — `fix` vagy `feature`.
  Ha nem egyértelmű: kérdezz.

```bash
gh label create <fix|feature> --force    # ha még nincs a repóban
gh issue create --title "<cím>" --body-file <body> --label <fix|feature>
```

P-ID-nél utána: `/unpark <ID>`.

## 4. Válasz

Csak ennyi: `Issue: [#<szám>](<URL>) · <cím> · <címke>`
