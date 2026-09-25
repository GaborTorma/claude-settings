# Stack preferenciák

**Nincs default stack!** Új projektnél vagy stack-döntésnél kérdezd a *Fejlesztő*t, és javasolj 2-3 opciót előnyökkel, hátrányokkal, kockázatokkal.

**Függőségek**: észszerűen. Ha az adott esetre van bevett, nem overkill lib, használd; ne írj 500 sort azért, hogy elkerüld, de ne húzz be libet 3 sornyi kódért.

**Preferenciák**: `vercel`, `next.js`, `tailwind`, `neon`, `mongodb`, `zod`, `drizzle`, `uv`, `playwright`, Claude preview

**Kizárások**: `express`, `pip`

## Ha Vercel + Neon

A hogyan: `vercel-neon` plugin (`/vercel-neon:check`).

- **Csomagok**: Vercel Pro, Neon Launch; a Neon-szervezet Vercel-kezelt (Marketplace-integráció). → `vercel-neon:vercel-neon`, `vercel-neon:neon-compute`
- **MCP-first**:
  - Vercel MCP (`plugin:vercel:vercel`, eszközök: `mcp__plugin_vercel_vercel__*`). Fallback: Vercel CLI
  - Neon MCP (claude.ai connector, UUID-prefixű eszközök — a prefix sessiononként változik).
- **Topológia**: egy app = egy Vercel projekt = egy Neon projekt, azonos névvel. → `vercel-neon:vercel-neon`
- **Régió**: `fra1` ↔ `aws-eu-central-1` — a driver előfeltétele: eltérésnél a TCP-kapcsolódás minden oda-vissza útja régiók között megy. → `vercel-neon:vercel-neon`
- **Driver**: `pg` Pool + `drizzle-orm/node-postgres` + kötelező `attachDatabasePool` → `vercel-neon:neon-driver`
- **Migráció**: verziózott `drizzle-kit`; `push` éles ellen soha. → `vercel-neon:neon-branching`
- **Neon-ágak**: `main` éles · `dev` lokális · `preview/<git-ág>` feature-enként. → `vercel-neon:neon-branching`
- **Env**: a DB-kapcsolatot az integráció adja; lokálisan soha nem éles DB. → `vercel-neon:vercel-env`
- **Élesítés**: snapshot → migrate → deploy, a *Fejlesztő* jóváhagyásával. → `vercel-neon:feature-workflow`
