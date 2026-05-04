# codex-pet

[中文说明](./README.zh-CN.md)

Turn a single reference image into a usable Codex custom pet, then install it directly into `~/.codex/pets/<pet-id>/`.

This repository packages a reusable Codex skill that turns a character image into a validated, deployable Codex pet atlas.

## Preview

### Frieren-style example

![Frieren contact sheet](./docs/assets/frieren-contact-sheet.png)

### Fern-style example

![Fern contact sheet](./docs/assets/fern-contact-sheet.png)

## What This Repository Includes

- `codex-pet-from-image/`
  A reusable Codex skill for image-to-pet generation
- `codex-pet-from-image/scripts/`
  Small helpers for run setup, cutout preparation, cleanup, recording, and install
- `codex-pet-from-image/references/`
  Compact notes and a worked example workflow

## What The Skill Does

`codex-pet-from-image` will:

- use one user-provided image as the identity reference
- recreate a clean base character image in the same style
- remove the background and tighten the cutout
- enlarge the prepared reference so the character does not end up too small
- prepare a standard `hatch-pet` run
- generate all 9 required animation rows with `imagegen`
- clean chroma-key green from decoded row strips before packaging
- validate the atlas and package it as a Codex pet
- deploy the finished pet into `~/.codex/pets/<pet-id>/`

## Why This Exists

The built-in pet pipeline is powerful, but the image-to-pet path usually needs a few practical fixes:

- reference characters often come out too small
- green chroma backgrounds can leak into intermediate rows
- some high-quality generations work better with slot-based extraction than component-only extraction

This repository packages those fixes into one repeatable workflow.

## Installation

Copy the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-from-image ~/.codex/skills/codex-pet-from-image
```

After that, you can call it from any Codex conversation.

## Quick Start

Attach a reference image and say:

```text
Use $codex-pet-from-image to turn this reference image into an installed Codex pet.
```

Natural-language variants also work, for example:

```text
Make this character image into a Codex pet and deploy it to the pet repository.
```

## Example Workflow

See the full step-by-step example here:

- [Example Workflow](./codex-pet-from-image/references/example-workflow.md)

That document shows:

- what kind of reference image to provide
- how the base cutout is prepared
- which 9 animation rows are generated
- how cleanup and validation work
- what the final install directory looks like

## Repository Layout

```text
codex-pet-from-image/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
docs/
  assets/
```

## Important Defaults

- prepared reference cutouts are enlarged to about `1.25x`
- generated rows should keep the character at roughly `72%–84%` of slot height
- decoded row strips are cleaned before final atlas extraction
- finalization uses `--allow-slot-extraction`

## Output

When a run succeeds, the installed result looks like:

```text
~/.codex/pets/<pet-id>/
  pet.json
  spritesheet.webp
```

## Notes On Redistribution

This repository publishes the workflow and supporting scripts.

It does not bundle third-party character pet packs by default. If you plan to publish generated pet assets, make sure you have the right to redistribute the character art.
