---
date: 2026-09-22
source: claude-settings (korábban rules/versioning.md)
kind: skill
deferred: 2026-09-22
---

**Miért halasztva**: a rule 2026-04-26 óta élt, mégis alig történt release.
Felmérés (2026-09-22, `~/Development/Claude`):

- `revolut`: release-it + CHANGELOG, 6 tag — az utolsó 2026-04-30, utána leállt.
- `package-monitor`: release-it konfigurálva, 0 tag — sosem futott.
- `auto-bpm`: 16 tag, kézzel (iOS).
- `claude-plugins`: `plugin.json` verziók léptek, 0 tag (a `/curate` tag-lépése kimarad).
- Manas2026, MicrOasis2026, varazskez, Torma.AI: nincs setup.

Okok, amiket a döntésnél kezelni kell:

1. **Nincs trigger**: a rule leírja, *mi* a release, de nem *mikor*; a
   „manuális” miatt az *AI* sosem hozza fel. Javaslat: a
   `/commit-push-pr-merge` végén release-javaslat, ha van `feat`/`fix` az
   utolsó tag óta.
2. **Bootstrapból hiányzik**: a `git.md` „Új projekt” lépései nem említik a
   release-setupot.
3. **iOS / monorepo nincs lefedve**: mi a verzió forrása (`package.json` vs
   `CFBundleShortVersionString` vs közös szám), build-számozás — ez inkább az
   `apple` / `multi-platform-parity` pluginba való.

# Verziókezelés

- **Séma**: SemVer (`MAJOR.MINOR.PATCH`).
- **Tag**: `v1.2.3` tag (`git push --tags`)
- **`CHANGELOG.md`**: tooling generálja.
- **Release**: **manuális, helyi**, nem CI auto-release!

## Node — `release-it` + `@release-it/conventional-changelog`

- Dev dep
- `.release-it.json`:
   - `tagName: v${version}`
   - `npm.publish: false` default
   - `github.release: true`
   - plugin preset `conventionalcommits`
- `package.json` script:
   - `"release": "release-it"`.

## Python — `commitizen`

- Dev dep
- `pyproject.toml`
   - `[tool.commitizen]`
      - `version_provider = "pep621"`
      - `tag_format = "v$version"`
      - `update_changelog_on_bump = true`
- `[project] version` a single source.
