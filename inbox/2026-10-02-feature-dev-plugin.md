---
date: 2026-10-02
source: claude-settings
kind: skill
---

# `feature-dev` plugin: amit érdemes átvenni az `intent-driven-planning`-be

## Mi

A `claude-plugins-official` piactér `feature-dev` pluginja
(<https://github.com/anthropics/claude-plugins-official/tree/main/plugins/feature-dev>)
egy 7 fázisú feature-workflow, ami nagyrészt ugyanazt fedi, mint a saját
`intent-driven-planning`. Engedélyezni nem érdemes, de három eleme hiányzik nálunk,
ezeket érdemes átvenni.

## Miért

- Letöltve, nincs engedélyezve:
  `~/.claude/plugins/marketplaces/claude-plugins-official/plugins/feature-dev`.
  Egy `/feature-dev [leírás]` command + 3 agent (`code-explorer`, `code-architect`,
  `code-reviewer`; mind `model: sonnet`, csak olvasó eszközökkel).
- Fázisok és megfelelőjük nálunk:

  | `feature-dev` fázis | Nálunk |
  | --- | --- |
  | 1. Discovery (probléma, cél, megszorítás) | `intent-driven-planning:intent` |
  | 2. Codebase Exploration: 2–3 párhuzamos `code-explorer`, mindegyik 5–10 kulcsfájlt ad vissza, utána a fő session elolvassa őket | **nincs explicit lépés** |
  | 3. Clarifying Questions: élesetek, hibakezelés, integrációs pontok, visszafelé kompatibilitás, teljesítmény — „DO NOT SKIP”, választ megvár | részben `intent` / `spec`; nincs kötelező kérdéslista |
  | 4. Architecture Design: 2–3 párhuzamos `code-architect` eltérő fókusszal (minimális változás / clean architecture / pragmatikus), ajánlással, a *Fejlesztő* választ | `plan`, de **egy** változattal |
  | 5. Implementation, csak explicit jóváhagyás után | `intent-driven-planning:apply` |
  | 6. Quality Review: 3 párhuzamos `code-reviewer` (egyszerűség/DRY · hibák · konvenciók), a *Fejlesztő* dönt: most / később / így marad | **nincs**; lásd `2026-10-02-pr-review-toolkit.md` |
  | 7. Summary | worklog (`/worklog`) |

- A `feature-dev` nem ismeri a mi keretünket: nincs Spec-fájl (`.spec/<slug>.md`),
  nincs worktree / `feat/<slug>` ág, nincs TDD-ciklus, nincs megvalósítási napló.
  Párhuzamosan engedélyezve két versengő feature-folyamat lenne.

## Hogyan alkalmazd

- A `feature-dev` plugint **ne** engedélyezd; a `/curate` döntsön, melyik elem kerül
  az `intent-driven-planning`-be (a plugin-repóban, nem a `rules/`-ban):
  1. **Exploráció az `intent` előtt vagy alatt**: 2–3 párhuzamos, olvasó, sonnetes
     szubagent eltérő szemponttal (hasonló feature-ök, architektúra, érintett terület),
     kimenetük kulcsfájl-lista; a fő session azokat elolvassa, mielőtt kérdez.
     Illeszkedik az `agents.md` modellválasztásához.
  2. **Kötelező tisztázó kérdéslista a `spec`-ben**: élesetek, hibakezelés, integrációs
     pontok, visszafelé kompatibilitás, teljesítmény — a választ meg kell várni.
  3. **2–3 alternatív megközelítés a `plan`-ben** (minimális / tiszta / pragmatikus),
     ajánlással, a *Fejlesztő* választ — a Karpathy „surface tradeoffs” elvével egyezik.
  4. **Review-lépés az `apply` végén**: párhuzamos reviewerek eltérő fókusszal, a
     megállapításokról a *Fejlesztő* dönt (most / később → `/park` / így marad).
     Ugyanaz a döntés, mint a `pr-review-toolkit` bekötése — együtt kezelendő.
- Költség: egy teljes futás 8–9 szubagent; kis feature-nél a 2–4. lépés legyen opcionális.
