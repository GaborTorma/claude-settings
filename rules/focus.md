# Fókusz

Egyszerre egy nyitott téma. Ami elkezdődött, az lezárul — vagy kimondottan parkol.

- **Lezárt** = kész, ellenőrizve, commitolva; vagy a *Fejlesztő* döntése szerint parkolva / eldobva.
- **Session elején**: ha félbemaradt munka van (commitolatlan változás, nyitott worktree,
  mergeletlen ág), egy mondatban jelezd, mielőtt az új kérésbe kezdesz.

## Új téma menet közben

Ha a *Fejlesztő* a nyitott feladattól független témát hoz:

1. **Ne válts csendben.** Egy sorban: mi a nyitott feladat, hol tart, mi van hátra.
2. **Kérdezd meg** (`AskUserQuestion`):
   - **Előbb lezárjuk** — ajánlott, ha a maradék rövid. Az új ötlet automatikusan parkol.
   - **Váltunk** — a nyitott munka parkol: commitolva vagy saját ágon, egy sorral, hogy mi van hátra.
   - **A nyitottat eldobjuk.**
3. **Parkolás**: parkolólista a sessionben, egy sor ötletenként — a *Fejlesztő* szavaival,
   hogy később is érthető legyen; jelöld, kinek a szándéka: *Fejlesztő* (kérte, vagy az ő
   félbemaradt munkája) / *AI* (magától vette észre).
4. **Lezáráskor** sorold fel: `Parkolóban: …`, és kérdezd meg `AskUserQuestion`-nel: Hogy folytassuk?
   Ha a *Fejlesztő* elveti a kérdést → a válasz végén:

   ```markdown
   1. **Aktuális:** <ami most folyamatban van>
   2. **Parkolóban:**
      1. <parkolt tétel> — *Fejlesztő* | *AI*
   ```

   Ha nincs aktuális:

   ```markdown
   **Parkolóban:**

   1. <parkolt tétel> — *Fejlesztő* | *AI*
   ```

Ha a *Fejlesztő* kifejezetten vált ("hagyjuk, jöjjön X") → nem kérdezel, de egy sorban
rögzíted, mi maradt nyitva.

**Nem új téma**: a nyitott feladathoz tartozó kérdés vagy finomítás; rövid, kódot nem
érintő kérdés — válaszolj röviden, utána egy mondattal vissza a nyitott feladathoz.

**Megszakíthat**: éles hiba, blokkoló, vagy a nyitott feladat előfeltétele.

## Az *AI* se csapongjon

- Menet közben észrevett, nem kért javítás → ne csináld meg, parkold.
- Mellékszálat ("közben ezt is megnézem") ne nyiss a *Fejlesztő* kérése nélkül, de parkold.
