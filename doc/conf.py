"""Shared Sphinx configuration for an independent document/language pair."""
import json
import os
import shutil
from pathlib import Path
from io import BytesIO
from zipfile import ZipFile, ZipInfo, ZIP_DEFLATED

DOC_DIR = Path(__file__).resolve().parent
document_id = os.environ.get("ELITE_DOCUMENT", "quickstart")
language = os.environ.get("ELITE_LANGUAGE", "zh_CN")
documents = json.loads((DOC_DIR / "documents.json").read_text(encoding="utf-8"))
languages = json.loads((DOC_DIR / "languages.json").read_text(encoding="utf-8"))
document = documents[document_id]["languages"][language]
locale = languages[language]

project = document["title"]
author = locale["author"]
copyright = locale["copyright"]
version = release = document["version"]
root_doc = "index"
extensions = ["myst_parser"]
source_suffix = {".md": "markdown", ".rst": "restructuredtext"}
myst_heading_anchors = 3
exclude_patterns = ["_build", "images/README.md"]
html_theme = "sphinx_rtd_theme"
html_title = project
html_show_sourcelink = False
html_copy_source = False
numfig = True
highlight_language = "none"

latex_engine = "xelatex"
output_name = f"{document_id}-{language}"
latex_documents = [("index", f"{output_name}.tex", project, author, "manual")]
latex_show_urls = "footnote"
latex_use_xindy = False
# Avoid Sphinx 8 colorrows recursion with TeX Live 2026 array/colortbl.
# https://github.com/sphinx-doc/sphinx/issues/14465
latex_table_style = ["booktabs"]
fonts = locale["fonts"]
font_commands = [
    r"\usepackage{fontspec}",
    rf"\setmainfont{{{fonts['main']}}}",
    rf"\setsansfont{{{fonts['sans']}}}",
    rf"\setmonofont{{{fonts['mono']}}}[Scale=0.85]",
]
if "cjk_main" in fonts:
    font_commands += [
        r"\usepackage{xeCJK}",
        rf"\setCJKmainfont{{{fonts['cjk_main']}}}[AutoFakeSlant=0.2]",
        rf"\setCJKsansfont{{{fonts['cjk_sans']}}}",
        rf"\setCJKmonofont{{{fonts['cjk_mono']}}}[AutoFakeSlant=0.2]",
    ]
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "extraclassoptions": "openany,oneside",
    "fontpkg": "\n".join(font_commands),
    "preamble": (
        r"\sloppy\setlength{\emergencystretch}{3em}\setlength{\headheight}{15pt}"
        + locale.get("latex_preamble", "")
    ),
    "sphinxsetup": "verbatimwithframe=true,VerbatimColor={rgb}{0.96,0.97,0.98}",
}


def prepare_example_downloads(app):
    """Package the current example sources before Sphinx resolves downloads."""
    document_root = DOC_DIR / document_id
    excluded = {".git", "__pycache__", "build", "install", "log"}
    for name, relative_source in documents[document_id].get("downloads", {}).items():
        source = document_root / relative_source
        if not source.is_dir():
            raise FileNotFoundError(f"Missing download source: {source}")
        buffer = BytesIO()
        with ZipFile(buffer, "w", compression=ZIP_DEFLATED) as archive:
            for path in sorted(source.rglob("*")):
                relative = path.relative_to(source)
                if (not path.is_file() or excluded.intersection(relative.parts)
                        or path.suffix in {".pyc", ".pyo"}):
                    continue
                info = ZipInfo((Path(source.name) / relative).as_posix())
                info.create_system = 3
                info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
                info.compress_type = ZIP_DEFLATED
                archive.writestr(info, path.read_bytes())
        target = document_root / "downloads" / f"{name}.zip"
        target.parent.mkdir(parents=True, exist_ok=True)
        content = buffer.getvalue()
        if not target.exists() or target.read_bytes() != content:
            target.write_bytes(content)


def export_pdf_downloads(app, exception):
    """Export resolved local downloads without HTML hashes or PDF links."""
    if exception is not None or app.builder.name != "latex":
        return
    document_root = (DOC_DIR / document_id).resolve()
    target_root = Path(app.outdir) / "downloads"
    # This directory is generated exclusively by this callback.
    if target_root.exists():
        shutil.rmtree(target_root)
    target_root.mkdir(parents=True)
    for filename in sorted(app.env.dlfiles):
        source = (Path(app.srcdir) / filename).resolve()
        relative = source.relative_to(document_root)
        # Put ZIP archives directly in downloads; retain example package paths.
        if relative.parts[0] == "downloads":
            relative = Path(*relative.parts[1:])
        target = target_root / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)


def setup(app):
    app.connect("builder-inited", prepare_example_downloads)
    app.connect("build-finished", export_pdf_downloads)
