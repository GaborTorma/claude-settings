---
date: 2026-10-02
source: git-graph
kind: rule
---

# Félkész munka parkolása `git stash`-sel a `dev` ágon

**Mi**: ha a fő checkoutban (`dev`, Fix-jellegű munka) félkész, commitolatlan
változás van, és új téma szorítja ki (focus.md → „Váltunk”), a félkész munka
**névvel ellátott stash**-be megy, és a `.parked.md` tétele hivatkozik rá.

**Miért**: a focus.md „Váltunk” ága ma azt mondja, hogy „a nyitott munka
commitolva vagy saját ágon marad”. Feature-munkánál ez magától igaz (a
worktree megtartja), a `dev`-en viszont nincs saját ág, és egy fél kész
„WIP” commit a `dev`-en szemetet visz a `main`-be (a `/commit-push-merge`
ff-only viszi át). A stash pont erre való: tiszta munkafát ad history nélkül.
Kockázatai miatt viszont szabály kell hozzá:

- **láthatatlan** — a `git status` nem mutatja, könnyű elfelejteni (a
  git-graph ezért kapott stash-megjelenítési issue-t: GaborTorma/git-graph#22);
- **csak lokális** — nem pusholódik, gépváltáskor vagy klón-törléskor elvész;
- **verem, nem név** — a `stash@{0}` index elcsúszik minden új stash-sel;
- **követetlen fájl** alapból kimarad (`-u` nélkül), és a `pop` ütközhet.

**Hogyan alkalmazd**:

1. Csak a fő checkoutban, `dev`-en, rövid félbehagyásra. Feature-ágon /
   worktree-ben nem kell (a worktree megtartja); napoknál hosszabb parkolásra
   inkább `wip/<slug>` ág + push.
2. Parkolás:
   ```bash
   git stash push -u -m "P<ID>: <téma röviden>"
   ```
   és a `/park` tétel szövegébe: `stash: "P<ID>: <téma>"`.
3. Folytatás (`/pick P<ID>`): a stash-t **üzenet alapján** keresd, ne
   indexszel:
   ```bash
   git stash list --format='%gd %s' | grep 'P<ID>:'
   git stash pop <a talált stash@{n}>
   ```
   Ütközésnél a stash megmarad (`pop` nem dobja el) — feloldás után
   `git stash drop <ref>`, a *Fejlesztő* jóváhagyásával (a drop
   visszafordíthatatlan).
4. A `/parked` és a session eleji ellenőrzés jelezze, ha van stash
   (`git stash list` nem üres), különösen P-ID nélküli stash-t — az
   elfelejtett munka.
5. A `dev` `ff-only` utolérése (`git merge --ff-only origin/main`) előtt a
   stash-elt munka nem akadály: tiszta munkafán fut.

Megfontolandó a `/curate`-nek: a focus.md „Váltunk” sorának kiegészítése, és a
`/park` / `/pick` / `/parked` skillekbe a stash-lépés.
