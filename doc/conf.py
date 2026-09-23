"""Shared configuration; each document is built as its own Sphinx project."""
import json
import os
from pathlib import Path

DOC_DIR = Path(__file__).resolve().parent
document_id = os.environ.get("ELITE_DOCUMENT", "quickstart")
document = json.loads((DOC_DIR / "documents.json").read_text(encoding="utf-8"))[document_id]

project = document["title"]
author = "艾利特智能机器人股份有限公司"
copyright = "2026, ELITE ROBOTS. 保留所有权利"
version = release = document["version"]
language = "zh_CN"
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
latex_documents = [("index", f"{document_id}.tex", project, author, "manual")]
latex_show_urls = "footnote"
latex_use_xindy = False
latex_elements = {
    "papersize": "a4paper",
    "pointsize": "11pt",
    "extraclassoptions": "openany,oneside",
    "fontpkg": r"""
\usepackage{fontspec}
\usepackage{xeCJK}
\setmainfont{Latin Modern Roman}
\setsansfont{Latin Modern Sans}
\setmonofont{DejaVu Sans Mono}[Scale=0.85]
\setCJKmainfont{Noto Serif CJK SC}[AutoFakeSlant=0.2]
\setCJKsansfont{Noto Sans CJK SC}
\setCJKmonofont{Noto Sans Mono CJK SC}[AutoFakeSlant=0.2]
""",
    "preamble": r"\sloppy\setlength{\emergencystretch}{3em}\setlength{\headheight}{15pt}\addto\captionsenglish{\renewcommand{\chaptername}{章节}}",
    "sphinxsetup": "verbatimwithframe=true,VerbatimColor={rgb}{0.96,0.97,0.98}",
}
