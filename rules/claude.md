# CLAUDE.md karbantartás

- **Nincs** `CLAUDE.md` → hozd létre (`/init`), új projektnél a bootstrap része.
- **Van** → tartsd frissen: dokumentált tény (parancs, struktúra, konvenció, stack, env) változásakor ugyanabban a körben, surgical — csak az érintett sort.
- **Több részből álló** projekt (monorepo, `apps/*`, `packages/*`, külön frontend/backend) → minden önálló alrész kapjon **saját** `CLAUDE.md`-t, csak a rá jellemző infóval; a root nem ismétli.
- **Tartalom**: használt build/test/lint/run parancs, magas szintű architektúra, nem nyilvánvaló konvenciók, tanulságok, tapasztalatok — tömören.
- **Audit/frissítés**: `claude-md-management` skill (`claude-md-improver`, `revise-claude-md`).
