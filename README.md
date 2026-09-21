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

## Plugin-fejlesztés

A `torma-ai` marketplace `directory` source-ként van regisztrálva
(`~/.claude/local-plugins`), de a Claude Code a pluginokat **verzió-mappába
másolja** (`~/.claude/plugins/cache/torma-ai/<plugin>/<verzió>`) — a repóban
végzett szerkesztés nem hat, amíg a `plugin.json` verziója nem változik.

Bump nélküli teszteléshez indítsd a sessiont a plugin könyvtárával:

```bash
claude --plugin-dir plugins/apple
```

Kiadás után a cache frissítése:

```bash
claude plugin marketplace update torma-ai
claude plugin update <plugin>@torma-ai
```

A `claude plugin tag` `{name}--v{version}` alakú git taget készít, és ellenőrzi,
hogy a `plugin.json` és a marketplace-bejegyzés verziója egyezik.
