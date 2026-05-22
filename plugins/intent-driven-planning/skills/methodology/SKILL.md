---
name: methodology
description: Intent-Driven Planning módszertan kontextusa — slug/branch konvenciók, Spec-fájl elhelyezés, élő dokumentum fegyelem. Aktiválódik ha a user `intent-driven-planning:` slash commandot használ, `.spec/*.md` fájllal dolgozik, vagy a current branch slug-ja egyezik egy létező Spec-fájl basenamejével.
---

# Intent-Driven Planning — Methodology

Az Intent-Driven Planning három tervezési fázisra (intent → spec → plan) és egy megvalósítási fázisra (apply) bontja a feature / refactor / fix munkafolyamatot, + egy mellék-command (`review`) tervezés közbeni koherencia-ellenőrzéshez. Mindegyik külön slash commanddal indul; fájlt az `intent-driven-planning:plan` ír (mentés), az `intent-driven-planning:apply` pedig bővít.

| Fázis | Command                         | Tartalom                                                                                      |
| ----- | ------------------------------- | --------------------------------------------------------------------------------------------- |
| 1     | `intent-driven-planning:intent` | Probléma, célok, sikerkritérium, NEM-célok, későbbi megvalósítás                              |
| 2     | `intent-driven-planning:spec`   | Funkcionális + nem-funkcionális követelmények, elfogadási kritériumok                         |
| 3     | `intent-driven-planning:plan`   | Tervezett változtatások + implementációs lépések (TDD-szerűen) + teljes **Spec-fájl** mentése |
| 4     | `intent-driven-planning:apply`  | Plan-lépések megvalósítása TDD-ciklusban + `Megvalósítási napló` bővítése deltákkal           |
| —     | `intent-driven-planning:review` | Tervezés közben futtatható koherencia-check a draft-on (report-only)                          |

A három tervezési fázis-command iteratív review-t használ a Plan harness-en keresztül; csak `intent-driven-planning:plan` approve-ja jelenti a teljes terv jóváhagyását és a fájl mentését. A `review` nem mutál semmit, és nem kötődik fázishoz — bármelyik draft-állapotra adaptívan fut.

## Elnevezés

**Slug** — az `Intent` magvát tükröző kebab-case azonosító. Claude javasolja, a user hagyja jóvá. Ez köti össze a **Spec-fájl**t és a branchet.

**Spec-fájl** — `.spec/<slug>.md`. Kategorizáláshoz almappa is használható: `.spec/<group>/<slug>.md` (pl. `.spec/auth/oauth-token-rotation.md`).

**Prefix** — az `Intent` jellege szerint: `feat` (új funkció), `fix` (bug- vagy regressziófix), `refactor` (viselkedést nem érintő szerkezeti átalakítás).

**Branch** — `<prefix>/<slug>`. Ha a repo látható branch-konvenciót használ, ahhoz igazodj.

## Élő dokumentum fegyelem

A **Spec-fájl** szakaszai különböző életciklust követnek a Plan-jóváhagyás körül:

- **Session indulásakor**: ha a current branch slug-ja egyezik egy `.spec/<slug>.md` vagy `.spec/<group>/<slug>.md` fájl basenamejével, vagy a user explicit **Spec-fájl**ra hivatkozik, **olvasd el** a fájlt az első tájékozódó lépések között.

- **Tervezés közben — backward-propagation szükséges**:
   - Ha a `Spec` írásakor kiderül valami, ami módosítja az `Intent`-et, az `Intent`-et **frissíteni kell**.
   - Ha a `Plan` írásakor kiderül valami, ami a `Spec`-et vagy `Intent`-et érinti, azokat is frissíteni kell.
   - A `Plan`-jóváhagyás egy konzisztens, koherens dokumentumra menjen át.

- **Plan-jóváhagyás után — fagyott állapot**: az `Intent`, `Spec`, `Plan` szakaszok **tartalma többé nem módosul**. Ezek tükrözik, mire vállalkoztunk a tervezéskor. **Egyetlen kivétel**: a Plan-lépés-bullet-ek (`IS-XX` / `MS-XX:IS-YY` / `MS-XX:MV-XX` / `GV-XX`) `[ ]` → `[x]` állapot-jelölése implementáció közben — ez nem tartalmi módosítás, csak haladás-tracking. Az `MS-XX` heading-nek nincs külön checkbox-a; a milestone-állapot a benne lévő `IS` és `MV` lépésekből olvasható.

- **Implementáció közben — `## Megvalósítási napló` bővül**: az eltérések, fix-ek, follow-up-ok és refactorok a Plan után fűzött `Megvalósítási napló` szakaszba kerülnek **strukturált bejegyzésként** (sablon: `intent-driven-planning:plan` Sablon szakasza). Az eredeti három szakasz változatlan marad — a napló adja a "tényleges megvalósítás" rétegét.

   **Mit NEM rögzít a napló**: a Plan változatlan lefutása nem keletkeztet bejegyzést — ha egy `IS-XX` (vagy `MS-XX:IS-YY`) lépés pontosan a Plan szerint ment, nincs delta amit rögzíteni kellene.

   **Korábbi bejegyzés frissítése új helyett**: ha olyan dolog történik, ami egy **korábbi `IL-XX` bejegyzést érint** (pl. egy korábbi `Nyitott` tétel teljesül, egy korábbi delta tovább módosul vagy visszavonódik), akkor a **meglévő bejegyzést kell frissíteni** — ne nyiss újat. Új `IL-XX` csak független, új deltához készül.

- **Intent szintű változás** (a probléma vagy cél maga változik): állj meg, és egyeztess a userrel.

### Megvalósítási napló — példa bejegyzések

- <a id="IL-01">**IL-01**</a> — _Eltérő technikai megközelítéssel_ [[IS-04](#IS-04)]
   - **Típus**: Eltérés
   - **Indoklás**: A Plan-megközelítés (közvetlen módosítás) duplikációt hozott volna egy meglévő segédfüggvénnyel; implementáláskor derült ki, hogy a helper kiterjesztése egyszerűbb és kevesebb új kódot igényel.
   - **Delta**: Az [IS-04](#IS-04) célját a meglévő segédfüggvény kiterjesztésével értük el, közvetlen módosítás helyett. A Failing test és az eredmény változatlan; csak a megvalósítás módja tér el a Plantól.

- <a id="IL-02">**IL-02**</a> — _Menet közben felfedezett bug fixe_ [—]
   - **Típus**: Fix
   - **Indoklás**: Az [IS-05](#IS-05) implementálásakor egy meglévő edge case bug derült ki — a kód hibás állapotba kerül; a bug blokkolja az [IS-05](#IS-05) Failing test-jét, ezért itt és most javítható (külön ticketre halasztva regressziót okozna a Plan későbbi lépéseinek tesztjeiben).
   - **Delta**: Minimális javítás az érintett függvényben; az [IS-05](#IS-05) Failing test-je ezután már a tervezett viselkedést méri, a Plan többi lépését nem mozdítja.
   - **Nyitott**: a fix mellé tartozó regressziós teszt megírása későbbre halasztva — külön follow-up ticketre kerül, mert a Plan scope-ján kívül esik.
   - **Commit**: `fix(<scope>): <subject> [IL-02]`
