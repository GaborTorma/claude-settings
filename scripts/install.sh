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
)

# Mappa marad valódi directory, fájlonként symlink. Más eszközök (pluginok)
# is dobhatnak ide saját fájlt.
DIR_FILE_SYMLINK_TARGETS=(
  "commands"
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

  # Árva linkek: a repóból törölt (vagy pluginba költözött) fájlok symlinkjei.
  local dst target
  for dst in "$dst_dir"/*; do
    [ -L "$dst" ] || continue
    target="$(readlink "$dst")"
    case "$target" in
      "$REPO_DIR"/*)
        [ -e "$target" ] || {
          rm "$dst"
          echo "Eltávolítva (a repóból törölve): $dst"
        }
        ;;
    esac
  done

  for src in "$src_dir"/*; do
    [ -e "$src" ] || continue
    link_one "$src" "$dst_dir/$(basename "$src")"
  done
}

# Korábbi telepítések maradványai: a repóra mutató symlinkek, amelyeknek már
# nincs dolguk. Idegen célra mutató linkhez nem nyúlunk.
drop_stale_link() {
  local dst="$1" why="$2"
  [ -L "$dst" ] || return 0
  case "$(readlink "$dst")" in
    "$REPO_DIR"/*)
      rm "$dst"
      echo "Eltávolítva ($why): $dst"
      ;;
  esac
}

# A settings.user.json managed drop-in fájlként symlinkelődik: a Claude Code
# ezt a szintet olvassa, de sosem írja, a listák (allow/deny) pedig összeadódnak
# a user settings-szel. Rendszerkönyvtár, ezért sudo kell.
managed_dropin_dir() {
  case "$(uname -s)" in
    Darwin) echo "/Library/Application Support/ClaudeCode/managed-settings.d" ;;
    Linux)  echo "/etc/claude-code/managed-settings.d" ;;
    *)      echo "" ;;
  esac
}

link_managed_settings() {
  local src="$REPO_DIR/settings.user.json"
  local dir; dir="$(managed_dropin_dir)"
  local dst="$dir/claude-settings.json"

  if [ -z "$dir" ]; then
    echo "Kihagyva (nem támogatott OS: $(uname -s)): managed settings drop-in"
    return
  fi

  if [ -L "$dst" ] && [ "$(readlink "$dst")" = "$src" ]; then
    return
  fi

  # Érvénytelen managed JSON-nal a Claude Code el sem indul.
  if ! python3 -m json.tool "$src" >/dev/null 2>&1; then
    echo "HIBA: érvénytelen JSON: $src — a managed symlink kihagyva."
    return
  fi

  if [ -t 0 ] && confirm "Managed settings symlink (sudo): $dst → $src?"; then
    sudo mkdir -p "$dir"
    sudo ln -sfn "$src" "$dst"
    echo "Symlink: $dst → $src"
  else
    echo
    echo "FIGYELEM: a permission-szabályok nem élnek. Futtasd:"
    echo "  sudo mkdir -p \"$dir\""
    echo "  sudo ln -sfn \"$src\" \"$dst\""
  fi
}

install_symlinks() {
  mkdir -p "$CLAUDE_DIR"
  # ~/.claude/settings.local.json nem settings-precedencia-szint; a permissions
  # helye a settings.user.json → managed settings drop-in.
  drop_stale_link "$CLAUDE_DIR/settings.local.json" "nem olvasott szint"
  # A pluginok a claude-plugins repóba költöztek, a marketplace git remote.
  drop_stale_link "$CLAUDE_DIR/local-plugins" "a pluginok külön repóban"

  for name in "${SYMLINK_TARGETS[@]}"; do
    link_one "$REPO_DIR/$name" "$CLAUDE_DIR/$name"
  done

  for dir in "${DIR_FILE_SYMLINK_TARGETS[@]}"; do
    link_dir_files "$REPO_DIR/$dir" "$CLAUDE_DIR/$dir"
  done

}

main() {
  install_symlinks
  link_managed_settings

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
