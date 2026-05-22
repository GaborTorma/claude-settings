---
description: Intent-Driven Planning Phase 4 — Apply: az utolsó elkészült Spec-fájl Plan-lépéseinek megvalósítása.
---

# Intent-Driven Planning — Apply (Phase 4)

A jóváhagyott **Spec-fájl** Plan-szakaszát megvalósítja: minden lépés a Plan saját mezői szerint fut (`Művelet` / `Failing test` / `Implementáció` / `Verify` / `Commit`), a `Megvalósítási napló` strukturált `IL-XX` bejegyzésekkel bővül a deltáknál.

## Előfeltétel

Létezik egy lezárt **Spec-fájl** (`.spec/<slug>.md` vagy `.spec/<group>/<slug>.md`) `Intent` + `Spec` + `Plan` + `Megvalósítási napló` szakaszokkal. Ha nincs ilyen, küldd a usert az `intent-driven-planning:plan` commandra.

## Kötelező háttér

**Olvasd be** a `methodology` skill `Élő dokumentum fegyelem` szakaszát — szabályai az Apply teljes futása alatt érvényesek.

## Workflow

1. **Spec-fájl meghatározása**:
   - Ha a current branch slug-ja egyezik egy `.spec/<slug>.md` / `.spec/<group>/<slug>.md` basenamejével → azt töltsd be (a `methodology` skill ekkor auto-aktiválódik).
   - Ha argumentumként útvonalat kapsz → azt töltsd be.
   - Sem branch-match, sem arg: `AskUserQuestion`-nel kérj választást a meglévő `.spec/**/*.md` fájlok közül (legutóbb módosított elöl).

2. **Branch + előfeltételek ellenőrzése**:
   - Branch egyezik a Plan `Előfeltételek.Branch` sorával? Ha nem, javasold a `git checkout -b <branch>` futtatását — **kérj user-megerősítést, ne futtasd auto**.
   - Plan `Előfeltételek` többi tétele (dep, env var, migration, fixtures, mcp): státusz röviden, eltérést jelezz.

3. **Spec-fájl első commit**:
   - Ellenőrizd, hogy a Spec-fájl már szerepel-e a branch history-ban (`git cat-file -e HEAD:<spec-path>`).
   - Ha **nincs commit** (untracked vagy unstaged), commitold **az első Plan-lépés előtt**, külön commit-ban (pl. `docs(spec): add <slug>`).

4. **Resume-pont meghatározása**:
   - Olvasd a Plan-lépés-bullet-ek `[ ]` / `[x]` állapotát (`IS-XX`, `MS-XX:IS-YY`, `MS-XX:MV-XX`, `GV-XX`) — az `[x]`-elt lépéseket kihagyod, az első `[ ]` az indulópont.
   - Multi-stage Plan: ha minden `MS-XX:IS-YY` `[x]`, de van `MS-XX:MV-XX` ami még `[ ]`, ott folytasd — ne a következő milestone-nál. (Az `MS-XX` heading-nek nincs külön checkbox-a; az állapot a benne lévő lépésekből olvasható.)
   - Ha a Plan régi sablonú (nincs checkbox), vagy az állapot inkonzisztens a commit-aktivitással / `Megvalósítási napló` bejegyzésekkel, jelezd a usernek és kérj iránymutatást.

5. **Plan-lépések végrehajtása** — minden hátralévő `IS-XX` (vagy `MS-XX:IS-YY`) lépésnél:
   1. **Implementáció** a Plan `Művelet` / `Failing test` / `Implementáció` / `Verify` mezői szerint.
   2. **Spec-jelölés**: zöld `Verify` után pipáld a lépés `[ ]` → `[x]` jelölését a Spec-fájlban — még commit előtt.
   3. **Commit** a Plan `Commit` mezője szerint — **egy commit**: a kód-változás + a `[x]` jelölés együtt.
   4. Delta esetén `IL-XX` napló-bejegyzés a `methodology` szabálya szerint.

   **Multi-stage milestone-zárás** — egy `MS-XX` **utolsó** `MS-XX:IS-YY` lépésénél a 2. és 3. pont közé beékelődik:
   - `MS-XX:IS-YY` `[x]` után futtasd le az összes `MS-XX:MV-XX` `Milestone verify` lépést (integrációs smoke, AC, regresszió).
   - Csak ha minden `MS-XX:MV-XX` zöld: pipáld mindegyiket `[x]`, és **csak ezután** mehet a commit (egy commit: utolsó IS kód + `MS-XX:IS-YY` `[x]` + minden `MS-XX:MV-XX` `[x]`). Az `MS-XX` heading-nek nincs külön checkbox-a — a milestone implicit lezárt, ha minden alá tartozó `IS` és `MV` `[x]`.
   - Piros `MS-XX:MV-XX` blokkolja a commit-ot és a következő `MS-(XX+1)` indulását.

6. **Globális verifikáció**:
   - A `Plan.Globális verifikáció` (`GV-XX`) mind zöld.

7. **Zárás-jelentés**:
   - Röviden a usernek: hány `IS-XX` ment Plan szerint, hány `IL-XX` napló-bejegyzés keletkezett, mi a végállapot.
   - A push és a release a useré.
