---
date: 2026-09-26
source: claude-plugins
kind: skill
---

# fal.ai MCP: gyakorlati tapasztalatok az első bekötésből

Kiegészítés ehhez: `2026-09-26-ai-kepgeneralas-fal-recraft.md`.

**Mi**: a fal MCP bekötésének és első használatának buktatói. Érintett terület: auth, session-betöltés, alapértelmezett méret, promptolás.

**Miért**: az első próbánál ezek mind előjöttek.

**Hogyan alkalmazd**:

- **Üres kulcs, ami „Connected”-nek látszik.** Ha a `FAL_KEY` nincs a shell env-ben, a
  `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer $FAL_KEY"`
  parancs üres kulccsal menti el a szervert. A `claude mcp list` ettől még `✔ Connected`-et mutat, mert a kapcsolatot ellenőrzi, a kulcsot nem. Közben minden hívás, a `get_pricing` is, ezt adja:
  `{"error":{"type":"authorization_error","message":"Invalid API key"}}`
  Javítás: `claude mcp remove fal-ai --scope user`, majd újra `add` a literális kulccsal, vagy előtte `export FAL_KEY=...`.
- **Session közben hozzáadott MCP nem töltődik be.** A futó session nem látja a tooljait, a ToolSearch sem találja őket. Kerülőút, újraindítás nélkül:
  `claude -p '<feladat>' --allowedTools 'mcp__fal-ai__*' < /dev/null`
  A `< /dev/null` nélkül „no stdin data received” warningot ír.
- **Toolok (11)**: `search_models`, `recommend_model`, `get_model_schema`, `get_pricing`, `search_docs`, `upload_file`, `run_model`, `submit_job`, `check_job`, `get_job_result`, `cancel_job`.
- **Ár és méret.** A `fal-ai/flux-2` ára $0.012/MP. A 16:9 landscape preset alapértelmezésben 1024×576 px, egy kép ≈ $0.007. Hero-képhez ez kevés, ~2560 px széles kell: kérj nagyobb méretet, vagy használj upscale-t.
- **Promptolás.**
  - A FLUX.2 értelmetlen álírást rajzol a díszített tárgyakra (pl. tibeti betűk egy hangtálon). Ha nem kell szöveg: „plain, undecorated”.
  - A „szabad hely bal oldalt a szövegnek” kérést gyengén követi. Hatásosabb, ha a témát pozícionálod: „subject placed in the right third”.
- **A kép ellenőrzése.** Töltsd le, és a Read toollal nézd meg saját magad, mielőtt megmutatod a *Fejlesztő*nek. Így az artefaktumok (álírás, kompozíció) még előtte kiderülnek.
