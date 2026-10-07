# claude-settings

Személyes Claude Code környezet: globális szabályok, slash commandok és a
`torma-ai` plugin-marketplace.

## Telepítés

```bash
make install     # symlinkek ~/.claude alá + managed settings drop-in
make update      # fast-forward pull + újratelepítés, ha a HEAD elmozdult
make push        # git push
```

## Mi hova kerül

| Repóban | Célja | Hogyan |
| --- | --- | --- |
| `rules/` | globális instrukciók, minden sessionben betöltődnek | symlink → `~/.claude/rules` |
| `CLAUDE.md` | globális user memory | symlink → `~/.claude/CLAUDE.md` |
| `commands/` | slash commandok | fájlonkénti symlink → `~/.claude/commands/` |
| `inbox/` | más sessionökből érkezett tanulságok a kurációig | nem kerül ki sehova |
| `settings.user.json` | gépfüggetlen permission-szabályok (`allow`, `deny`) | symlink → managed settings drop-in (`sudo`, lásd lent) |

## Miért managed drop-in a settings.user.json

A settings-precedencia öt szintje: managed → CLI → `.claude/settings.local.json`
(projekt) → `.claude/settings.json` (projekt) → `~/.claude/settings.json` (user).
**User-szintű `settings.local.json` nincs köztük**, a `~/.claude/settings.json`-t
pedig a Claude Code maga is írja (`enabledPlugins`, modell, `/config`) — ezért nem
symlinkeljük ide.

A managed szint `managed-settings.d/` drop-in könyvtárát a Claude Code olvassa, de
sosem írja, és a listák (`permissions.allow`, `deny`) összeadódnak a user
settings-szel. Az `install.sh` ide symlinkeli a `settings.user.json`-t:

| OS | Könyvtár |
| --- | --- |
| macOS | `/Library/Application Support/ClaudeCode/managed-settings.d/` |
| Linux, WSL | `/etc/claude-code/managed-settings.d/` |

Rendszerkönyvtár, ezért `sudo` kell; nem interaktív futásnál az `install.sh` kiírja
a két parancsot. Ellenőrzés: `/status` → `Setting sources` sorában `(drop-ins)`.

**Kockázatok**:

- Érvénytelen JSON-nal a Claude Code **el sem indul** — szerkesztés után
  `python3 -m json.tool settings.user.json`. Az `update.sh` érvénytelen remote
  állapotot nem húz le.
- Céges claude.ai-policy vagy MDM esetén a drop-in figyelmeztetés nélkül kiesik
  (`first-wins`).
- Cloud sessionökre nem hat.

A plugin-engedélyezést (`enabledPlugins`) és a marketplace-regisztrációt a
Claude Code saját állományai tartják (`~/.claude/settings.json`,
`~/.claude/plugins/known_marketplaces.json`) — ezeket nem duplikáljuk.

## Bővítés más sessionből

Ha egy másik projektben olyan tanulság születik, amit a jövőbeli sessionöknek
tudniuk kellene:

```
/capture <amit megtanultunk>
```

A command megkeresi ezt a repót a `~/.claude/rules` symlinkből, ír egy
append-only fájlt az `inbox/`-ba, commitol és pushol. A `rules/`-hoz **nem**
nyúl — az inbox tartalma egyetlen session kontextusába sem kerül be.

Amikor összegyűlt néhány bejegyzés:

```
/curate
```

Ez dönti el bejegyzésenként, hogy rule lesz belőle (ide, a `rules/`-ba), skill
(a plugin-repóba, verzió-bumppal és taggel), elvetjük, vagy halasztjuk
(`inbox/deferred/`).

A kétlépcsős mechanizmus oka a kontextus-költség: a `rules/` minden sessionbe
betöltődik, teljes egészében — oda csak az kerülhet, ami mindig igaz. A skillből
viszont csak a `description` látszik, amíg nem hívják; ott a növekedés olcsó.

## Pluginok

A `torma-ai` marketplace külön repóban él: `GaborTorma/claude-plugins` (privát).
A Claude Code a git remote-ból húzza, ezért az ott végzett szerkesztés csak push
után hat — a plugin-fejlesztés loopját az a repó README-je írja le.

```bash
claude plugin marketplace add git@github.com:GaborTorma/claude-plugins.git
claude plugin marketplace update torma-ai   # kézi frissítés
```
