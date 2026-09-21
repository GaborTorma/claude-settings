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
| `settings.user.json` | permission-szabályok | **kézzel** a `~/.claude/settings.json`-ba |

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

## Pluginok

A `torma-ai` marketplace külön repóban él: `GaborTorma/claude-plugins` (privát).
A Claude Code a git remote-ból húzza, ezért az ott végzett szerkesztés csak push
után hat — a plugin-fejlesztés loopját az a repó README-je írja le.

```bash
claude plugin marketplace add git@github.com:GaborTorma/claude-plugins.git
claude plugin marketplace update torma-ai   # kézi frissítés
```
