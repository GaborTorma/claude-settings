#!/usr/bin/env bash
# Update: fast-forward pull a remote-ról, majd reinstall (csak ha HEAD elmozdult).
# Nem pushol és nem rebase-el: divergenciánál vagy ütközésnél megáll, semmit nem
# dob el.
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_DIR"

upstream=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || true)
if [ -z "$upstream" ]; then
  echo "update: nincs upstream — kihagyva."
  exit 0
fi

git fetch --quiet

behind=$(git rev-list --count "HEAD..$upstream")
if [ "$behind" -eq 0 ]; then
  echo "Up to date — install kihagyva."
  exit 0
fi

# A settings.user.json managed drop-in-ként él: érvénytelen JSON-nal a Claude
# Code el sem indul, ezért ilyen remote állapotot nem húzunk le.
if ! git show "$upstream:settings.user.json" | python3 -m json.tool >/dev/null 2>&1; then
  echo "update: a remote settings.user.json érvénytelen JSON — pull kihagyva." >&2
  exit 1
fi

if ! git pull --ff-only --quiet; then
  echo "update: nem fast-forward (lokális, nem pusholt commit vagy ütköző változás)." >&2
  echo "update: oldd fel kézzel: cd $REPO_DIR && git status" >&2
  exit 1
fi

echo "update: pull OK ($behind commit)."
make -C "$REPO_DIR" install
