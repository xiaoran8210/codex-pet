#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


ROW_IDS = {
    "idle",
    "running-right",
    "running-left",
    "waving",
    "jumping",
    "failed",
    "waiting",
    "running",
    "review",
}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    args = parser.parse_args()

    run_dir = Path(args.run_dir).expanduser().resolve()
    request = json.loads((run_dir / "pet_request.json").read_text(encoding="utf-8"))
    chroma_key = str(request.get("chroma_key") or "#00FF00")
    remover = (
        Path.home()
        / ".codex"
        / "skills"
        / ".system"
        / "imagegen"
        / "scripts"
        / "remove_chroma_key.py"
    )

    decoded_dir = run_dir / "decoded"
    for image_path in sorted(decoded_dir.glob("*.png")):
        if image_path.stem not in ROW_IDS:
            continue
        subprocess.run(
            [
                sys.executable,
                str(remover),
                "--input",
                str(image_path),
                "--out",
                str(image_path),
                "--key-color",
                chroma_key,
                "--soft-matte",
                "--transparent-threshold",
                "12",
                "--opaque-threshold",
                "220",
                "--despill",
            ],
            check=True,
        )
        print(image_path)


if __name__ == "__main__":
    main()
