#!/usr/bin/env bash
set -euo pipefail

PET_NAME=""
PET_ID=""
DESCRIPTION=""
REFERENCE=""
OUTPUT_DIR=""
DISPLAY_NAME=""
PET_NOTES=""
STYLE_NOTES=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --pet-name) PET_NAME="$2"; shift 2 ;;
    --pet-id) PET_ID="$2"; shift 2 ;;
    --display-name) DISPLAY_NAME="$2"; shift 2 ;;
    --description) DESCRIPTION="$2"; shift 2 ;;
    --reference) REFERENCE="$2"; shift 2 ;;
    --output-dir) OUTPUT_DIR="$2"; shift 2 ;;
    --pet-notes) PET_NOTES="$2"; shift 2 ;;
    --style-notes) STYLE_NOTES="$2"; shift 2 ;;
    *) echo "Unknown arg: $1" >&2; exit 2 ;;
  esac
done

if [[ -z "$REFERENCE" || -z "$OUTPUT_DIR" ]]; then
  echo "reference and output-dir are required" >&2
  exit 2
fi

python3 "${HOME}/.codex/vendor_imports/skills/skills/.curated/hatch-pet/scripts/prepare_pet_run.py" \
  --pet-name "$PET_NAME" \
  --pet-id "$PET_ID" \
  --display-name "$DISPLAY_NAME" \
  --description "$DESCRIPTION" \
  --reference "$REFERENCE" \
  --output-dir "$OUTPUT_DIR" \
  --pet-notes "$PET_NOTES" \
  --style-notes "$STYLE_NOTES" \
  --force
