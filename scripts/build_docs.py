#!/usr/bin/env python3
"""Build independent HTML/PDF manuals for enabled document/language pairs."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys


def select_builds(documents, languages, document_id, language):
    """Select available translations; never silently fall back to another language."""
    if language != "all" and language not in languages:
        raise ValueError(f"Unknown language: {language}")
    if document_id == "all":
        selected = [key for key, value in documents.items() if value["enabled"]]
    elif document_id not in documents:
        raise ValueError(f"Unknown document: {document_id}")
    elif not documents[document_id]["enabled"]:
        raise ValueError(f"Document '{document_id}' is not written/enabled yet.")
    else:
        selected = [document_id]

    builds = []
    for key in selected:
        translations = documents[key]["languages"]
        for code, translation in translations.items():
            if not translation["enabled"] or language not in ("all", code):
                continue
            if code not in languages:
                raise ValueError(f"Unknown language '{code}' configured for '{key}'.")
            builds.append((key, code))
    if not builds:
        raise ValueError(
            f"No enabled translation for document='{document_id}', language='{language}'."
        )
    return builds


def main():
    root = Path(__file__).resolve().parents[1]
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--document", default="all", help="all or a document ID in doc/documents.json")
    parser.add_argument("--language", default="all", help="all or a code in doc/languages.json")
    parser.add_argument("--format", choices=("html", "pdf", "all", "latex"), default="all")
    parser.add_argument("--output", type=Path, default=root / "build" / "docs")
    args = parser.parse_args()
    documents = json.loads((root / "doc" / "documents.json").read_text(encoding="utf-8"))
    languages = json.loads((root / "doc" / "languages.json").read_text(encoding="utf-8"))
    try:
        builds = select_builds(documents, languages, args.document, args.language)
    except ValueError as error:
        parser.error(str(error))
    for key, code in builds:
        if not (root / "doc" / key / code / "index.md").is_file():
            parser.error(f"Missing doc/{key}/{code}/index.md")
    formats = ["html", "pdf"] if args.format == "all" else [args.format]
    if "pdf" in formats:
        # Windows calls latexmk directly; Sphinx latexpdf needs make on POSIX.
        required_tools = ("latexmk", "xelatex")
        if sys.platform != "win32":
            required_tools += ("make",)
        missing = [name for name in required_tools if not shutil.which(name)]
        if missing:
            parser.error("Missing PDF tools: " + ", ".join(missing) + ". See README.md.")
    for key, code in builds:
        output = args.output.resolve() / key / code
        env = dict(os.environ, ELITE_DOCUMENT=key, ELITE_LANGUAGE=code)
        for fmt in formats:
            builder = "latexpdf" if fmt == "pdf" else fmt
            if fmt == "pdf" and sys.platform == "win32":
                builder = "latex"
            subprocess.run([
                sys.executable, "-m", "sphinx", "-M", builder,
                str(root / "doc" / key / code), str(output),
                "-c", str(root / "doc"), "-W", "--keep-going",
            ], env=env, check=True)
            if fmt == "pdf":
                if sys.platform == "win32":
                    # Generated make.bat can hide latexmk failures. Check it directly.
                    subprocess.run([
                        "latexmk", "-pdf", "-dvi-", "-ps-",
                        "-interaction=nonstopmode", "-halt-on-error",
                        f"{key}-{code}.tex",
                    ], cwd=output / "latex", env=env, check=True)
                pdf = output / "latex" / f"{key}-{code}.pdf"
                if not pdf.is_file():
                    raise RuntimeError(f"PDF was not generated: {pdf}")
                (output / "pdf").mkdir(parents=True, exist_ok=True)
                shutil.copy2(pdf, output / "pdf" / pdf.name)
                downloads = output / "pdf" / "downloads"
                if downloads.exists():
                    shutil.rmtree(downloads)
                shutil.copytree(output / "latex" / "downloads", downloads)
            print(f"Built {key}/{code}: {fmt} -> {output}", flush=True)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (subprocess.CalledProcessError, RuntimeError) as error:
        print(f"Documentation build failed: {error}", file=sys.stderr)
        sys.exit(1)
