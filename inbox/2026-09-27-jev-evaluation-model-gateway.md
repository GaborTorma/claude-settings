---
date: 2026-09-27
source: pakkly (package-monitor)
kind: skill
---

## Mi

A TypeSafe AI Jev (`typesafe-ai/jev`) „System One" döntési modell elérhető a
Vercel AI Gateway-en: szöveg nem jön ki belőle, csak tipizált valószínűség —
osztályozásra, routingra, pontozásra és jelöltválasztásra olcsó, de
kivonatolásra nem jó, és csak AI SDK 7-ből hívható.

## Miért

A pakkly (email → rendelés pipeline) Jev-felhasználását vizsgáltuk. Tények
(gateway `/v1/models`, 2026-09-27):

```json
{ "id": "typesafe-ai/jev", "type": "evaluation", "context_window": 32000,
  "supported_specifications": ["v4"], "zdr": "none", "no_training": "all",
  "pricing": { "input": "0.000000042", "output": "0" } }
```

- Az egyetlen `type: "evaluation"` modell a gateway 391 modellje közül.
- $0,042/M input token, az output ingyenes (Haiku 4.5: $1/M, Gemini 2.5
  Flash-Lite: $0,10/M). 70–500 ms latencia (gyártói adat).
- Limit: 64 000 token/kérés, ebből 32 000 a state + a leghosszabb kérdés;
  nincs streaming.
- Kérdéstípusok: `choice` (max. 255 opció, valószínűség-eloszlás +
  confidence), `score` (rendezett szintek), `boolean` (0–1 valószínűség).
  Egy kérésben több kérdés, párhuzamosan értékelve.
- **`zdr: "none"`** — a Haiku `all`, a Gemini `some`. Érzékeny adatnál (pl.
  levéltörzs) ez döntési szempont.
- Hívás: `experimental_evaluate` az `ai` csomagból — **csak AI SDK 7-ben**
  (`ai@6`-ban nincs, `@ai-sdk/gateway@3`-ban nincs `evaluationModel`).
  `experimental_` → az API változhat.
- Fekete doboz: csak szám jön vissza, indoklás nem.

## Hogyan alkalmazd

- Jó jelölt: igen/nem kapu (pl. „rendelésről szól-e a levél?" előszűrő),
  választás ismert jelöltek közül (pl. melyik nyitott rendeléshez tartozik egy
  levél, `choice` az id-kkel + „új"), enum-besorolás, phishing-valószínűség
  mint független második jel, regexszel gyűjtött jelöltek közüli választás.
- Nem jó: szabad szöveg vagy tetszőleges érték kinyerése (tételek, összeg,
  összefoglaló) — arra LLM kell.
- Bevezetés: shadow módban (a Jev-válasz naplózódik, de nem hat), kalibráció
  a kézi javítások alapján, csak utána élesben; mindig tanácsadó, a
  determinisztikus logika felette marad.
- Hívásminta:
  ```ts
  import { experimental_evaluate } from 'ai';
  const r = await experimental_evaluate({
    model: 'typesafe-ai/jev',
    state: { subject, from, body },
    questions: {
      related: { type: 'boolean', instructions: 'Is this about a physical-goods order or parcel?' },
      order: { type: 'choice', instructions: 'Which open order does it belong to?', criteria: { /* ids + new */ } },
    },
  });
  r.answers.related.probability; r.answers.order.choice;
  ```
- Lehetséges hely: a `vercel:ai-gateway` skill modellválasztási része.
