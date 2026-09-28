---
name: commit-push-pr-merge-deploy
description: Commit + push + PR + merge a mainbe + kiadás (release, deploy) egy menetben. Használd amikor a Fejlesztő /commit-push-pr-merge-deploy-t ír, vagy egy kész branch munkáját azonnal élesíteni akarja.
argument-hint: "PR cím vagy kontextus (opcionális)"
---

A `/commit-push-pr-merge` folyamata, utána kiadás (`/release`) a friss `main`-ről.
A command meghívása maga a deploy-engedély — de csak akkor, ha az előző lépések
hibátlanul lefutottak.

## 1. Merge

`/commit-push-pr-merge` (a *Fejlesztő* argumentumát add át `args`-ként).

Ha bármelyik lépése megállt (elbukott gate, nem mergelhető PR), **itt is állj
meg** — deploy nincs.

## 2. Kiadás

`/release`. Ha elbukik, **állj meg**: a merge
már a `main`-en van, de élesítés és tag nincs — javítás után újra `/release`.

Végül írd ki: PR szám + URL, merge SHA, kiadott verzió, deploy URL, GitHub Release URL.

Minden lépés után azonnal írd ki annak a válaszát, a lépés saját formájában.
Más köztes szöveg nincs.
