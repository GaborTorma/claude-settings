---
date: 2026-09-26
source: git-graph
kind: rule
---

**Mi**: minden reverse-DNS azonosító prefixe `ai.torma.`, sosem `co.torma.`
(vagy bármi más). Ide tartozik: launchd label, macOS/iOS Bundle ID, Java/Kotlin
package, Android applicationId, és minden egyéb csomag-domain.

**Miért**: a git-graph launchd agentje `co.torma.gitgraph` néven jött létre,
és a Fejlesztő átneveztette `ai.torma.git-graph`-ra. A saját domain az
`ai.torma` — a `co.torma` egy *AI*-kitalálta alapérték volt, nem döntés.

**Hogyan alkalmazd**:
- Új azonosítónál kérdezés nélkül `ai.torma.<projekt-név>` (a projekt-rész
  kebab-case ott, ahol a formátum engedi — pl. `ai.torma.git-graph`; Bundle
  ID-nál és Java package-nél a platform szabálya szerint).
- Meglévő `co.torma.*` azonosítót nem nevezel át magadtól, de jelezd. Átnevezésnél
  a régit is takarítsd el: launchd-nél a régi agent `launchctl bootout` + a régi
  plist törlése, különben a következő bejelentkezéskor a régi is elindul
  (git-graph-nál ugyanazért a portért versenyzett volna a kettő).
