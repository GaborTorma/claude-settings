---
date: 2026-09-25
source: varazskez
kind: skill
---

# vercel-init — Vercel + Neon projekt indítása nulláról

## Mi

Egy új webapp bekötése lépésről lépésre: GitHub-repó → Vercel projekt → git
connect → Neon a Marketplace-ről → négy Neon-ág (`main` éles, `test` CI,
`preview/<git-branch>` feature, `dev` lokális) → kód az integráció változóival.
A lépéseket az *AI* a Vercel-, Neon- és GitHub-MCP-vel (vagy CLI-vel) végzi.

## Miért

A Neon Marketplace-integráció több, nem dokumentált módon viselkedik, és utólag
ezek csendes hibákat okoznak (a preview rossz DB-re megy: `relation "…" does not
exist`, `42P01`):
- preview-deploynál saját ágat nyit, és a kapcsolati adatokat **deployment-szinten
  injektálja** — a `vercel env ls` nem mutatja, a kézi, azonos nevű változót felülírja;
- az adatbázist **azonosító alapján követi**, nem név alapján;
- a változói minden targeten a `main`-re mutatnak → `vercel env pull` = éles DB lokálisan;
- git connect nélkül a preview-ágak nem takarítódnak;
- rossz framework / Root Directory esetén rossz eszközzel buildel
  (`Error: Command "… build" exited with 127`).

Ha ezeket az induláskor rendezzük, később nincs mit javítani.

## Hogyan alkalmazd

1. **Ellenőrzés**: élnek-e a Vercel-, Neon- és GitHub-MCP-k (vagy `vercel`, `gh`); melyik Vercel team.
2. **Repó**: `git init`, `.gitignore`, `.env.example`, első commit, `gh repo create`.
3. **Vercel projekt**: `vercel link` (név = app neve). Framework = a valós
   keretrendszer, monorepóban **Root Directory = az app mappája**. Régió: `fra1`
   (`vercel.json` `regions` + projektbeállítás).
4. **Git connect**: `vercel git connect` (a Vercel GitHub-appjának hozzáférés).
   Döntés: merge = éles deploy, vagy `git.deploymentEnabled: false` a `main`-re + kézi promote.
5. **Neon**: `vercel integration add neon --metadata region=fra1` (→ `aws-eu-central-1`),
   production + preview környezetre, preview-branchelés bekapcsolva. Neon MCP-vel
   ellenőrizd a régiót. **Saját adatbázist ne hozz létre**: az alapértelmezett `neondb` marad.
6. **Ágak** (Neon MCP `create_branch` a `main`-ből): `dev` a lokális fejlesztésnek,
   `test` a CI-nak. A `preview/<git-branch>` ágakat az integráció nyitja.
7. **Kód**:
   - kapcsolat: `POSTGRES_URL` (futásidő), `POSTGRES_URL_NON_POOLING` (migráció); saját DB-változó ne legyen;
   - Fluid Compute: `pg` Pool + `attachDatabasePool` (a Neon ajánlása); az URL-ben
     `sslmode=verify-full`, és az adatbázis neve rögzítve (`/neondb`);
   - migráció: verziózott (`drizzle-kit generate` + `migrate`), `push` soha a `main`-re;
     a preview-build előtt migráció, csak ha `VERCEL_ENV=preview`.
8. **Lokális env**: `.env` a `dev` ágra (host-csere: az ágak öröklik a szerepkört és
   a jelszót). `vercel env pull` soha a `.env.local`-ba.
9. **CI**: e2e a `test` ágon, utána `reset_from_parent`.
10. **Első deploy és ellenőrzés**: push → preview; mérd, hogy a preview a saját ágára
    megy (`pg_stat_database.xact_commit` az ágon előtte/utána). Merge → éles (vagy promote).

**Munka közben**: feature = git branch = worktree = `preview/<git-branch>` Neon-ág;
a worktree `.env`-je host-cserével készül (a `.env`, `.vercel/`, `node_modules` nem
jön át). A branch törlésével a Neon-ág is megszűnik.

**Korlátok**: a Claude Code szűrője az éles deployt és a Vercel env-titok írását
letiltja — ezeket a *Fejlesztő* futtatja. Törlés és `reset` előtt kérdezz, kockázatos
lépés előtt snapshot. Éles DB-átállás: `vercel deploy --prod --skip-domain` → DB-művelet
→ azonnal `vercel promote`.

A vercel-neon plugin `neon-driver` és `vercel-env` skillje ezekben elavult.
**Nincs kipróbálva**: előre létrehozott ágat újrahasznosít-e a Vercel; két Vercel
projekt egy Neon projekten.
