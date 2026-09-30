---
name: issues
description: A projekt nyitott GitHub issue-inak listája címke szerint, majd kérdés a folytatásról. Használd amikor a Fejlesztő /issues-t ír, vagy azt kérdezi, milyen teendők vannak a projektben.
allowed-tools: Bash(gh issue list *)
---

## Kontextus

- Issue-k: !`gh issue list --state open --limit 50 --json number,title,labels,url || true`

Hiba (nincs remote, nincs `gh` auth) → mutasd a hibát és állj meg. Üres lista → csak
ennyi: `Nincs nyitott issue.`

## 1. Lista

A sessionbe, címke szerint csoportosítva (`feature`, `fix`, címke nélkül), a csoporton
belül szám szerint:

```markdown
**feature**

- [#<szám>](<URL>) · <cím>

**fix**

- [#<szám>](<URL>) · <cím>
```

## 2. Kérdés

`AskUserQuestion`, header: `Folytatás`, kérdés: „Hogy folytassuk?”. Az opciók az
issue-k, a `label`: `#<szám> · <cím>`; a `description` egy rövid mondat, a javasoltnál
`Javasolt — ` kezdettel. 4 opció a határ — ami nem fér bele, `Folytatás 2` kérdésbe
kerül; egy hívásban legfeljebb 4 kérdés.

A választott issue-ra: `/pick #<szám>`.
