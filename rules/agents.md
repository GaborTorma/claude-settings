# Szubagentek

Szubagent = külön kontextusban futó *AI*-munkás; a fő session csak a záró
reportját látja. **Delegálj, ha a konklúzió kell, nem a nyersanyag.**

- **Használd**: sok fájlon átívelő keresés, zajos exploráció (hosszú log, sok
  találatos grep), független párhuzamos feladatok — egy üzenetben indítva.
- **Ne használd**: egyetlen ismert fájl/tény, kis lokális edit. Amit már
  delegáltál, ne futtasd le te is; futó agent eredményét ne találd ki.
- **Keretek**: pár agent, ne tucat — mindegyik teljes session-költséggel fut. A
  prompt álljon meg magában (fájlutak, elvárt output). A záró reportot a
  *Fejlesztő* nem látja, a lényeget told tovább.

## Modell a feladathoz, nem a sessionhöz

Ha a fő session `opus`/`fable`, egy mechanikus keresés akkor is mehet olcsóbban.

| Feladat | Modell |
| --- | --- |
| Mechanikus: fájl-lista, grep-összesítés, formátum-konverzió | `haiku` |
| Kutatás, kódkeresés, rutin implementáció, teszt-írás | `sonnet` |
| Architektúra, nehéz debug, kockázatos refaktor, security review | `opus` / `fable` |

**Precedencia**: `Agent` tool `model` paramétere → agent-definíció frontmatter
`model:` → default subagent model → szülő session modellje.

**Kivétel**: `subagent_type: "fork"` mindig a szülő modelljén fut.
