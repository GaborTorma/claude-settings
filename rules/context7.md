# Context7 használat

- **Mi**: `context7` MCP szerver — friss, verziókövetett dokumentáció.
- **KÖTELEZŐ**: külső library / framework / csomagkezelő / SDK / API / CLI / cloud service
használatakor **előbb docs (lásd Sorrend), utána kód vagy válasz**. A tréning adat
elavulhatott.
- **Verzió**: előbb olvasd ki a projekt verzióját (`package.json`, lockfile, `pyproject.toml`), és arra kérdezz.
- **Gyakoriság**: sessionönként témánként egyszer elég — ugyanazt ne kérdezd le újra.
- **Ne használd**: saját business logika, általános programozási koncepció, nem lib-eredetű belső hiba.
- **Workflow**: `resolve-library-id` → `query-docs` / `get-library-docs`.
- **Csomagba épített docs**: ha a telepített csomag verzió-illesztett docs-ot szállít, az megelőzi a Context7-et. Pl. `"next": ">=16.2.0"`.
- **Sorrend**: csomagba épített docs > Context7 > hivatalos docs (webfetch) > tréning-memória/web search.
- **Fallback**: ha a Context7 nem elérhető vagy nincs találat → következő forrás a sorrendből, és **mondd ki** a *Fejlesztő*nek, hogy nem Context7-ből dolgozol.
