#!/usr/bin/env bash
set -euo pipefail

PACKAGE_DIR=""
PET_ID=""
CODEX_HOME_DIR="${CODEX_HOME:-$HOME/.codex}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --package-dir) PACKAGE_DIR="$2"; shift 2 ;;
    --pet-id) PET_ID="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$PACKAGE_DIR" || -z "$PET_ID" ]]; then
  echo "package-dir and pet-id are required" >&2
  exit 2
fi

TARGET_DIR="$CODEX_HOME_DIR/pets/$PET_ID"
mkdir -p "$TARGET_DIR"
cp "$PACKAGE_DIR/pet.json" "$TARGET_DIR/pet.json"
cp "$PACKAGE_DIR/spritesheet.webp" "$TARGET_DIR/spritesheet.webp"
echo "$TARGET_DIR"
