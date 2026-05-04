#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def newest_imagegen_file(root: Path) -> Path:
    files = sorted(root.rglob("ig_*"), key=lambda path: path.stat().st_mtime, reverse=True)
    if not files:
        raise SystemExit(f"no built-in imagegen files found under {root}")
    return files[0]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--run-dir", required=True)
    parser.add_argument("--job-id", required=True)
    parser.add_argument(
        "--generated-root",
        default=str(Path.home() / ".codex" / "generated_images"),
    )
    args = parser.parse_args()

    source = newest_imagegen_file(Path(args.generated_root).expanduser().resolve())
    recorder = (
        Path.home()
        / ".codex"
        / "vendor_imports"
        / "skills"
        / "skills"
        / ".curated"
        / "hatch-pet"
        / "scripts"
        / "record_imagegen_result.py"
    )

    subprocess.run(
        [
            sys.executable,
            str(recorder),
            "--run-dir",
            str(Path(args.run_dir).expanduser().resolve()),
            "--job-id",
            args.job_id,
            "--source",
            str(source),
        ],
        check=True,
    )

    print(source)


if __name__ == "__main__":
    main()
