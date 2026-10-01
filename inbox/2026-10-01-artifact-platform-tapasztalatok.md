---
date: 2026-10-01
source: git-graph
kind: skill
---

# Artifact platform — mért tapasztalatok

**Mi**: az Artifact runtime képességeiről több, a doksiból nem nyilvánvaló, de
mérve igaz tény — főleg arról, hogyan ér el egy lap egy futó Claude Code
sessiont, és mi kell az élő, gépen futó adathoz.

**Miért**: a git-graph élő Artifactjánál és a „lap kér, a Claude végrehajt”
ötletnél ezek döntötték el a tervet; elsőre két ponton is rossz feltevésből
indultam (a `sample`-t a sessionnek hittem, és sessionönkénti újrapublikálást
terveztem a figyelés miatt). Részletek, számokkal:
`git-graph/docs/artifact-findings.md`.

**Hogyan alkalmazd** — ha egy Artifact-lapnak a sessionnel vagy a géppel kell
beszélnie:

## A lapról a sessionbe (2026-10-01, Claude Code 2.1.285)

- **`sample` ≠ session.** Állapot nélküli modellhívás, a sessionről, repóról
  semmit nem tud. Session felé a `comments.sendToClaude({anchor, text})` az út
  (`capabilities: {comments: {}}`).
- **Annak a sessionnek megy, amelyiknek a paneljén a lap nyitva van** — nem
  minden figyelőnek. Két session ugyanazon a lapon: mindkettő csak a saját
  paneljén nyomott gombot kapta.
- **Figyelés (`ArtifactComments watch`) nem kell hozzá** — a figyelés
  lekapcsolása után is megérkezett. Elég, ha a session megnyitja a lapot.
- A session „Artifact comment sent to Claude” üzenetet kap; a szálban válaszol
  (`reply`) és lezárja (`resolve`). A kérés kommentszálként megmarad.
- **Hozzájárulás**: az app Artifactonként egyszer kérdez; másik sessionben és
  app-újraindítás után sem kérdez újra.
- Gombot csak `canSendToClaude() === "available"` mellett mutass.
- A szöveget a session megbízhatatlan adatként kapja → kérésként kezeli,
  megerősítést kér. Romboló műveletnél ez kívánt.

## Figyelés felfegyverzése (auto-replies armed)

- Felfegyverez: a session **maga publikálja** az Artifactot, vagy `watch` egy
  olyan linkre, amit a **Fejlesztő a saját üzenetében** adott.
- **Nem** fegyverez fel: `watch` hookból / tool-kimenetből kapott linkre —
  szó szerint: *„auto-replies arm only for an artifact whose link the user gave
  in their own message”*. (A panelről küldött `sendToClaude`-ot ez nem érinti.)

## Gépen futó adat a lapon (`host:` híd, 2026-09-30)

- A `host:<név>` MCP csak a **Claude app configjában**
  (`claude_desktop_config.json`) felvett szerverrel megy, a `claude mcp add`-os
  nem látszik. Az app futás közben felülírja a configot → beírás után azonnal
  újraindítás.
- A lapnak deklarálnia kell az `mcp` capability-t a tool-listával; enélkül
  `use("mcp")` → `null`. Új tool → manifest bővítés + újrapublikálás.
- `readOnlyHint: true` a toolokon, különben hívásonként megerősítést kérhet.
- `watchTool` pollozása ~30 s-ra padlózik → gyorsabb élő frissítéshez
  `callTool` saját időzítővel (2 s-os olcsó ujjlenyomat, változáskor teljes adat).
- Csak az appban, a tulajdonosnak működik; böngészőben `server_not_connected`.

## Headless publikálás (`claude -p`)

- `-p`-ben az Artifact tool alapból ki: `CLAUDE_CODE_ARTIFACT=1` kell (Desktop
  sessionből öröklődik, launchd alól nem).
- A tool egy org-policy lekérdezés után kapcsol be, gyakran az első init után →
  `--input-format stream-json`, hiányzó toolnál újrakérdezés ugyanabban a
  folyamatban.
- Adatot ne ágyazz a lapba: nagy lap frissítése ~50 s volt, vékony lapé ~6 s.
