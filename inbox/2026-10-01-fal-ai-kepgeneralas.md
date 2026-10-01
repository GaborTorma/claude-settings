---
date: 2026-10-01
source: claude-settings (összevonva: 2026-09-26-ai-kepgeneralas-fal-recraft, 2026-09-26-fal-mcp-gyakorlati-tapasztalatok, rules/fal-ai.md)
kind: rule
---

# fal.ai képgenerálás (+ Recraft vektorhoz)

**Mi**: a `fal-ai` MCP szerver egy kulccsal sok képmodellt ér el (FLUX.2, Recraft, Seedream, Qwen), valamint upscale-t, háttér-eltávolítást (BiRefNet) és inpaintet. Képgeneráláshoz ez az általános eszköz. Vektoros képhez (logó, ikon, SVG, favicon-forrás) a Recraft `text-to-vector` endpointja való (`fal-ai/recraft/v4.1/text-to-vector`, `…/pro/…`), mert natív SVG-t ad; fotórealizmusban gyengébb.

**Miért**: 2026-09-26-i felmérés a korábbi projekteken. AI-képgenerátor sehol nem volt bekötve.
Hasznos lett volna ott, ahol illusztráció vagy hangulatkép kell: `varazskez/hangfurdo` hero kép nélkül, `web/estimese` mesekönyv-illusztrációk és hiányzó `og:image`.
Káros lett volna ott, ahol a képnek hitelesnek kell lennie: Fertőszentmiklós ingatlan (ott a profi fotós mellett döntöttünk), Manas/MicrOasis termék-screenshotok.

**Hogyan alkalmazd**:

- **Rule-jelölt (rövid mag)**:
  - `fal-ai` MCP képgeneráláshoz.
  - Vektoros képhez Recraft `text-to-vector`.
- **Bekötés**: hivatalos remote MCP (`https://mcp.fal.ai/mcp`, `Authorization: Bearer $FAL_KEY`, user scope).
  - **Üres kulcs, ami „Connected”-nek látszik.** Ha a `FAL_KEY` nincs a shell env-ben, a `claude mcp add --transport http fal-ai https://mcp.fal.ai/mcp --header "Authorization: Bearer $FAL_KEY"` üres kulccsal menti el a szervert. A `claude mcp list` ettől még `✔ Connected`-et mutat, mert a kapcsolatot ellenőrzi, a kulcsot nem. Közben minden hívás ezt adja: `{"error":{"type":"authorization_error","message":"Invalid API key"}}`. Javítás: `claude mcp remove fal-ai --scope user`, majd újra `add` a literális kulccsal, vagy előtte `export FAL_KEY=...`.
  - **Session közben hozzáadott MCP nem töltődik be.** A futó session nem látja a tooljait, a ToolSearch sem találja őket. Kerülőút: `claude -p '<feladat>' --allowedTools 'mcp__fal-ai__*' < /dev/null`. A `< /dev/null` nélkül „no stdin data received” warningot ír.
- **Ár és méret**: ~$0.02–0.09/kép. A `fal-ai/flux-2` ára $0.012/MP. A 16:9 landscape preset alapértelmezésben 1024×576 px, egy kép ≈ $0.007. Hero-képhez ez kevés, ~2560 px széles kell: kérj nagyobb méretet, vagy használj upscale-t. Költés előtt `get_pricing`.
- **Promptolás**:
  - A FLUX.2 értelmetlen álírást rajzol a díszített tárgyakra (pl. tibeti betűk egy hangtálon). Ha nem kell szöveg: „plain, undecorated”.
  - A „szabad hely bal oldalt a szövegnek” kérést gyengén követi. Hatásosabb, ha a témát pozícionálod: „subject placed in the right third”.
- **Ellenőrzés**: a képet töltsd le, és a Read toollal nézd meg saját magad, mielőtt megmutatod a *Fejlesztő*nek.
- **Szabályok**:
  - AI-kép illusztrációhoz és hangulathoz igen. Hiteles tartalomhoz (ingatlan, termék-UI, valós személy) nem.
  - A generált asset WebP-ként kerüljön a repóba, mellé mentve a prompt és a modell neve (reprodukálhatóság).
  - Az OG-kép kódból készüljön (`next/og`), a favicon-készlet forrásképből `sharp` scripttel — ezekhez ne AI-t használj.
- **Runtime** (*User*-oldali) képgenerálás: Vercel AI Gateway (AI SDK `generateImage`), nem MCP; fejlesztés közbeni asset-gyártáshoz nem való.
- **Midjourney**: nincs hivatalos API, és a ToS tiltja az automatizált hozzáférést — ne használd.
- **Hivatalos skillek**: [fal-ai-community/skills](https://github.com/fal-ai-community/skills) (model-routing, fal-prompting, commercial, marketing, fal-redesign, …). A futtatáshoz a `genmedia` CLI-t feltételezik, nem az MCP-t — saját skillnél ezekből a routing/prompting tudás átvehető.
