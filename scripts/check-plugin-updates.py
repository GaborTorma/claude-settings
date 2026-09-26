#!/usr/bin/env python3
"""Telepített Claude Code pluginok elavultság-ellenőrzése.

Read-only: frissíti a marketplace-katalógusokat (metaadat), de plugint nem
telepít és nem töröl. A kimenet első sora STATUS: OK vagy STATUS: TEENDO.

A katalógus háromféleképpen mondja meg, mi az elérhető verzió — mindhármat
kezelni kell:
  1. `version` mező a marketplace.json-ben          → közvetlen összevetés
  2. path-forrás (./plugins/x)                      → a klónban lévő plugin.json
  3. url-forrás `sha` pinnel                        → a pinelt commit plugin.json-ja
A 2. eset verzió nélkül is előfordul (a telepített "verzió" ilyenkor commit-sha):
ott a cache és a katalógus mappájának tartalmi diffje dönt.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

PLUGINS = Path.home() / ".claude" / "plugins"
CACHE = PLUGINS / "cache"
MARKETPLACES = PLUGINS / "marketplaces"
HTTP_TIMEOUT = 20


def claude_bin() -> str | None:
    """A PATH ütemezett futásnál szűkebb lehet, mint interaktív shellben."""
    if found := shutil.which("claude"):
        return found
    for p in (Path.home() / ".local/bin/claude", Path("/usr/local/bin/claude"), Path("/opt/homebrew/bin/claude")):
        if p.exists():
            return str(p)
    return None


def refresh_catalogs() -> str:
    """Katalógus-szinkron. Enélkül a verzió-összevetés elavult adaton dolgozna."""
    exe = claude_bin()
    if not exe:
        return "! a claude CLI nem található, a katalógusok a korábbi állapotukon maradtak"
    try:
        r = subprocess.run(
            [exe, "plugin", "marketplace", "update"],
            capture_output=True, text=True, timeout=180,
        )
        return (r.stdout.strip().splitlines() or ["(nincs kimenet)"])[-1] if r.returncode == 0 \
            else f"! katalógus-frissítés sikertelen: {r.stderr.strip()[:200]}"
    except subprocess.TimeoutExpired:
        return "! katalógus-frissítés időtúllépés"


def load_catalog() -> dict[tuple[str, str], dict]:
    out: dict[tuple[str, str], dict] = {}
    for mp in sorted(p.name for p in MARKETPLACES.iterdir() if p.is_dir()):
        f = MARKETPLACES / mp / ".claude-plugin" / "marketplace.json"
        if not f.exists():
            continue
        for entry in json.loads(f.read_text()).get("plugins", []):
            out[(mp, entry["name"])] = entry
    return out


def remote_version(repo_url: str, ref: str) -> str | None:
    repo = repo_url.replace("https://github.com/", "").removesuffix(".git")
    url = f"https://raw.githubusercontent.com/{repo}/{ref}/.claude-plugin/plugin.json"
    try:
        with urllib.request.urlopen(url, timeout=HTTP_TIMEOUT) as r:
            return json.loads(r.read()).get("version")
    except (urllib.error.URLError, json.JSONDecodeError, TimeoutError, OSError):
        return None


def dirs_differ(a: Path, b: Path) -> bool:
    """Sha-verziós pluginoknál a tartalom dönt. A .in_use a Claude Code markere."""
    r = subprocess.run(["diff", "-rq", str(a), str(b)], capture_output=True, text=True)
    return any(".in_use" not in line for line in r.stdout.splitlines() if line.strip())


def available(mp: str, entry: dict) -> tuple[str | None, str]:
    if entry.get("version"):
        return entry["version"], "katalógus"
    src = entry.get("source")
    if isinstance(src, str) and src.startswith("."):
        f = (MARKETPLACES / mp / src / ".claude-plugin" / "plugin.json").resolve()
        # Verzió nélküli plugin.json (vagy hiányzó manifest) esetén a telepített
        # "verzió" commit-sha — ilyenkor csak a tartalom összevetése mond igazat.
        if f.exists() and (v := json.loads(f.read_text()).get("version")):
            return v, "path"
        return None, "path-sha"
    if isinstance(src, dict) and src.get("url"):
        return remote_version(src["url"], src.get("sha", "HEAD")), "pin"
    return None, "?"


def orphans() -> list[tuple[str, str]]:
    found = []
    for marker in CACHE.glob("*/*/*/.orphaned_at"):
        d = marker.parent
        size = subprocess.run(["du", "-sh", str(d)], capture_output=True, text=True).stdout.split("\t")[0]
        found.append((size.strip(), str(d.relative_to(CACHE))))
    return sorted(found, key=lambda x: x[1])


def main() -> int:
    installed = json.loads((PLUGINS / "installed_plugins.json").read_text())["plugins"]
    catalog_note = refresh_catalogs()
    catalog = load_catalog()

    outdated: list[dict] = []
    unknown: list[str] = []

    for key, entries in sorted(installed.items()):
        name, _, mp = key.partition("@")
        entry = catalog.get((mp, name))
        for inst in entries:
            have = inst.get("version")
            hit = {
                "id": f"{name}@{mp}",
                "scope": inst.get("scope", "user"),
                "project": inst.get("projectPath"),
            }
            if entry is None:
                unknown.append(f"{name}@{mp}: nincs a katalógusban (telepítve: {have})")
                continue
            avail, kind = available(mp, entry)
            if kind == "path-sha":
                cache_dir = Path(inst["installPath"])
                cat_dir = (MARKETPLACES / mp / entry["source"]).resolve()
                if cache_dir.is_dir() and cat_dir.is_dir() and dirs_differ(cache_dir, cat_dir):
                    outdated.append(hit | {"change": "a katalógus tartalma eltér a telepítettől"})
                continue
            if avail is None:
                unknown.append(f"{name}@{mp}: az elérhető verzió nem volt lekérdezhető (hálózat?)")
            elif avail != have:
                outdated.append(hit | {"change": f"{have} → {avail}"})

    orphan_list = orphans()

    print("STATUS:", "TEENDO" if outdated else "OK")
    print(f"# {catalog_note}")
    print()

    if outdated:
        print(f"ELAVULT ({len(outdated)}):")
        for hit in outdated:
            print(f"  - {hit['id']} ({hit['scope']}): {hit['change']}")
        print()
        print("Frissítés:")
        for hit in outdated:
            if hit["scope"] == "project":
                # A project scope ahhoz a könyvtárhoz tartozik, ahonnan telepítve lett.
                print(f"  cd {hit['project'] or '<projekt>'} && claude plugin update {hit['id']} -s project")
            else:
                print(f"  claude plugin update {hit['id']}")
        print()
    else:
        print("Minden telepített plugin naprakész.")
        print()

    if unknown:
        print("NEM ELLENŐRIZHETŐ:")
        for line in unknown:
            print(f"  - {line}")
        print()

    if orphan_list:
        print(f"HASZNÁLATON KÍVÜLI CACHE ({len(orphan_list)}):")
        for size, path in orphan_list:
            print(f"  {size:>6}  {path}")
        print("  takarítás: find ~/.claude/plugins/cache -mindepth 4 -maxdepth 4 "
              "-name .orphaned_at -print0 | xargs -0 -n1 dirname | xargs rm -rf")
        print()

    return 1 if outdated else 0


if __name__ == "__main__":
    sys.exit(main())
