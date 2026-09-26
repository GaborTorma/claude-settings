# claude-settings

Személyes Claude Code környezet: globális szabályok, slash commandok és a
`torma-ai` plugin-marketplace.

## Telepítés

```bash
make install     # symlinkek ~/.claude alá + shell rc auto-sync hook
make link        # ugyanaz, a shell rc érintése nélkül
make update      # sync + újratelepítés, ha a HEAD elmozdult
```

## Mi hova kerül

| Repóban | Célja | Hogyan |
| --- | --- | --- |
| `rules/` | globális instrukciók, minden sessionben betöltődnek | symlink → `~/.claude/rules` |
| `CLAUDE.md` | globális user memory | symlink → `~/.claude/CLAUDE.md` |
| `commands/` | slash commandok | fájlonkénti symlink → `~/.claude/commands/` |
| `inbox/` | más sessionökből érkezett tanulságok a kurációig | nem kerül ki sehova |
| `settings.user.json` | permission-szabályok, `additionalDirectories` (claude-settings, claude-plugins) | **kézzel** a `~/.claude/settings.json`-ba |

## Miért kézi a settings.user.json

A settings-precedencia öt szintje: managed → CLI → `.claude/settings.local.json`
(projekt) → `.claude/settings.json` (projekt) → `~/.claude/settings.json` (user).
**User-szintű `settings.local.json` nincs köztük.** A `~/.claude/settings.local.json`
csak akkor számít, ha a Claude Code-ot magából a home-könyvtárból indítod — ott
az `.claude/settings.local.json` a *projekt*-local fájl. Minden más projektben az
oda symlinkelt szabályok nem hatnak.

A `permissions` helye ezért a user settings, amit a Claude Code maga is ír — nem
symlinkeljük ide. A `settings.user.json` a verziózott forrás, a tartalmát kézzel
kell bemásolni; az `install.sh` figyelmeztet, ha hiányzik.

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
