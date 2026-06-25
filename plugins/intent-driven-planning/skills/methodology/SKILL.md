---
name: methodology
description: Intent-Driven Planning módszertan kontextusa — slug/branch konvenciók, Spec-fájl elhelyezés, élő dokumentum fegyelem. Aktiválódik ha a Fejlesztő `intent-driven-planning:` slash commandot használ, `.spec/*.md` fájllal dolgozik, vagy a current branch slug-ja egyezik egy létező Spec-fájl basenamejével.
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

**Slug** — az `Intent` magvát tükröző kebab-case azonosító. Az AI javasolja, a Fejlesztő hagyja jóvá. Ez köti össze a **Spec-fájl**t és a branchet.

**Spec-fájl** — `.spec/<slug>.md`. Kategorizáláshoz almappa is használható: `.spec/<group>/<slug>.md` (pl. `.spec/auth/oauth-token-rotation.md`).

**Prefix** — az `Intent` jellege szerint: `feat` (új funkció), `fix` (bug- vagy regressziófix), `refactor` (viselkedést nem érintő szerkezeti átalakítás).

**Branch** — `<prefix>/<slug>`. Ha a repo látható branch-konvenciót használ, ahhoz igazodj.

## Hivatkozások

A Spec-fájl prózájában (Intent / Spec / Plan / Megvalósítási napló) a kódbeli hivatkozások **relatív linkek** legyenek — a Spec-fájl helyéhez képest.

- **Fájl**: a link szövege a fájl és útvonala, a target a relatív útvonal. Példa: `[src/auth/middleware.ts](../src/auth/middleware.ts)`.

- **Konkrét, létező függvény / változó / symbol**: a link szövege **csak a symbol neve** (sor nélkül), a target relatív útvonal **`#LNN` sor-hash-sel**. A sorszám a link URL-jében legyen, a szövegben **ne**. Példa: `[validateToken](../src/auth/middleware.ts#L42)` — a Fejlesztő a `validateToken` szöveget látja, a kattintás a 42. sorra ugrik.

- **Csak létező kódra**: ha a hivatkozott symbol még nem létezik (pl. tervezett új függvény a Plan-ben), **ne tegyél linket** — csak inline backtick kód-formázás (` `` `).

- **Spec-fájlok közötti link**: a `.spec/` almappa-konvenciót követve relatív (pl. `[.spec/auth/oauth-token-rotation.md](./auth/oauth-token-rotation.md)`).

## Élő dokumentum fegyelem

A **Spec-fájl** szakaszai különböző életciklust követnek a Plan-jóváhagyás körül:

- **Session indulásakor**: ha a current branch slug-ja egyezik egy `.spec/<slug>.md` vagy `.spec/<group>/<slug>.md` fájl basenamejével, vagy a Fejlesztő explicit **Spec-fájl**ra hivatkozik, **olvasd el** a fájlt az első tájékozódó lépések között.

- **Tervezés közben — backward-propagation szükséges**:
   - Ha a `Spec` írásakor kiderül valami, ami módosítja az `Intent`-et, az `Intent`-et **frissíteni kell**.
   - Ha a `Plan` írásakor kiderül valami, ami a `Spec`-et vagy `Intent`-et érinti, azokat is frissíteni kell.
   - A `Plan`-jóváhagyás egy konzisztens, koherens dokumentumra menjen át.

- **Plan-jóváhagyás után — fagyott állapot**: az `Intent`, `Spec`, `Plan` szakaszok **tartalma többé nem módosul**. Ezek tükrözik, mire vállalkoztunk a tervezéskor. **Kivételek** (nem tartalmi tervezés-módosítás, hanem haladás-rögzítés): (1) a Plan-lépés-bullet-ek (`IS-XX` / `MS-XX:IS-YY` / `MS-XX:MV-XX` / `GV-XX`) `[ ]` → `[x]` állapot-jelölése implementáció közben; (2) a `Milestone summary` / `Globális summary` placeholder-skeleton kitöltése a milestone- ill. Plan-záráskor valós tartalommal (eredmény, érintett fájlok, teljesült AC-k, delták, commit). Az `MS-XX` heading-nek nincs külön checkbox-a; a milestone-állapot a benne lévő `IS` és `MV` lépésekből olvasható.

- **Implementáció közben — `## Megvalósítási napló` bővül**: az eltérések, fix-ek, follow-up-ok és refactorok a Plan után fűzött `Megvalósítási napló` szakaszba kerülnek **strukturált bejegyzésként** (sablon: `intent-driven-planning:plan` Sablon szakasza). Az eredeti három szakasz változatlan marad — a napló adja a "tényleges megvalósítás" rétegét.

   **Mit NEM rögzít a napló**: a Plan változatlan lefutása nem keletkeztet bejegyzést — ha egy `IS-XX` (vagy `MS-XX:IS-YY`) lépés pontosan a Plan szerint ment, nincs delta amit rögzíteni kellene.

   **Korábbi bejegyzés frissítése új helyett**: ha olyan dolog történik, ami egy **korábbi `IL-XX` bejegyzést érint** (pl. egy korábbi `Nyitott` tétel teljesül, egy korábbi delta tovább módosul vagy visszavonódik), akkor a **meglévő bejegyzést kell frissíteni** — ne nyiss újat. Új `IL-XX` csak független, új deltához készül.

- **Intent szintű változás** (a probléma vagy cél maga változik): állj meg, és egyeztess a Fejlesztővel.

### Megvalósítási napló — példa bejegyzések

- <a id="IL-01"></a>**IL-01** — _Eltérő technikai megközelítéssel_ [[IS-04](#IS-04)]
   - **Típus**: Eltérés
   - **Indoklás**: A Plan-megközelítés (közvetlen módosítás) duplikációt hozott volna egy meglévő segédfüggvénnyel; implementáláskor derült ki, hogy a helper kiterjesztése egyszerűbb és kevesebb új kódot igényel.
   - **Delta**: Az [IS-04](#IS-04) célját a meglévő segédfüggvény kiterjesztésével értük el, közvetlen módosítás helyett. A Failing test és az eredmény változatlan; csak a megvalósítás módja tér el a Plantól.

- <a id="IL-02"></a>**IL-02** — _Menet közben felfedezett bug fixe_ [—]
   - **Típus**: Fix
   - **Indoklás**: Az [IS-05](#IS-05) implementálásakor egy meglévő edge case bug derült ki — a kód hibás állapotba kerül; a bug blokkolja az [IS-05](#IS-05) Failing test-jét, ezért itt és most javítható (külön ticketre halasztva regressziót okozna a Plan későbbi lépéseinek tesztjeiben).
   - **Delta**: Minimális javítás az érintett függvényben; az [IS-05](#IS-05) Failing test-je ezután már a tervezett viselkedést méri, a Plan többi lépését nem mozdítja.
   - **Nyitott**: a fix mellé tartozó regressziós teszt megírása későbbre halasztva — külön follow-up ticketre kerül, mert a Plan scope-ján kívül esik.
   - **Commit**: `fix(<scope>): <subject> [IL-02]`
