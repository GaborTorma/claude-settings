---
name: changelog
description: Magyar nyelvű CHANGELOG.md bejegyzés generálása az aktuális branch tényleges kódváltozásai alapján. Használd amikor a Fejlesztő /changelog-ot ír, vagy egy feature/fix branch munkájának végén changelog bejegyzést szeretne készíteni. A skill a commit üzenetek helyett a tényleges diff-et elemzi és emberi, érthető magyar leírást ír.
---

# Changelog skill

Magyar nyelvű CHANGELOG bejegyzést generálsz az aktuális branch és a `main` branch közötti tényleges változások alapján.

## Lépések

### 1. Változások összegyűjtése

Futtasd ezeket a parancsokat, hogy megértsd mi változott:

```bash
# Aktuális branch neve
git branch --show-current

# Összefoglaló: mely fájlok változtak és mennyivel
git diff main...HEAD --stat

# A teljes diff (a tényleges változások megértéséhez)
git diff main...HEAD

# Commit lista (kontextushoz, de NEM ez lesz a changelog szövege)
git log main..HEAD --oneline
```

Ha a `main` nem létezik, próbáld `master`-rel. Ha a repo nincs git alatt, jelezd a Fejlesztőnek.

### 2. Változások elemzése

A diff alapján azonosítsd:

- **Új funkciók**: új fájlok, új függvények/osztályok/endpointok, új konfigurációs lehetőségek
- **Javítások**: bugfix jellegű változások, hibakezelés javítása
- **Teljesítmény**: optimalizációk
- **Refaktor**: struktúraváltozások viselkedésváltozás nélkül
- **Konfiguráció/build**: config, env, CI változások
- **Dokumentáció**: doc fájlok, kommentek

Fontos: **ne a commit üzenetekből dolgozz**, hanem a tényleges kódváltozásokból. Amit a diff mutat, azt írd le érthetően.

### 3. Magyar szöveg írása

Írj természetes, érthető magyar leírásokat. Ne fordítsd le gépiesen az angol kód/commit szövegeket — magyarázd el mit jelent a változás az end-user szempontjából.

Példák jó leírásra:

- ❌ "add rate limiting to auth endpoints" → ❌ "rate limiting hozzáadva az auth endpointokhoz"
- ✅ "Bevezetésre került a kérésszám-korlátozás a bejelentkezési végpontokon, hogy megakadályozza a brute-force támadásokat"

- ❌ "fix null pointer in user service"
- ✅ "Javítva egy összeomlást, ami akkor lépett fel, ha az end-user profilja nem tartalmazott e-mail címet"

### 4. Bejegyzés formátuma

```markdown
## [dátum] - [branch neve, opcionális]

### Új funkciók

- Leírás...

### Javítások

- Leírás...

### Egyéb változások

- Leírás...
```

- Dátum: mai nap, `YYYY-MM-DD` formátumban
- Csak azokat a szekciókat add hozzá, amikhez van tartalom
- Ha nincs semmi az adott kategóriában, hagyd ki a szekciót
- Listaelem max ~100 karakter, tömör de érthető

### 5. CHANGELOG.md frissítése

- Ha létezik `CHANGELOG.md`: az új bejegyzést a fájl **elejére** szúrd be (a legújabb legyen felül)
- Ha nem létezik: hozd létre az új bejegyzéssel
- Ne töröld a meglévő bejegyzéseket

A módosítás után írd ki a terminálba az elkészült bejegyzést, hogy a Fejlesztő lássa.
