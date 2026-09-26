---
date: 2026-09-26
source: claude-plugins
kind: skill
---

# AI képgenerálás webdesignhoz: fal.ai + Recraft

**Mi**: webdesign-assethez a fal.ai MCP az általános eszköz, vektoros logóhoz/ikonhoz a Recraft MCP; runtime (*User*-oldali) képgenerálás a Vercel AI Gateway-en át megy.

**Miért**: 2026-09-26-i felmérés a korábbi projekteken. AI-képgenerátor sehol nem volt bekötve.
Hasznos lett volna ott, ahol illusztráció vagy hangulatkép kell: `varazskez/hangfurdo` hero kép nélkül, `web/estimese` mesekönyv-illusztrációk és hiányzó `og:image`.
Káros lett volna ott, ahol a képnek hitelesnek kell lennie: Fertőszentmiklós ingatlan (ott a profi fotós mellett döntöttünk), Manas/MicrOasis termék-screenshotok.

**Hogyan alkalmazd**:

- **fal.ai**: hivatalos remote MCP (`https://mcp.fal.ai/mcp`, Bearer `FAL_KEY`, user scope). Egy kulccsal elérhető a FLUX.2, Recraft, Seedream és Qwen, valamint háttér-eltávolítás (BiRefNet), upscale és inpaint. Ár: ~$0.02–0.09/kép.
- **Recraft**: hivatalos remote MCP (`https://mcp.recraft.ai/mcp`, OAuth). Natív SVG, brand style, vectorize. Logóhoz, ikonhoz és favicon-forráshoz; fotórealizmusban gyengébb.
- **Vercel AI Gateway**: csak runtime funkcióhoz (AI SDK `generateImage`). Nem MCP, fejlesztés közbeni asset-gyártáshoz nem való.
- **Szabályok**:
  - AI-kép illusztrációhoz és hangulathoz igen. Hiteles tartalomhoz (ingatlan, termék-UI, valós személy) nem.
  - A generált asset WebP-ként kerüljön a repóba, mellé mentve a prompt és a modell neve (reprodukálhatóság).
  - Az OG-kép kódból készüljön (`next/og`), a favicon-készlet forrásképből `sharp` scripttel — ezekhez ne AI-t használj.
- **Midjourney**: nincs hivatalos API, és a ToS tiltja az automatizált hozzáférést — ne használd.
