---
date: 2026-09-30
source: workflow-sandbox
kind: rule
---

# Command Kontextus-sor: nem-nulla exit megszakítja a commandot

**Mi**: egy slash command / skill `` !`<parancs>` `` Kontextus-sora, ha a parancs nem-nulla exit
kóddal lép ki, az **egész command betöltését megszakítja** — ezért minden olyan sor, amelynek a
bukása tervezett ág, legyen bukásbiztos: `` !`<parancs> || true` ``.

**Miért**: a workflow-sandbox tesztben a `/push` remote nélkül semmit nem csinált, a „repó
létrehozása” ág soha nem futott le:

```text
Shell command failed for pattern "!`git remote get-url origin`": [stderr]
error: No such remote 'origin'
```

Ugyanez a minta 19 Kontextus-sorban volt 14 commandban (`cat .parked.md` fájl nélkül,
`gh pr view` PR nélkül, `git describe --tags` tag nélkül, `git log origin/main..HEAD` és
`gh issue list` remote nélkül). Javítva: claude-settings `5eb0928`.

**Hogyan alkalmazd** — command/skill írásakor és review-jánál:

- Ha a sor bukása egy tervezett ág (nincs remote, nincs fájl, nincs PR, nincs tag):
  `` !`<parancs> || true` ``.
- `2>&1` **nem kell**: 0-s exitnél a stderr is bekerül a Kontextusba (próba-commanddal
  ellenőrizve 2026-09-30: `cat .nincs-ilyen || true` → `cat: .nincs-ilyen: No such file or directory`).
- A command szövege a **kimenet tartalmára** ágazzon el (`No such file` → üres parkoló,
  `No such remote` → repó-létrehozás), ne az exit kódra.
- Az `allowed-tools` pontos mintáját bővítsd prefix-mintára, hogy a `|| true`-s alak is illeszkedjen:
  `Bash(cat .parked.md)` → `Bash(cat .parked.md *)`.
- Mindig 0-val kilépő sorokhoz (`git status`, `git branch --show-current`) nem kell.
