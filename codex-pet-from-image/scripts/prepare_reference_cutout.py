#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def alpha_bbox(image: Image.Image):
    alpha = image.getchannel("A")
    return alpha.getbbox()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True)
    parser.add_argument("--output", required=True)
    parser.add_argument("--scale", type=float, default=1.25)
    parser.add_argument("--padding-ratio", type=float, default=0.12)
    args = parser.parse_args()

    src = Path(args.input).expanduser().resolve()
    dst = Path(args.output).expanduser().resolve()

    image = Image.open(src).convert("RGBA")
    bbox = alpha_bbox(image)
    if bbox is None:
        raise SystemExit("input image does not contain visible alpha content")

    cropped = image.crop(bbox)
    scaled = cropped.resize(
        (
            max(1, round(cropped.width * args.scale)),
            max(1, round(cropped.height * args.scale)),
        ),
        Image.Resampling.LANCZOS,
    )

    pad = max(12, round(max(scaled.width, scaled.height) * args.padding_ratio))
    canvas = Image.new(
        "RGBA",
        (scaled.width + pad * 2, scaled.height + pad * 2),
        (0, 0, 0, 0),
    )
    canvas.alpha_composite(scaled, (pad, pad))

    dst.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dst)
    print(dst)


if __name__ == "__main__":
    main()
