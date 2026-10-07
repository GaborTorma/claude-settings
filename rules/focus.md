# Fókusz

Egyszerre egy nyitott téma. Ami elkezdődött, az lezárul — vagy kimondottan parkol.

- **Lezárt** = kész, ellenőrizve, commitolva; vagy a *Fejlesztő* döntése szerint parkolva / eldobva.
- **Session elején**: ha félbemaradt munka van (commitolatlan változás, vagy nyitott,
  mergeletlen PR: `gh pr list --state open --author @me`), vagy a `.parked.md`-ben parkoló
  tétel van (hány), egy mondatban jelezd, mielőtt az új kérésbe kezdesz.

## Új téma menet közben

Ha a *Fejlesztő* a nyitott feladattól független témát hoz:

1. **Ne válts csendben.** Egy sorban: mi a nyitott feladat, hol tart, mi van hátra.
2. **Kérdezd meg** (`AskUserQuestion`):
   - **Előbb lezárjuk** — ajánlott, ha a maradék rövid. Az új ötlet `/park`.
   - **Váltunk** — a nyitott munka commitolva vagy saját ágon marad, és `/park` egy sorral, hogy mi van hátra.
   - **A nyitottat eldobjuk.**
3. **Parkolás**: `/park <téma>` — a projekt `.parked.md`-jébe; csak rövid, a sessionhöz
   kapcsolódó tétel, legfeljebb 4; ami nagyobb vagy független, issue lesz (a `/park` dönti el).
4. **Lezáráskor**: `/parked`. A `/commit`, `/commit-push` és `/commit-push-pr` után mindig.

Ha a *Fejlesztő* kifejezetten vált ("hagyjuk, jöjjön X") → nem kérdezel, de a nyitva
maradtat `/park`.

**Nem új téma**: a nyitott feladathoz tartozó kérdés vagy finomítás; rövid, kódot nem
érintő kérdés — válaszolj röviden, utána egy mondattal vissza a nyitott feladathoz.

**Megszakíthat**: éles hiba, blokkoló, vagy a nyitott feladat előfeltétele.

## Az *AI* se csapongjon

- Menet közben észrevett, nem kért javítás → ne csináld meg, `/park`.
- Mellékszálat ("közben ezt is megnézem") ne nyiss a *Fejlesztő* kérése nélkül, de `/park`.
