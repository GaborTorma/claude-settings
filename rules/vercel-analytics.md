# Vercel Analytics

## A csomag beépítése NEM kapcsolja be a mérést

- A `@vercel/analytics` (és a `@vercel/speed-insights`) telepítése és a komponens
  beillesztése **önmagában nem gyűjt adatot**. A projekt dashboardján külön kell
  bekapcsolni: **Project → Analytics → Enable**.
- **Miért csúszik át az ellenőrzésen**: bekapcsolás nélkül is ott a
  `<vercel-analytics>` elem a HTML-ben, a `/_vercel/insights/script.js` **200**-at
  ad, és a `POST /_vercel/insights/event` **400**-at érvénytelen törzsre — vagyis
  minden élőnek látszik, miközben az adat eldobódik.
- **Nem gyűjt visszamenőleg.** Ami a bekapcsolás előtt történt, elveszett.
- **Ellenőrzés egy hívással**: MCP `get_web_analytics` → ha nincs bekapcsolva,
  `400 web_analytics_not_enabled`. Ezt hidd el, ne a fenti 200/400-akat.
- Új projektnél a mérés bekötése akkor kész, ha ez a hívás **számot ad vissza**.

## Az adat kiolvasása — csak MCP-n át

- A Web Analyticsnek **nincs publikus REST API-ja**. Vercel API tokennel nem
  kérdezhető le (`/v1/web-analytics`, `/api/web-analytics`, … mind 404).
  A token a deployhoz és a projektműveletekhez jó, az adathoz nem.
- Az általános `mcp.vercel.com` végpont hitelesítéskor **hatókört választat**, és a
  személyes hatókör egy csapat projektjéhez **403**-at ad
  (`You must re-authenticate to this scope`). Projektre szűkített végpont a
  megbízható, ott nincs mit elvéteni:

```bash
claude mcp add --transport http <név> https://mcp.vercel.com/<team-slug>/<project-slug>
claude mcp login  <név>     # böngészős jóváhagyás
claude mcp get    <név>     # → Status: ✔ Connected
```

- Ha a `login` **pár másodperc alatt** lefut, gyanús: valószínűleg korábbi
  munkamenetet fogadott el, és a hatókör változatlan maradt. `logout` + `login`
  kikényszeríti az új jóváhagyó képernyőt.
- Az MCP-kapcsolat a munkamenet **indulásakor** jön létre: az újonnan hozzáadott
  szerver a futó beszélgetésben még nem látszik, **újraindítás kell**.
