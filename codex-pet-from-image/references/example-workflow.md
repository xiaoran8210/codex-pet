# Example Workflow

This is the standard flow for turning one image into an installed Codex pet.

## 1. Provide a Reference Image

Give Codex one clear character image and a desired pet name if you have one.

Example prompt:

```text
Use $codex-pet-from-image to make this image into a Codex pet named fern-chibi.
```

Good reference images are:

- full-body or near full-body
- visually consistent
- already close to the style you want
- free of heavy text overlays or large decorative frames

## 2. Base Character Cleanup

The skill first creates a clean base character image:

- same visual identity as the reference
- decorative borders and detached effects removed
- generated on chroma-key green
- background removed locally
- transparent cutout cropped and enlarged to about `1.25x`

This prepared cutout becomes the source of truth for the rest of the run.

## 3. Pet Run Preparation

The skill prepares a standard `hatch-pet` workspace containing:

- `pet_request.json`
- `imagegen-jobs.json`
- `prompts/base-pet.md`
- `prompts/rows/*.md`
- `references/layout-guides/*.png`

## 4. Generate the 9 Required Rows

The skill generates and records all required rows:

- `idle`
- `running-right`
- `running-left`
- `waving`
- `jumping`
- `failed`
- `waiting`
- `running`
- `review`

Each row is generated from:

- the original user reference
- the cleaned base image
- the matching layout guide

The prompts explicitly push for a larger on-frame character so the pet does not read too small.

## 5. Cleanup and Finalize

Before packaging, the skill removes green chroma leakage from decoded row strips.

Then it finalizes the run and validates:

- contact sheet quality
- frame extraction
- final atlas structure
- packaged `pet.json`
- packaged `spritesheet.webp`

The workflow allows slot-based extraction when that produces cleaner results than component-only extraction.

## 6. Deploy

When validation passes, the pet is installed to:

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

## What Success Looks Like

A successful run should give you:

- a stable character identity across rows
- no visible green background in the final contact sheet
- no clipped limbs, staff, hair, or accessories
- a character that reads large enough in each frame
- a ready-to-use pet in the local Codex pet repository

## Publishing Note

If you plan to publish your generated pet assets publicly, make sure you have the right to redistribute the character art. The workflow itself is safe to publish, but bundled character packs may require additional permission.
