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
| `plugins/` | a `torma-ai` marketplace | symlink → `~/.claude/local-plugins` |
| `settings.user.json` | permission-szabályok | **kézzel** a `~/.claude/settings.json`-ba |

## Miért kézi a settings.user.json

A settings-precedencia öt szintje: managed → CLI → `.claude/settings.local.json`
(projekt) → `.claude/settings.json` (projekt) → `~/.claude/settings.json` (user).
**`~/.claude/settings.local.json` nincs köztük**, ezért az oda symlinkelt
szabályok soha nem hatnak. A `permissions` blokk helye a user settings, amit a
Claude Code maga is ír — ezért nem symlinkeljük ide, hanem a
`settings.user.json` a verziózott forrás, és a tartalmát kézzel kell bemásolni.
Az `install.sh` figyelmeztet, ha hiányzik.

A plugin-engedélyezést (`enabledPlugins`) és a marketplace-regisztrációt a
Claude Code saját állományai tartják (`~/.claude/settings.json`,
`~/.claude/plugins/known_marketplaces.json`) — ezeket nem duplikáljuk.
