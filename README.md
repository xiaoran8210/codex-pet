# codex-pet

Turn a single reference image into a usable Codex custom pet, then install it directly into `~/.codex/pets/<pet-id>/`.

This repository packages a reusable Codex skill that handles the full workflow from character image to validated pet atlas.

## What This Skill Does

`codex-pet-from-image/` will:

- use one user-provided image as the identity reference
- generate a clean base character image in the same visual style
- remove the background and tighten the cutout
- enlarge the prepared reference so the character does not end up too small
- prepare a standard `hatch-pet` run
- generate all 9 required animation rows with `imagegen`
- clean chroma-key green from decoded row strips before final packaging
- validate the atlas and package it as a Codex pet
- deploy the finished pet into `~/.codex/pets/<pet-id>/`

## Why This Repo Exists

The built-in pet pipeline is powerful, but the image-to-pet path needs a few practical fixes to feel production-ready:

- reference characters often come out too small
- green chroma backgrounds can leak into intermediate rows
- some good generations need slot-based extraction instead of component-only extraction

This skill bakes those fixes into one repeatable workflow.

## Install

Copy the skill into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-from-image ~/.codex/skills/codex-pet-from-image
```

After that, you can call it from any Codex conversation.

## Quick Start

With a reference image attached, say:

```text
Use $codex-pet-from-image to turn this reference image into an installed Codex pet.
```

Or:

```text
Make this character image into a Codex pet and deploy it to the pet repository.
```

## Example Workflow

A complete end-to-end example is documented here:

- [Example Workflow](./codex-pet-from-image/references/example-workflow.md)

It shows what to provide, what the skill generates, what gets validated, and what appears in the final install directory.

## Repo Layout

```text
codex-pet-from-image/
  SKILL.md
  agents/openai.yaml
  references/
  scripts/
```

## Important Defaults

- prepared reference cutouts are enlarged to about `1.25x`
- generated rows should keep the character at roughly `72%–84%` of slot height
- decoded row strips are cleaned before final atlas extraction
- finalization uses `--allow-slot-extraction`

## About Prebuilt Character Pets

Technically, this repo could also include ready-to-install pet packages.
For a public GitHub repository, I recommend not bundling third-party character pets unless you have clear redistribution rights for those assets.

Because of that, this repo currently ships the workflow, not copyrighted character packs.
