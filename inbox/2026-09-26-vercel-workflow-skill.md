---
date: 2026-09-26
source: varazskez (hangfurdo)
kind: skill
---

# Vercel Workflow SDK: új `vercel-workflow` skill a vercel-neon pluginbe + kiegészítés a `neon-compute`-ba

## Mi

A vercel-neon plugin kapjon egy `vercel-workflow` skillt a Workflow SDK
(`workflow` csomag) Vercel + Neon stackbe illesztéséről. A `neon-compute`
skill pedig mondja ki: a gyakori pollozó cront (pl. `*/15`) ki lehet váltani
entitásonként alvó workflow-val (`sleep()` az esedékes időpontig), és így a
Neon compute scale-to-zero-ba mehet.

## Miért

A varazskez projektben a vendég-e-maileket és az alkalom előtti
emlékeztetőket Workflow SDK-ra tettük (workflow@4.8.9, Next 16). Közben
előjött néhány nem nyilvánvaló csapda. Ezek a Vercel + Neon párosnál
projektfüggetlenül visszatérnek, a meglévő `vercel:workflow` skill viszont egyiket sem
említi:

1. **Adat-rezidencia.** A Vercel World a workflow-eseménynaplót **iad1-ben
   (USA)** tárolja, titkosítva, az app régiójától függetlenül (bundled docs:
   `deploying/world/vercel-world.mdx` → Limitations). A mi szabványunk
   `fra1` ↔ `aws-eu-central-1`, és az adatkezelési tájékoztatók EU-s tárolást
   ígérnek. Ezért a workflow inputja, a step visszatérési értéke és a step
   hibaüzenete **csak azonosító lehet**. A személyes adatot a step az EU-s
   DB-ből olvassa. Az SMTP-hiba szövegében is lehet e-mail-cím, ezért a
   részletes hiba a DB-be megy, nem a `throw`-ba.
2. **A Node-modul tilalom tranzitív.** Ha a workflow-törzs egy olyan modulból
   importál (akár csak egy tiszta helper függvényt), amelyik a `pg` Pool-t
   vagy a `nodemailer`-t húzza be, akkor a build `next.config.ts` betöltésekor
   elhasal:
   ```
   ERROR: [plugin: workflow-node-module-error] You are attempting to use "pg" which depends on Node.js modules. Packages that depend on Node.js modules are not available in workflow functions.
   ⨯ Failed to load next.config.ts
   ```
   A step-törzsek importjait a transzformáció eltávolítja, a workflow-törzs
   által használt importokat nem. Megoldás: a workflow-törzsben használt
   helper (pl. a hook-token) mellékhatás-mentes modulban éljen (a workflow
   fájlban magában), a DB-t húzó modulból csak `import type` legyen.
3. **Next 16 `proxy.ts`.** A matchernek ki kell hagynia a
   `.well-known/workflow/` útvonalat, különben a queue-hívások elhasalnak.
   Hibaüzenet: `[local world] Queue operation failed … detached ArrayBuffer`.
4. **Generált route-ok.** A `withWorkflow` az `app/.well-known/workflow/`
   alá ír. Saját `.gitignore`-t kap, de az eslint `Unused eslint-disable
   directive` warningot ad rá, ezért `globalIgnores`-ba kell tenni. Plusz
   `.workflow-data/` (Local World) a `.gitignore`-ba.
5. **Outbox minta e-mailhez.** Az idempotencia nem SMTP-kulccsal jön
   (nincs), hanem DB-állapottal: `queued` napló-sor, és a workflow csak az
   ID-t kapja. A step `status !== 'queued'` esetén no-op. Átmeneti hibánál
   `RetryableError` visszalépéssel, 5xx-nél `FatalError`. A végső kudarcot a
   workflow `try/catch`-e jelöli, és értesítőt küld. Claim + sorba állítás
   **egy tranzakcióban** (`pg` Pool-lal van `db.transaction`), különben a step
   újrapróbálása elveszítheti a levelet.
6. **Hook mint egyediség-őr és ébresztő.** Determinisztikus token
   (`emlekezteto:<id>`) + `await hook.getConflict()` a workflow elején. A
   duplán indított példány így azonnal kilép, ezért a pótló/backfill végpont
   bármikor újrafuttatható. **Csapda:** minden `hook.then(...)` hívás a
   *következő* payloadra iratkozik fel. `Promise.race([sleep(at), hook])`
   ciklusban ezért egyetlen függő hook-ígéretet kell körökön át vinni, és csak
   akkor kérni újat, ha az beérkezett. Különben egy gazdátlan `.then` nyeli el
   a következő ébresztést.
7. **A futás a deploymenthez van kötve.** Egy hetekig alvó workflow az
   indító deploy kódján fut tovább. A step-ben lévő logika (pl. levélsablon)
   javítása a már alvó futásokat nem érinti; ehhez „Rerun on latest” vagy
   `start(..., { deploymentId: "latest" })` kell.
8. **Neon-költség.** A 15 perces cron óránként 4× ébresztette a computet
   (a scale-to-zero 5 perc után lép be, így ez kb. ⅓-os ébrenlét). Az
   entitásonként alvó workflow alvás közben nem nyúl a DB-hez, csak az
   esedékes pillanatban.

## Hogyan alkalmazd

- **`vercel-workflow` skill (vercel-neon plugin)**. Trigger: a *Fejlesztő*
  cront, háttérmunkát, e-mail-küldést, újrapróbálást vagy ütemezett levelet
  kér Vercel + Neon stacken, vagy a `workflow` csomagot említi. Tartalom:
  a fenti 1–7. pont ellenőrzőlistaként, plusz a lokális teszt receptje:
  - SMTP-nyelő: `uvx --from aiosmtpd python -m aiosmtpd -n -d -l 127.0.0.1:2525`;
  - ideiglenes `.claude/launch.json`-konfig `runtimeExecutable: "env"` +
    `SMTP_HOST=127.0.0.1 SMTP_PORT=2525` override-dal (a `.env` valódi
    SMTP-je érintetlen marad);
  - futások megtekintése: `npx workflow inspect runs --json`.
  Kötelező először a csomagba épített docs
  (`node_modules/workflow/docs/`). Telepítés előtt:
  `npm pack workflow@<ver>` a scratchpadbe, és onnan olvasható.
- **`neon-compute` skill**. A „60 percnél gyakoribb cron vagy polling”
  szakaszba kerüljön be alternatívaként: időpont-alapú teendőnél
  (emlékeztető, lejárat, follow-up) entitásonként alvó workflow a pollozó cron
  helyett. Ennek a költsége a workflow-lépésekben jelentkezik, nem a
  compute-órákban. Hivatkozás a `vercel-workflow` skillre.
- Valós példa a varazskez repóban: `hangfurdo/workflows/level.ts`,
  `hangfurdo/workflows/emlekezteto.ts`, `hangfurdo/lib/outbox*.ts`
  (branch `feat/workflow-emails`, 2026-09-26).
