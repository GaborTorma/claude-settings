---
description: Intent-Driven Planning Phase 4 — Apply: az utolsó elkészült Spec-fájl Plan-lépéseinek megvalósítása.
---

# Intent-Driven Planning — Apply (Phase 4)

A jóváhagyott **Spec-fájl** Plan-szakaszát megvalósítja: minden lépés a Plan saját mezői szerint fut (`Művelet` / `Failing test` / `Implementáció` / `Verify` / `Commit`), a `Megvalósítási napló` strukturált `IL-XX` bejegyzésekkel bővül a deltáknál.

## Előfeltétel

Létezik egy lezárt **Spec-fájl** (`.spec/<slug>.md` vagy `.spec/<group>/<slug>.md`) `Intent` + `Spec` + `Plan` + `Megvalósítási napló` szakaszokkal. Ha nincs ilyen, küldd a Fejlesztőt az `intent-driven-planning:plan` commandra.

## Kötelező háttér

**Olvasd be** a `methodology` skill `Élő dokumentum fegyelem` szakaszát — szabályai az Apply teljes futása alatt érvényesek.

## Workflow

1. **Spec-fájl meghatározása**:
   - Ha a current branch slug-ja egyezik egy `.spec/<slug>.md` / `.spec/<group>/<slug>.md` basenamejével → azt töltsd be (a `methodology` skill ekkor auto-aktiválódik).
   - Ha argumentumként útvonalat kapsz → azt töltsd be.
   - Sem branch-match, sem arg: `AskUserQuestion`-nel kérj választást a meglévő `.spec/**/*.md` fájlok közül (legutóbb módosított elöl).

2. **Branch + előfeltételek ellenőrzése**:
   - Branch egyezik a Plan `Előfeltételek.Branch` sorával? Ha nem, javasold a `git checkout -b <branch>` futtatását — **kérj Fejlesztő-megerősítést, ne futtasd auto**.
   - Plan `Előfeltételek` többi tétele (dep, env var, migration, fixtures, mcp): státusz röviden, eltérést jelezz.

3. **Spec-fájl első commit**:
   - Ellenőrizd, hogy a Spec-fájl már szerepel-e a branch history-ban (`git cat-file -e HEAD:<spec-path>`).
   - Ha **nincs commit** (untracked vagy unstaged), commitold **az első Plan-lépés előtt**, külön commit-ban (pl. `docs(spec): add <slug>`).

4. **Resume-pont meghatározása**:
   - Olvasd a Plan-lépés-bullet-ek `[ ]` / `[x]` állapotát (`IS-XX`, `MS-XX:IS-YY`, `MS-XX:MV-XX`, `GV-XX`) — az `[x]`-elt lépéseket kihagyod, az első `[ ]` az indulópont.
   - Multi-stage Plan: ha minden `MS-XX:IS-YY` `[x]`, de van `MS-XX:MV-XX` ami még `[ ]`, ott folytasd — ne a következő milestone-nál. (Az `MS-XX` heading-nek nincs külön checkbox-a; az állapot a benne lévő lépésekből olvasható.)
   - Ha a Plan régi sablonú (nincs checkbox), vagy az állapot inkonzisztens a commit-aktivitással / `Megvalósítási napló` bejegyzésekkel, jelezd a Fejlesztőnek és kérj iránymutatást.

5. **Plan-lépések végrehajtása** — minden hátralévő `IS-XX` (vagy `MS-XX:IS-YY`) lépésnél:
   1. **Implementáció** a Plan `Művelet` / `Failing test` / `Implementáció` / `Verify` mezői szerint.
   2. **Spec-jelölés**: azonnal, amint a lépés **saját** `Verify`-ja zöld: `[ ]` → `[x]`.
   3. Delta esetén `IL-XX` napló-bejegyzés a `methodology` szabálya szerint.

   **Multi-stage milestone-zárás** — egy `MS-XX` **utolsó** `MS-XX:IS-YY` lépésénél, miután az utolsó IS `[x]`-ed:
   - Futtasd le az összes `MS-XX:MV-XX` `Milestone verify` lépést.
   - Csak ha minden `MS-XX:MV-XX` zöld: pipáld mindegyiket `[x]`.
   - **Töltsd ki a `Milestone summary` blokkot** a Plan placeholder-skeletonja szerint, valós tartalommal: a milestone eredménye 1-2 mondatban, logikai területenként egy sor a kiváltó `MS-XX:IS-YY` lépés(ek)re és az érintett fájl(ok)ra mutató linkkel, `Teljesült` AC-lista az `MS-XX:MV-XX` referenciájával, `Delták` a keletkezett `IL-XX`-ekkel. Ez a kitöltött summary a stop-pont előtti összefoglaló a Fejlesztőnek.
   - **Egy Milestone commit** a summary `Commit` mezője szerint: a milestone teljes felgyűlt kódváltozása + az összes `MS-XX:IS-YY` `[x]` + az összes `MS-XX:MV-XX` `[x]` + a kitöltött summary egyetlen commitba kerül.
   - Az `MS-XX` heading-nek nincs külön checkbox-a — a milestone implicit lezárt, ha minden alá tartozó `IS` és `MV` `[x]`.
   - Piros `MS-XX:MV-XX` blokkolja a commit-ot és a következő `MS-(XX+1)` indulását.

6. **Globális verifikáció + záró commit**:
   - Futtasd le a `Plan.Globális verifikáció` (`GV-XX`) lépéseit. Zöldre váltás után azonnal pipáld `[x]`-szel.
   - **Flat módban (nincs `MV-XX`)** — a Plan-lépésekre eddig nem volt commit. A `GV-XX`-ek `[x]`-elése után:
      - **Töltsd ki a `Globális summary` blokkot** a Plan placeholder-skeletonja szerint, valós tartalommal: a Plan eredménye 1-2 mondatban, logikai területenként egy sor a kiváltó `IS-XX` lépés(ek)re és az érintett fájl(ok)ra mutató linkkel, `Teljesült` AC-lista a `GV-XX` referenciájával, `Delták` a keletkezett `IL-XX`-ekkel (és hogy külön commit-ban vannak-e).
      - **Állj meg.** A kitöltött summary az összefoglaló a Fejlesztőnek a végállapotról.
      - Fejlesztő-megerősítés után **egy záró Globális commit** a summary `Commit` mezője szerint: az összes felgyűlt kódváltozás + minden `IS-XX` `[x]` + minden `GV-XX` `[x]` + a kitöltött summary egyetlen commitba kerül.
   - **Multi-stage módban** — a milestone-ok már commitolva vannak. A `GV-XX` általában nem keletkeztet kódváltozást; ha mégis (kis fix, regresszió), az `IL-XX` napló-bejegyzéssel és saját commit-tal kezelendő. A `GV-XX` `[x]` jelölések pedig a következő `IL-XX` commit-jával együtt mennek be, vagy ha nincs `IL-XX`, akkor külön `docs(spec)` commit-ban.

7. **Zárás-jelentés**:
   - Röviden a Fejlesztőnek: hány `IS-XX` ment Plan szerint, hány `IL-XX` napló-bejegyzés keletkezett, mi a végállapot.
   - A push és a release a Fejlesztőé.
