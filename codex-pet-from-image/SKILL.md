---
name: codex-pet-from-image
description: Create a usable Codex custom pet from one provided reference image, then validate and deploy it into ~/.codex/pets. Use when the user gives a character image, sticker, mascot, anime chibi, or other visual reference and wants an installable Codex pet rather than a standalone illustration.
---

# Codex Pet From Image

## Overview

This skill turns one reference image into a deployable Codex pet package. It uses the reference image as the identity lock, generates a clean base image, enlarges and tightens the reference cutout, creates all 9 required animation rows with `imagegen`, removes chroma-key backgrounds from decoded row strips, validates the atlas, and installs the result into `~/.codex/pets/<pet-id>/`.

Default assumption: the user wants execution, not a plan. When enough information is present, perform the full workflow end to end.

## When To Use

Trigger this skill when the user:

- provides a character image and wants a Codex pet
- asks to convert a sticker, chibi illustration, mascot, anime character, or OC into a Codex pet
- wants to replace an existing Codex pet with a new image-based version
- wants a full `pet.json + spritesheet.webp` package deployed into the local Codex pet folder

Do not use this skill for:

- simple web demos or draggable HTML mascots
- vector/icon extension work
- generic image editing that is not meant to become a Codex pet

## Workflow

### 1. Establish the source of truth

- Use the user-provided image as the primary identity reference.
- Ask for a pet name only if the user did not give one and a safe default would be awkward.
- Prefer a short stable slug such as `frieren-chibi`.
- Work inside the current project workspace unless the user asks for a different location.

### 2. Create a clean base character

- Use built-in `image_gen` first.
- Recreate only the character in the exact supplied style.
- Remove decorative sticker borders, bubble outlines, text, and detached sparkles unless the user explicitly wants them in the pet.
- Generate on a perfectly flat `#00ff00` chroma-key background.
- Save the generated source image into the workspace and remove the background with:

```bash
python "${HOME}/.codex/skills/.system/imagegen/scripts/remove_chroma_key.py" \
  --input <source.png> \
  --out <cutout.png> \
  --auto-key border \
  --soft-matte \
  --transparent-threshold 12 \
  --opaque-threshold 220 \
  --despill
```

- Then enlarge and tighten the cleaned cutout so the reference character is not too small:

```bash
python scripts/prepare_reference_cutout.py \
  --input <cutout.png> \
  --output <cutout-prepared.png> \
  --scale 1.25
```

- Treat the prepared cutout as the reference-of-record for the pet run.
- Default target: the reference character should read roughly `1.2x–1.3x` larger than a conservative first pass.

### 3. Prepare the pet run

- Use the bundled helper:

```bash
bash scripts/create_pet_run.sh \
  --pet-name "<display name>" \
  --pet-id "<pet-id>" \
  --description "<one sentence>" \
  --reference "<absolute path to cutout-prepared.png>" \
  --output-dir "<absolute run dir>"
```

- The created run directory will contain:
  - `pet_request.json`
  - `imagegen-jobs.json`
  - `prompts/base-pet.md`
  - `prompts/rows/*.md`
  - `references/layout-guides/*.png`

### 4. Record the base job

- Record the original built-in `imagegen` base output with the official recorder, not by hand-editing manifests.
- Use the helper:

```bash
python scripts/record_latest_imagegen_result.py \
  --run-dir "<absolute run dir>" \
  --job-id base
```

### 5. Generate all 9 action rows

Required rows:

- `idle`
- `running-right`
- `running-left`
- `waving`
- `jumping`
- `failed`
- `waiting`
- `running`
- `review`

For each row:

- Read the exact row prompt from `prompts/rows/<state>.md`.
- Attach:
  - the original reference image
  - `decoded/base.png`
  - the matching layout guide
- Use built-in `image_gen` to generate one row strip.
- In every row-generation prompt, explicitly require the character to occupy more of each slot:
  - target roughly `72%–84%` of frame height
  - avoid tiny character scale
  - keep full body visible with safe padding
- Then record it with:

```bash
python scripts/record_latest_imagegen_result.py \
  --run-dir "<absolute run dir>" \
  --job-id "<state>"
```

Rules:

- Do not skip rows.
- Do not use local drawing code to fake rows.
- Do not mirror `running-right` into `running-left` by default. Generate `running-left` as its own row unless the user explicitly asks to optimize for speed over fidelity.
- Keep the user’s reference style, even when it is more polished than the default Codex pixel-pet house style.
- If a row comes back visually too small, regenerate that row before finalization instead of accepting it.

### 6. Finalize and package

- Before finalization, strip chroma-key green from all decoded row strips:

```bash
python scripts/clean_decoded_rows.py \
  --run-dir "<absolute run dir>"
```

- After all jobs are complete, finalize with:

```bash
python "${HOME}/.codex/vendor_imports/skills/skills/.curated/hatch-pet/scripts/finalize_pet_run.py" \
  --run-dir "<absolute run dir>" \
  --skip-videos \
  --allow-slot-extraction \
  --package-dir "<absolute run dir>/package"
```

- Inspect:
  - `qa/contact-sheet.png`
  - `qa/review.json`
  - `final/validation.json`

Block acceptance if:

- the face drifts away from the reference
- the hair, staff, or outfit changes materially across rows
- green chroma-key background is still visible behind the character in contact-sheet frames
- the character reads too small relative to the frame
- detached effects appear
- any frame is clipped or bleeds into another slot

### 7. Deploy into the Codex pet folder

- Install only after packaging succeeded.
- Use the helper:

```bash
bash scripts/install_packaged_pet.sh \
  --package-dir "<absolute run dir>/package" \
  --pet-id "<pet-id>"
```

- Final deployment target:

```text
${CODEX_HOME:-$HOME/.codex}/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

## Fast Execution Pattern

When the user gives one image and says “make this into a Codex pet,” execute in this order:

1. Generate clean base image from the reference.
2. Remove the chroma-key background locally.
3. Enlarge and tighten the cutout reference.
4. Prepare the pet run.
5. Record `base`.
6. Generate and record every row in order:
   `idle`, `running-right`, `running-left`, `waving`, `jumping`, `failed`, `waiting`, `running`, `review`.
7. Clean decoded rows, finalize, inspect contact sheet, package, and install.

## Resources

### scripts/

- `create_pet_run.sh`
  Wrapper around the official `prepare_pet_run.py`.
- `prepare_reference_cutout.py`
  Crops transparent edges and scales the cleaned cutout up to a stronger default reference size.
- `record_latest_imagegen_result.py`
  Records the newest built-in `imagegen` output into a chosen pet job.
- `clean_decoded_rows.py`
  Removes chroma-key green from decoded row strips before frame extraction and atlas composition.
- `install_packaged_pet.sh`
  Deploys a packaged pet into `~/.codex/pets/<pet-id>/`.

### references/

- `project-summary.md`
  Compact summary of the working pattern derived from this project, including what made the image-based pet path succeed.
