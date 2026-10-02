---
date: 2026-10-02
source: claude-settings
kind: skill
---

# PR-review lépés: `pr-review-toolkit` célzottan, a `/code-review` mellé

## Mi

A PR-folyamatban (`/commit-push-pr`, `/commit-push-pr-merge`, `/merge-pr`) most nincs
kódreview. A `claude-plugins-official` piactér `pr-review-toolkit` pluginja
(`/review-pr [aspects]` + 6 agent) ezt pótolhatja, de csak célzottan, a beépített
`/code-review` és `/simplify` mellett.

## Miért

- Állapot 2026-10-02-án: a `merge-pr.md` csak akkor áll meg, ha a GitHub kötelező
  review-t kér; a saját commandok semmilyen review-t nem futtatnak. Kézzel elérhető:
  `/code-review` (hibák a diffben, `--comment`-tel PR-kommentként), `/simplify`.
- A plugin letöltve, de nincs engedélyezve:
  `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/pr-review-toolkit`.
- Agentjei és az átfedés:

  | Agent | Átfedés |
  | --- | --- |
  | `code-reviewer` (`model: opus`) | ≈ `/code-review` |
  | `code-simplifier` | ≈ `/simplify` |
  | `silent-failure-hunter` | **új**: elnyelt hiba, rossz fallback, hiányzó log |
  | `pr-test-analyzer` | **új**: tesztlefedettség-rések, élesetek |
  | `type-design-analyzer` | **új**: TS-típusok invariánsai (1–10 pontozás) |
  | `comment-analyzer` | **új**: elavult, félrevezető komment |

- Kockázat:
  - Teljes futás = több párhuzamos agent → drága.
  - Az agentek `description`-je „proactively” indulást ír elő: engedélyezve kérés
    nélkül is elindulhatnak munka közben (költség, és ütközik a `focus.md`-vel).
- Lokálisan, a branch diffjén fut (`git diff`), nem a GitHub PR-en: a PR nyitása előtt
  is használható.

## Hogyan alkalmazd

- A *Fejlesztő* még nem döntött; opciók:
  1. Engedélyezés + bekötés: a `/commit-push-pr(-merge)` a PR előtt
     `/review-pr errors tests types comments` + `/code-review`; a duplikáló
     `code`/`simplify` aspektus kimarad.
  2. Csak engedélyezés, kézi `/review-pr`.
  3. Nem kell, maradnak a beépítettek.
- Engedélyezésnél kezelni kell a proaktív indulást (pl. az agentek kizárása az
  automatikus használatból, vagy csak a command használata) — a plugin magától nem tiltja.
- Kapcsolódik: `2026-09-29-ci-pr-gate.md` (CI mint merge-feltétel) — a review ugyanazon
  a ponton lenne gate.
