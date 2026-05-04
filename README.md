# codex-pet

This repository contains a reusable Codex skill for turning one reference image into a deployable Codex custom pet.

## Included Skill

- `codex-pet-from-image/`

This skill:

- takes a user-provided character image as the identity reference
- generates a clean base character image
- prepares a `hatch-pet` run
- generates all 9 required animation rows with `imagegen`
- removes chroma-key green from decoded row strips
- validates the final atlas
- deploys the packaged pet into `~/.codex/pets/<pet-id>/`

## Install

Copy the skill folder into your Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R codex-pet-from-image ~/.codex/skills/codex-pet-from-image
```

## Use

In Codex, call:

```text
Use $codex-pet-from-image to turn this reference image into an installed Codex pet.
```

Or say it more naturally:

```text
Make this character image into a Codex pet and deploy it to the pet repository.
```

## Notes

- The skill defaults to enlarging the prepared reference cutout to about `1.25x`.
- The skill includes a decoded-row cleanup step so green chroma-key backgrounds do not leak into the final pet.
- Finalization uses `--allow-slot-extraction` because some valid imagegen outputs are cleaner with slot-based extraction than component extraction.
