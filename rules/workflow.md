# Munkafolyamat

Ágkezelés git + GitHub alatt, stack-függetlenül. Ha a stacknek van saját
workflow-skillje (DB-ág, preview, deploy), az erre épül, nem írja felül.

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

**Útválasztás a feladat típusa szerint**, a munka indulásakor. A kategóriák a
Conventional Commits type-jai (→ `/commit`):

- Feature-jellegű: `feat`, `refactor`, és típustól függetlenül a breaking change (`!`) és minden
  migráció, amit egy `git revert` nem állít vissza (pl. DB-séma, tárolt adat, más kliensek által hívott API, env).
- Fix-jellegű: minden más (`fix`, `perf`, `style`, `docs`, `test`, `build`, `chore`, ...).
- Vegyes feladat → feature-ág. Ha egy Fix-jellegű munkáról menet közben kiderül, hogy feature-jellegű, állj meg és kérdezz.

## Init

1. `git init -b main`
2. `git-graph --launch-config`
3. `.gitignore` (→ [enviroment.md](enviroment.md))
4. `.env.example` (→ [enviroment.md](enviroment.md))
5. `CLAUDE.md` (→ [claude.md](claude.md))
6. `git commit -m "Initial commit"`
7. `git branch dev`
8. `git switch dev`

Remote (GitHub) nem része az initnek → `/push`, amikor a *Fejlesztő* kéri.

## Fix-jellegű munka:

**Indulás** — a `dev` utoléri a `main`-t:

1. `git fetch`
2. `git switch dev`
3. `git merge --ff-only origin/main`
4. Ha nem fast-forward (a `dev`-en merge-eletlen munka van): egyeztess a *Fejlesztő*vel.

**Munka**: commit `/commit`-tal.

**Merge** a *Fejlesztő* jóváhagyásával, PR nélkül: `/commit-push-merge`. A `dev` megmarad.

## Feature-jellegű munka:

**Indulás**: `/worktree-open` — saját worktree, `feat/` vagy `refactor/` ág.

**Munka**:

1. Commit `/commit`-tal
2. Első push: `git push -u origin HEAD`

A `main` munka közben nem kerül be az ágba — csak a PR merge-e fésüli össze. Kivétel:
ütközésnél a lezáráskor a `/merge-pr` az ágban oldja fel (`git merge origin/main`).

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
