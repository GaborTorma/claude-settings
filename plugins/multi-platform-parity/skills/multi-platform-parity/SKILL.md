---
name: multi-platform-parity
description: Egy app több kliens-platformjának (PWA, iOS, iPad, watchOS, Android, desktop) verzió- és feature-paritásának fenntartása. Használd amikor a felhasználó ugyanazon app több platformján dolgozik — feature-t implementál EGY platformra, verziót/release-t koordinál, azt kérdezi "szinkronban vannak-e a platformok", PARITY.md-ről / feature-mátrixról, shared core-ról, API backward compat-ról régi kliensekkel, vagy app-store review skew-ról beszél. Akkor is, ha nem mondja ki a "parity" szót.
---

# Multi-platform parity

Cél több-platformos appnál: **azonos képesség** minden cél-platformon, idiomatikus natív UX-szel. A divergencia legyen **szándékos és dokumentált**, sosem véletlen drift.

## Mikor aktiválódj

A repo több kliens-platformot tartalmaz ugyanarra az appra (pl. `apps/web/` vagy `pwa/` PWA + `ios/` + `android/` + watch target), VAGY a felhasználó egy platformra implementál és a többi érintett. Ekkor a paritás **passzív felelősséged**: ha egy változás szétcsúsztatná a platformokat, jelezd — ne hagyd csendben.

## 1. Verzió- és release-koordináció

- **Egy verzió-forrás**: a SemVer single-source (`versioning.md`) generálja minden platform marketing-verzióját — iOS `CFBundleShortVersionString`, Android `versionName`, PWA `manifest`. Csak `buildNumber`/`versionCode` térhet el platformonként.
- **Store-lag tény**: iOS/Android review napokig tart, PWA instant → a release nem megy egyszerre élesbe; a rollout-ablakban több kliensverzió él egyszerre.
- **Forced-update gate**: backend `minSupportedVersion`; régi kliensnek feature-specifikus elutasítás + natív forced-update UX.
- **Breaking-et ne deploy-olj előre**: a backend/PWA a leglassabb platform rollout-jához igazodjon (canary → teljes).
- **PWA service worker = verziózott kliens**: a cache-elt bundle a store-lag analógja. Verzió-bélyegzett SW + explicit frissítés (`skipWaiting`+`clients.claim`, vagy waiting+user-prompt reload); a `minSupportedVersion` gate a stale bundle-t is zárja.

## 2. Shared core architektúra

- **Logika a core-ba**: validáció (`zod`), üzleti szabály, állapotgép, formázás, design token CSAK shared core-ban (`packages/`, `shared/`, `core/`). Új platform előtt `grep`/`Glob` — ne duplikáld.
- **Hova tartozik?**: platform-független számítás/szabály/formázás → core; valódi natív (UI render, navigáció, OS API, permission) → platform-réteg. Kétségnél core. watchOS: a megjelenítés natív, az **adat** a core-ból jön.
- **Pinnelt közös core**: minden platform ugyanazt a core-verziót/SHA-t pinneli; eltérő pin → rejtett parity-drift.
- **Anti-pattern azonnal jelezd**: logika a platform-rétegben → javasold a core-ba emelést, ne másold csendben a másik platformra.

## 3. API/séma single-source + backward compat

- **Séma a single source of truth**: `zod`/OpenAPI/protobuf egy helyen, kliens-típusok **generálva**. Generált fájlt kézzel ne szerkessz; sorrend séma → codegen → handler.
- **Additív változás**: új mező opcionális + default. Kötelező mező / törlés / átnevezés breaking → strict natív decoder (Swift `Codable`, Kotlin data class) elhasal.
- **Breaking → verziózz, ne törölj**: `/v2` vagy mezőszintű a régi mellett, közös handler + verzió-adapter (ne copy-paste endpoint). Tartsd a régi szerződést, amíg a leglassabb platform (a stale PWA-bundle is) fel nem zárkózik.
- **Verzió-tudatos válasz**: kliens-verzió (header) szerint trimmeld a választ, ne küldj olyat ami a régi parsert töri. Contract/snapshot teszt rögzítse a sémát, bukása blokkolja a commitot (`git.md` pre-commit gate).

## 4. Feature/UX parity + szándékos divergencia

- **`feature flag`, ne hard-fork**: flag-definíció a core-ban egy helyen, remote-vezérelt (offline-ra cache-elhető, pl. watchOS) → a parity-állapot kódból auditálható és kill-switch-elhető. Build-time flag tilos.
- **Tiszteld a natív konvenciót** (HIG, Material, watchOS glanceable, iPad multitasking, PWA offline/installable): azonos képesség, idiomatikus interakció — pixel-egyezést ne hajszolj. Redukált belépési pont (watch complication) vagy platform-extra (widget) hiánya nem parity-bug.

## 5. PARITY.md, DoD, divergencia-napló

- **`PARITY.md` a repo gyökerében**: sor = feature, oszlop = platform, cella `✅/🚧/❌/➖` + eltérésnél a **MIÉRT** egy mondatban (HIG, hardver-limit, store-policy). Feature-rel egy körben frissítsd; parity-kérdésnél ELŐSZÖR ezt olvasd, ne a kliensek kódjából találgass.
- **DoD = minden cél-platform**: a feature kész, ha mindenhol zöld (lint/typecheck/test, `git.md`) VAGY `PARITY.md`-ben explicit kivétel (ok + visszazárási trigger: dátum/verzió/„store-jóváhagyás után"). Store-csúszás `🗓️`, nem `➖`. Néma rés tilos.
- **Egy platform előtt kérdezz** (`AskUserQuestion`): a többi érintett platform most menjen, vagy ütemezett skew? A platform-érintettség intent/prioritás → user dönt; a kód-tényt (hol van már meg) `grep`/`Read` olvassa ki (`exploration.md`).
- **Közös acceptance + fixtures**: platform-független `Given/When/Then` + nyelvfüggetlen fixture-forrás (JSON/YAML), amit minden suite beolvas. Bugfix → reprodukáló teszt (`karpathy`), majd a TÖBBI platformon is ellenőrizd.
- **Repo-struktúra** (`claude.md`): platform-alrész saját `CLAUDE.md` a build/version/release paranccsal; a root a core-határt és a parity-forrást dokumentálja, ne ismételd.

## Feature-checklist (futtasd amikor új feature készül)

1. **Core?** A platform-független logika a shared core-ba került, nem egy platform-rétegbe.
2. **Séma?** Ha új API-mező/endpoint kell → séma single-source frissítve, kliens-típusok újragenerálva, additív (vagy verziózott, ha breaking).
3. **Platform-lista** — sorold fel az ÉRINTETT cél-platformokat. Amelyik most nem készül el → `AskUserQuestion`: együtt menjen vagy ütemezett skew?
4. **Flag?** Ha fokozatos/platformonként eltérő bevezetés → `feature flag` a core-ban, nem hard-fork.
5. **`PARITY.md`** frissítve: az új sor + platformonkénti cella + eltérés indoka.
6. **DoD**: minden cél-platformon zöld VAGY explicit, indokolt + visszazárási-triggeres kivétel a `PARITY.md`-ben.

## `PARITY.md` sablon

A scaffold: [assets/PARITY.template.md](../../assets/PARITY.template.md) — ezt írja ki a `multi-platform-parity:init` command (oszlop = felderített platform, sor = feature-leltár).

**Megjegyzés**: eszköz, nem dogma — egyetlen platformnál ne építs platform-adaptert/plugin-réteget kérés nélkül (`karpathy`). A parity-t a megosztott logika adja, nem a keretrendszer.
