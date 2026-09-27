---
date: 2026-09-27
source: pakkly (package-monitor)
kind: skill
---

## Mi

Vercel AI Gateway-en a thinking-szintet a top-level `reasoning` opcióval,
modellenként kell beállítani; provider-specifikus reasoning-opció
(`providerOptions.openai.reasoningEffort` stb.) minden providerre átszivárog.

## Miért

A pakkly `providerOptions()` providerenként kapcsolta ki a thinkinget
(`openai: { reasoningEffort: 'minimal' }`, `google: { thinkingConfig:
{ thinkingBudget: 0 } }`, `anthropic: { thinking: { type: 'disabled' } }`).
Az AI SDK 7 top-level `reasoning` opciójára cserélve mérés (reasoning token,
kimeneti token, idő) mutatta:

| modell | régi blokkok | `'none'` | `'minimal'` | `'none'` + `openai.reasoningEffort: 'minimal'` |
|---|---|---|---|---|
| gemini-2.5-flash-lite | 0 | 0 | 362 | 362 |
| claude-haiku-4.5 | 0 | 0 | 437 (26 s) | 673 |
| claude-sonnet-5 | 0 | 0 | 0 | 0 |
| gpt-5-nano | 0 | HIBA | 0 | 0 |

- A `'minimal'` a Geminin és a Haikun **bekapcsolja** a thinkinget.
- Az `openai.reasoningEffort` a gateway-en minden providerre érvényes; a régi
  kód csak azért működött, mert a Google- és Anthropic-blokk a saját
  modelljein felülírta.
- A régi `gpt-5` család elutasítja a `'none'`-t, a `gpt-5.2+` a `'minimal'`-t:
  `Unsupported value: 'none' is not supported with the 'gpt-5-2025-08-07' model. Supported values are: 'minimal', …`
  `Unsupported value: 'minimal' is not supported with the 'gpt-5.2-2025-12-11' model. Supported values are: 'none …`
  A régi kód tehát a mostani OpenAI-modelleken már hibás volt.
- Elutasítja a `'none'`-t: `openai/gpt-5`, `-mini`, `-nano`, `-fast`,
  `gpt-5-codex`, `gpt-5.1-codex-mini`. Elfogadja: `gpt-5.2`, `gpt-5.4-nano`,
  `gpt-5.6-luna`.

A gateway (`@ai-sdk/gateway` 4) a hívási opciókat változatlanul továbbküldi,
a providerenkénti leképezés szerver oldalon történik — kódból nem
ellenőrizhető, csak méréssel.

## Hogyan alkalmazd

- Thinking kikapcsolása: `reasoning: 'none'` minden modellre, kivétel a régi
  `gpt-5` család: `/^openai\/gpt-5(-mini|-nano)?(-fast)?$/` → `'minimal'`.
- Reasoning-jellegű `providerOptions` blokkot ne használj gateway mellett.
- Ellenőrzés: `usage.outputTokenDetails.reasoningTokens` és a kimeneti
  tokenszám, modellenként egy hívással — ne a docs alapján feltételezd.
- Referencia-implementáció: pakkly `packages/core/src/llm/extract.ts`
  `reasoning()` (commit `b0f94c6`).
- Lehetséges hely: a `vercel:ai-gateway` skill kiegészítése.
