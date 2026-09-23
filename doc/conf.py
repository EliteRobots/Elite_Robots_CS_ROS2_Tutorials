"""Shared Sphinx configuration for an independent document/language pair."""
import json
import os
from pathlib import Path

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
html_static_path = [str(DOC_DIR / "_static")]
html_css_files = ["manual.css"]
html_theme_options = {"navigation_depth": 4, "collapse_navigation": False}
numfig = True
highlight_language = "none"

latex_engine = "xelatex"
output_name = f"{document_id}-{language}"
latex_documents = [("index", f"{output_name}.tex", project, author, "manual")]
latex_show_urls = "footnote"
latex_use_xindy = False
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
