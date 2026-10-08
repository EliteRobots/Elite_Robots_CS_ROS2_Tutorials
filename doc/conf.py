"""Shared Sphinx configuration for an independent document/language pair."""
import json
import os
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
html_theme = "elite"
html_theme_path = [str(DOC_DIR / "_themes")]
html_title = project
html_static_path = [str(DOC_DIR / "_static")]
html_js_files = ["manual.js"]
html_show_sourcelink = False
html_copy_source = False
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


# Shared navigation labels; unavailable translations are not shown as links.
ELITE_UI = {'zh_CN': {'site_title': 'ROS 2 技术文档',
           'links': '相关网站',
           'website': '官网',
           'portal': '技术文档',
           'search': '搜索文档',
           'menu': '展开或收起目录',
           'chapters': '文档目录',
           'home': '首页',
           'breadcrumbs': '当前位置',
           'download': '下载 PDF',
           'version': '版本',
           'on_page': '页内目录',
           'pagination': '章节导航',
           'previous': '上一章',
           'next': '下一章',
           'top': '返回顶部',
           'skip': '跳到正文',
           'copy': '复制',
           'copied': '已复制',
           'copy_failed': '请手动复制'},
 'en': {'site_title': 'ROS 2 Documentation',
        'links': 'Related websites',
        'website': 'Website',
        'portal': 'Documentation',
        'search': 'Search documentation',
        'menu': 'Toggle navigation',
        'chapters': 'Chapters',
        'home': 'Home',
        'breadcrumbs': 'Breadcrumbs',
        'download': 'Download PDF',
        'version': 'Version',
        'on_page': 'On this page',
        'pagination': 'Page navigation',
        'previous': 'Previous',
        'next': 'Next',
        'top': 'Back to top',
        'skip': 'Skip to content',
        'copy': 'Copy',
        'copied': 'Copied',
        'copy_failed': 'Copy manually'},
 'fr': {'site_title': 'Documentation ROS 2',
        'links': 'Sites associés',
        'website': 'Site officiel',
        'portal': 'Documentation',
        'search': 'Rechercher',
        'menu': 'Afficher le menu',
        'chapters': 'Chapitres',
        'home': 'Accueil',
        'breadcrumbs': 'Fil d’Ariane',
        'download': 'Télécharger le PDF',
        'version': 'Version',
        'on_page': 'Sur cette page',
        'pagination': 'Navigation des pages',
        'previous': 'Précédent',
        'next': 'Suivant',
        'top': 'Retour en haut',
        'skip': 'Aller au contenu',
        'copy': 'Copier',
        'copied': 'Copié',
        'copy_failed': 'Copier manuellement'}}
ELITE_DOCUMENT_LABELS = {'zh_CN': {'quickstart': '快速使用手册', 'usage': '使用手册', 'interfaces': '接口手册'},
 'en': {'quickstart': 'Quickstart guide',
        'usage': 'User guide',
        'interfaces': 'Interface reference'},
 'fr': {'quickstart': 'Guide de démarrage',
        'usage': 'Guide d’utilisation',
        'interfaces': 'Référence des interfaces'}}
html_context = {
    "elite_ui": ELITE_UI.get(language, ELITE_UI["en"]),
    "elite_document_label": ELITE_DOCUMENT_LABELS.get(language, ELITE_DOCUMENT_LABELS["en"]).get(document_id, project),
    "elite_language_label": locale["label"],
    "elite_output_name": output_name,
    "elite_pdf_available": os.environ.get("ELITE_PDF_AVAILABLE") == "1",
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


def setup(app):
    app.connect("builder-inited", prepare_example_downloads)
