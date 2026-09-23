#!/usr/bin/env python3
"""Build independent HTML/PDF manuals from the document registry."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document", default="all", help="all, quickstart, usage, interfaces")
    parser.add_argument("--format", choices=("html", "pdf", "all", "latex"), default="all")
    parser.add_argument("--output", type=Path, default=root / "build" / "docs")
    args = parser.parse_args()
    documents = json.loads((root / "doc" / "documents.json").read_text(encoding="utf-8"))
    if args.document == "all":
        selected = [key for key, value in documents.items() if value["enabled"]]
    elif args.document not in documents:
        parser.error(f"Unknown document: {args.document}")
    elif not documents[args.document]["enabled"]:
        parser.error(f"Document '{args.document}' is not written/enabled yet.")
    else:
        selected = [args.document]
    if not selected:
        parser.error("No documents enabled.")
    for key in selected:
        if not (root / "doc" / key / "index.md").is_file():
            parser.error(f"Missing doc/{key}/index.md")
    formats = ["html", "pdf"] if args.format == "all" else [args.format]
    if "pdf" in formats:
        missing = [name for name in ("make", "latexmk", "xelatex") if not shutil.which(name)]
        if missing:
            parser.error("Missing PDF tools: " + ", ".join(missing) + ". See README.md.")
    for key in selected:
        output = args.output.resolve() / key
        env = dict(os.environ, ELITE_DOCUMENT=key)
        for fmt in formats:
            builder = "latexpdf" if fmt == "pdf" else fmt
            subprocess.run([
                sys.executable, "-m", "sphinx", "-M", builder,
                str(root / "doc" / key), str(output),
                "-c", str(root / "doc"), "-W", "--keep-going",
            ], env=env, check=True)
            if fmt == "pdf":
                pdf = output / "latex" / f"{key}.pdf"
                if not pdf.is_file():
                    raise RuntimeError(f"PDF was not generated: {pdf}")
                (output / "pdf").mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf, output / "pdf" / pdf.name)
            print(f"Built {key}: {fmt} -> {output}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Documentation build failed: {error}", file=sys.stderr)
        sys.exit(1)
