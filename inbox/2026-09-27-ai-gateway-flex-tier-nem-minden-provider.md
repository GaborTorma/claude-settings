---
date: 2026-09-27
source: pakkly (package-monitor)
kind: skill
---

## Mi

Az AI Gateway `providerOptions.gateway.serviceTier: 'flex'` beállítása
csak egyes providereknél érvényesül (Google, OpenAI) — Anthropic-modelleknél
csendben standard tier-en fut; a ténylegesen alkalmazott tier a
`providerMetadata.gateway.serviceTier`-ből olvasható ki.

## Miért

A pakkly `LLM_SERVICE_TIER=flex`-szel futott, feltételezve, hogy minden
hívás olcsóbb (és lassabb, mert sorban állhat). A *Fejlesztő* a Haiku
lassúságára panaszkodott; a gyanú a flex-sorban állás volt. Mérés:

| modell | `providerMetadata.gateway.serviceTier` |
|---|---|
| google/gemini-2.5-flash-lite | `flex` |
| openai/gpt-5-nano, gpt-5.2, gpt-5.4-nano | `flex` |
| anthropic/claude-haiku-4.5, claude-sonnet-5 | `undefined` (standard) |
| openai/gpt-5.6-luna | `undefined` |

A Haiku lassúságát tehát nem a flex okozta — és az Anthropic-hívásokra a
flex-kedvezmény sem járt. Hiba vagy figyelmeztetés nincs, a beállítás
egyszerűen nem hat.

## Hogyan alkalmazd

- Flex/priority tier bevezetésekor modellenként ellenőrizd:
  `console.log(result.providerMetadata?.gateway?.serviceTier)` — `'flex'` /
  `'priority'`, ha érvényesült, `undefined`, ha nem.
- Költségbecslésnél a flex-kedvezményt csak az ellenőrzött modellekre számold.
- Latencia-hibakeresésnél a tier nem magyarázat olyan modellre, amelyiknél
  `undefined`.
- Lehetséges hely: a `vercel:ai-gateway` skill kiegészítése.
