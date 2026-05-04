# Project Summary

This skill was derived from a working Frieren Codex pet project.

What worked:

- Treat the user-provided image as the primary identity lock.
- First generate a clean base character image in the same style as the reference.
- Remove the chroma-key background locally to create a reusable cutout.
- After cutout, crop transparent edges and scale the reference up by about `1.2x–1.3x`.
- Use `hatch-pet` to create the run structure and row prompts.
- Generate every animation row with `imagegen` instead of replacing rows with local drawing code.
- Clean decoded row strips before finalization so frame extraction does not preserve green backgrounds.
- Validate the final atlas before deployment.

Important quality rules:

- Do not let row generation drift away from the reference face, hair, prop, or outfit.
- Do not accept a pet that reads too small inside the frame; regenerate rows if needed.
- Do not accept detached sparkles, text, sticker borders, or copied layout-guide pixels.
- Do not accept visible chroma-key green behind the character in the final contact sheet.
- Do not rely on a mirrored `running-left` row by default when fidelity matters.
- The final output must be a valid `1536x1872` atlas with transparent unused cells.
