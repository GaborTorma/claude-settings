# Environment

- **Minden env-specifikus beállítás `.env`-be.** (Pl.: API key, host, port, DB URL, secret, feature flag).
- **Commit**: `.env.example` placeholder értékekkel.
- **Validálás**: a kötelező env-változók egy helyen, séma alapján, induláskor vagy buildkor;
  hiányzó vagy hibás érték → azonnali hiba. A szerver- és a kliensoldali változók külön kezelendők.
- **Szerver-titok** kliensoldalra nem kerülhet.
- **`.gitignore`**: `.env`, `.env.*`, `credentials.json`, `*.pem`, `*.key`, `!.env.example`.
- **Bootstrap**: `.env.example` + `.gitignore` az első commit része.
