#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
CLAUDE_DIR="$HOME/.claude"
MARKER="# claude-settings auto-update"
UPDATE_CMD="bash \"$REPO_DIR/scripts/sync.sh\" --quiet 2>/dev/null || true"
HOOK_LINE="${MARKER}"$'\n'"${UPDATE_CMD}"

NO_HOOK=0
[ "${1:-}" = "--no-hook" ] && NO_HOOK=1

# Egész mappa-symlink ~/.claude alá. Csak ott, ahol minden fájl ebből a repóból
# jön (más eszköz nem ír bele).
SYMLINK_TARGETS=(
  "rules"
  "CLAUDE.md"
  "settings.local.json"
)

# Mappa marad valódi directory, fájlonként symlink. Más eszközök (pluginok)
# is dobhatnak ide saját fájlt.
DIR_FILE_SYMLINK_TARGETS=(
  "commands"
  "hooks"
)

detect_shell() { basename "${SHELL:-}"; }

rc_file_for() {
  case "$1" in
    zsh)  echo "$HOME/.zshrc" ;;
    bash) echo "$HOME/.bashrc" ;;
    fish) echo "$HOME/.config/fish/config.fish" ;;
    *)    echo "" ;;
  esac
}

confirm() {
  local answer
  read -r -p "$1 [i/N] " answer
  [[ "$answer" =~ ^[iI]$ ]]
}

install_hook() {
  local rc="$1"

  if [ -z "$rc" ]; then
    echo "Ismeretlen shell: $SHELL — add hozzá manuálisan:"
    echo "  $UPDATE_CMD"
    exit 1
  fi

  mkdir -p "$(dirname "$rc")"

  if grep -qF "$MARKER" "$rc" 2>/dev/null; then
    local current
    current="$(awk -v m="$MARKER" 'f{print; exit} index($0,m){f=1}' "$rc")"
    if [ "$current" = "$UPDATE_CMD" ]; then
      echo "Hook naprakész: $rc"
      return
    fi

    local tmp; tmp="$(mktemp)"
    awk -v m="$MARKER" 'index($0,m){skip=2} skip>0{skip--; next} {print}' "$rc" > "$tmp"
    mv "$tmp" "$rc"
    printf '\n%s\n' "$HOOK_LINE" >> "$rc"
    echo "Hook frissítve: $rc"
    return
  fi

  printf '\n%s\n' "$HOOK_LINE" >> "$rc"
  echo "Hook hozzáadva: $rc"
}

link_one() {
  local src="$1" dst="$2"

  if [ ! -e "$src" ]; then
    echo "Kihagyva (nem létezik a repóban): $src"
    return
  fi

  mkdir -p "$(dirname "$dst")"

  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    return
  fi

  if [ -e "$dst" ] || [ -L "$dst" ]; then
    if confirm "Létezik: $dst — felülírjam symlink-kel?"; then
      rm -rf "$dst"
    else
      echo "Kihagyva: $dst"
      return
    fi
  fi

  ln -s "$src" "$dst"
  echo "Symlink: $dst → $src"
}

link_dir_files() {
  local src_dir="$1" dst_dir="$2"

  if [ ! -d "$src_dir" ]; then
    echo "Kihagyva (nem mappa a repóban): $src_dir"
    return
  fi

  # Migráció: korábbi egész-mappa-symlinket cseréljük valódi mappára.
  if [ -L "$dst_dir" ]; then
    local current_target; current_target="$(readlink "$dst_dir")"
    if [ "$current_target" = "$src_dir" ] \
       || confirm "Létezik mappa-symlink: $dst_dir → $current_target. Felülírjam valódi mappára?"; then
      rm "$dst_dir"
    else
      echo "Kihagyva: $dst_dir"
      return
    fi
  fi

  mkdir -p "$dst_dir"

  for src in "$src_dir"/*; do
    [ -e "$src" ] || continue
    link_one "$src" "$dst_dir/$(basename "$src")"
  done
}

install_symlinks() {
  mkdir -p "$CLAUDE_DIR"

  for name in "${SYMLINK_TARGETS[@]}"; do
    link_one "$REPO_DIR/$name" "$CLAUDE_DIR/$name"
  done

  for dir in "${DIR_FILE_SYMLINK_TARGETS[@]}"; do
    link_dir_files "$REPO_DIR/$dir" "$CLAUDE_DIR/$dir"
  done

  # Plugin marketplace: a repo plugins/ mappáját ~/.claude/local-plugins-be
  # symlinkeljük (mivel ~/.claude/plugins/ a Claude Code saját mappája).
  link_one "$REPO_DIR/plugins" "$CLAUDE_DIR/local-plugins"
}

main() {
  install_symlinks

  if [ "$NO_HOOK" -eq 1 ]; then
    echo "Kész (shell rc érintetlen — --no-hook)."
    return
  fi

  local shell rc
  shell="$(detect_shell)"
  rc="$(rc_file_for "$shell")"

  echo "Shell: $shell"
  install_hook "$rc"
  echo "Kész."
}

main "$@"
