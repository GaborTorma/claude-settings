# Munkafolyamat

Hogyan kezdünk vagy bővítünk egy projektet. Ha a stacknek van saját
workflow-skillje (DB-ág, preview, deploy), az erre épül, nem írja felül.

## Célok tisztázása

A munka indulásakor, a *Fejlesztő*vel. Ha a munka issue-ból vagy parkoló tételből indul (`/pick`), az 1–2. pontot az adja.

1. **Cél**: milyen problémát kell megoldani.
2. **Hatókör**: mi része az aktuális körnek és mi nem.
3. **Útválasztás** a feladat típusa szerint. A kategóriák a Conventional Commits type-jai (→ `/commit`):
   - Feature-jellegű: `feat`, `refactor`, és típustól függetlenül a breaking change (`!`) és minden
     migráció, amit egy `git revert` nem állít vissza (pl. DB-séma, tárolt adat, más kliensek által hívott API, env).
   - Fix-jellegű: minden más (`fix`, `perf`, `style`, `docs`, `test`, `build`, `chore`, ...).
   - Vegyes feladat → feature-ág. Ha egy Fix-jellegű munkáról menet közben kiderül, hogy feature-jellegű, állj meg és kérdezz.
4. **Stack**: új projektnél vagy új függőségnél → [stack.md](stack.md).

Ez a könnyített változat; nagyobb, több lépéses körnél az 1–2. pont → `/intent-driven-planning`.

## Ágak

| Ág | Szerep | Worktree | Élettartam |
| --- | --- | --- | --- |
| `main` | kiadható állapot, GitHub default | nincs saját | állandó |
| `dev` | Fix-jellegű munka | fő checkout | állandó |
| `feat/<slug>`, `refactor/<slug>` | Feature-jellegű munka | `/worktree-open` | merge-ig |

**`<slug>`**: a feladat tartalmából, a munka indulásakor — angol, ASCII kebab-case,
2–4 szó (pl. `oauth-login`, `extract-user-service`). Ugyanez a worktree neve és az ág vége (pl. `feat/oauth-login`).

**Teendők**: tartós → GitHub issue (`/issue`, `/issues`), `fix` / `feature` címkével;
rövid távú, félretett → `.parked.md` (`/park`). Indulás mindkettőből: `/pick`.

## Init

1. `git init -b main`
2. A stack váza: scaffold, lint / typecheck / test / format config
3. `.gitignore` (→ [enviroment.md](enviroment.md))
4. `.env.example` (→ [enviroment.md](enviroment.md))
5. `CLAUDE.md` (→ [claude.md](claude.md))
6. `/commit chore: initial commit` — egyetlen commit, témabontás nélkül
7. `git branch dev`
8. `git switch dev`
9. `/push`

## Fix-jellegű munka:

**Indulás** — a `dev` utoléri a `main`-t:

1. `git fetch`
2. `git switch dev`
3. `git merge --ff-only origin/main`

Ha nem fast-forward (a `dev`-en merge-eletlen munka van): egyeztess a *Fejlesztő*vel.

**Munka**: commit `/commit`-tal.

**Merge** a *Fejlesztő* jóváhagyásával, PR nélkül: `/commit-push-merge`. A `dev` megmarad.

## Feature-jellegű munka:

**Indulás**: `/worktree-open` — saját worktree, `feat/` vagy `refactor/` ág.

**Munka**:

`/commit-push`

A `main` munka közben nem kerül be az ágba — csak a PR merge-e fésüli össze.
Kivétel: ütközésnél a lezáráskor a `/merge-pr` az ágban oldja fel (`git merge origin/main`).

**Lezárás** a *Fejlesztő* jóváhagyásával: `/commit-push-pr-merge`.

Félbehagyott vagy eldobott feature: `/worktree-close` (mergeletlen munkánál rákérdez).

**Utána**: a session a fő checkoutban, `dev`-en folytatódik.

## Kiadás

`/release`, a *Fejlesztő* kérésére — nem minden merge után. Kiadatlan minden, ami
a legutóbbi `v*` tag óta a `main`-re került, akárhány merge is.

- A `main` pusholása nem deploy: a hosting `main`-auto-deployja ki van kapcsolva
  (a stack skillje szerint).
- Tag csak sikeres deploy után; az élesben lévő állapot = a legutóbbi `v*` tag.
- Ami még nincs kint: `git log $(git describe --tags --abbrev=0 --match 'v*')..main`.
