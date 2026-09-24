# Elite Robots ROS 2 文档

采用 **Sphinx + MyST Markdown**，按 **文档类型 → 语言 → 章节** 组织。每个文档/语言组合独立生成 HTML 站点及 PDF，具有各自的目录、搜索索引和输出路径。

当前中文快速手册版本为 **1.0.0**，适配版本及面向读者的修订记录分别见正文首页和 `doc/quickstart/zh_CN/changelog.md`。手册版本独立于 ROS 包版本。

目前只编写中文快速手册，已结合当前工作空间的驱动、机器人描述和 Gazebo 仿真源码核对；核对范围及待验证项见 `MAINTENANCE.md`。

## 目录结构

```text
doc/
├── documents.json            # 每份文档及译本的启用状态、标题和版本
├── languages.json            # 共用语言元数据与字体配置
├── conf.py                   # 共用 Sphinx 配置
├── _static/                  # 共用 HTML 样式
└── quickstart/
    ├── images/               # 不含语言文字的共用图片
    └── zh_CN/
        ├── index.md
        ├── overview.md
        ├── robot_setup.md
        ├── installation.md
        ├── driver.md
        ├── moveit.md
        ├── gazebo.md
        ├── support.md
        ├── changelog.md
        └── images/           # 中文界面截图
scripts/build_docs.py
CMakeLists.txt
package.xml
```

后续英文和法文快速手册分别放入 `doc/quickstart/en/`、`doc/quickstart/fr/`；usage 和接口手册分别使用 `doc/usage/<语言>/`、`doc/interfaces/<语言>/`。保持各译本的章节文件名一致，方便对照维护。

`languages.json` 预设 `zh_CN`、`en`、`fr`，但语言配置不代表已有译文。`documents.json` 中目前仅启用 `quickstart/zh_CN`；usage、interfaces 尚未启用。

`README.md`、`MAINTENANCE.md` 和图片目录中的 README 是仓库维护资料，不参与正式 HTML/PDF 的正文构建。

## 安装构建依赖

以下命令以 Ubuntu 22.04 为例，在仓库根目录执行：

```bash
sudo apt-get install -y python3-venv python3-pip
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

PDF 当前使用 XeLaTeX。中文 PDF 依赖：

```bash
sudo apt-get install -y \
  latexmk texlive-xetex texlive-lang-chinese \
  texlive-latex-extra texlive-fonts-recommended \
  fonts-noto-cjk fonts-dejavu-core fonts-lmodern
```

法文 PDF 另需 `texlive-lang-french`，用于 LaTeX 的法语排版与断词支持。其他新增语言也需安装相应的 LaTeX 语言支持包和字体。

PDF 字体由 `languages.json` 配置：西文使用 Latin Modern 和 DejaVu，中文额外使用 Noto CJK；英语、法语配置不加载中文字体。依赖版本约束见 `requirements.txt`。

## 直接构建

```bash
# 所有已启用的文档及译本；目前仅中文快速手册
.venv/bin/python scripts/build_docs.py --format all

# 只构建中文快速手册
.venv/bin/python scripts/build_docs.py \
  --document quickstart --language zh_CN --format all

# 所有已启用文档的中文 HTML
.venv/bin/python scripts/build_docs.py --language zh_CN --format html

# 只生成中文快速手册 PDF
.venv/bin/python scripts/build_docs.py \
  --document quickstart --language zh_CN --format pdf
```

`--document` 和 `--language` 默认都是 `all`。`--format` 支持 `html`、`pdf`、`all` 和仅生成 LaTeX 的 `latex`。通过 `--output /path/to/output` 指定输出根目录。

筛选规则：

- `--document all --language all`：构建所有已启用文档的已启用译本。
- `--document all --language en`：仅构建已有且启用的英文译本，跳过没有英文的文档。
- 指定一个尚未编写/启用的组合，或筛选后没有任何可构建译本，直接报错。
- 已启用的译本缺少 `index.md` 时，构建前报错。不会自动回退到中文或生成空白手册。

输出路径示例：

| 文档/语言 | HTML 入口 | PDF |
| --- | --- | --- |
| 中文快速手册 | `build/docs/quickstart/zh_CN/html/index.html` | `build/docs/quickstart/zh_CN/pdf/quickstart-zh_CN.pdf` |
| 英文快速手册（后续） | `build/docs/quickstart/en/html/index.html` | `build/docs/quickstart/en/pdf/quickstart-en.pdf` |
| 法文使用手册（后续） | `build/docs/usage/fr/html/index.html` | `build/docs/usage/fr/pdf/usage-fr.pdf` |

HTML 是独立多页面站点，PDF 是独立的一本手册。PDF 文件名带语言代码，复制到同一目录时也不会覆盖。构建将 Sphinx 警告视为失败。

可以直接打开 HTML 入口，或启动本地服务器：

```bash
python3 -m http.server 8000 --directory build/docs
```

浏览器访问 `http://localhost:8000/quickstart/zh_CN/html/`。

## 使用 colcon 构建

ROS 包名为 `elite_robots_cs_tutorials`。默认构建所有已启用译本的 HTML；PDF 通过 `BUILD_DOCS_PDF` 启用。

```bash
source /opt/ros/humble/setup.bash
cd ~/elite_ros_ws
colcon build --packages-select elite_robots_cs_tutorials \
  --cmake-args \
  -DPython3_EXECUTABLE="$PWD/src/Elite_Robots_CS_ROS2_Tutorials/.venv/bin/python" \
  -DBUILD_DOCS=ON \
  -DBUILD_DOCS_PDF=ON \
  -DDOCS_DOCUMENT=all \
  -DDOCS_LANGUAGE=all
```

使用 `-DDOCS_DOCUMENT=quickstart -DDOCS_LANGUAGE=zh_CN` 只构建中文快速手册。只要 HTML 时设置 `-DBUILD_DOCS_PDF=OFF`；跳过文档构建设置 `-DBUILD_DOCS=OFF`。CMake 会记住选项，切换时应显式设置。

构建输出：

```text
build/elite_robots_cs_tutorials/docs/quickstart/zh_CN/html/index.html
build/elite_robots_cs_tutorials/docs/quickstart/zh_CN/pdf/quickstart-zh_CN.pdf
```

默认隔离安装的成品位于：

```text
install/elite_robots_cs_tutorials/share/elite_robots_cs_tutorials/manuals/quickstart/zh_CN/
```

`--merge-install` 模式下位于 `install/share/elite_robots_cs_tutorials/manuals/`。

## 新增语言版本

以英文快速手册为例：

1. 创建 `doc/quickstart/en/index.md` 及章节文件，编写英文内容和该版本的 `toctree`。也要翻译正文标题、图片说明和首页文本；配置不会自动翻译正文。
2. 在 `doc/documents.json` 的 `quickstart.languages` 中新增以下成员：

   ```json
   "en": {
     "title": "CS, ES and LS Series ROS 2 Quickstart Guide",
     "version": "1.0.0",
     "enabled": true
   }
   ```

3. 执行：

   ```bash
   .venv/bin/python scripts/build_docs.py \
     --document quickstart --language en --format all
   ```

法语同理使用 `fr`。新增其他语言时，先在 `languages.json` 中添加对应的 Sphinx 语言代码、作者、版权与字体配置。译文尚未准备好时，可将该译本设为 `enabled: false`。

每个译本独立记录版本号，以反映翻译进度；正文首页和修订记录中的文档版本需与清单一致。该方案采用独立 Markdown 译本，不使用 gettext/PO 文件。

## 新增 usage 或接口手册

创建 `doc/usage/<语言>/index.md` 或 `doc/interfaces/<语言>/index.md`，编写相应章节，然后将 `documents.json` 中该文档的 `enabled` 改为 `true`，并在 `languages` 中注册至少一个译本。

不需要复制 `conf.py` 或修改快速手册目录。可以仅启用快速手册的英文，同时保留接口手册只有中文。

## 图片组织

- **语言专用图片**：例如中文界面截图，放在 `doc/quickstart/zh_CN/images/`，正文引用 `images/文件名.png`。当前正文图片使用这种引用方式。
- **共用图片**：例如不含文字的机器人照片，放在 `doc/quickstart/images/`，各译本通过 `../images/文件名.png` 引用。Sphinx 构建时会复制到对应 HTML/PDF 输出所需的位置。

新增或替换配图时使用 MyST `figure`，例如：

````markdown
```{figure} images/fig-6-1-gazebo.png
:name: gazebo-startup
:width: 90%
:alt: Gazebo 场景中的机器人模型

Gazebo 启动结果。
```
````

不同译本可以使用相同的图标签，因为它们分别构建。共用图片的说明和替代文本仍在各语言正文中翻译。PNG/JPEG 适合同时生成 HTML 和 PDF。

## 迁移与维护

原中文源文件已从 `doc/quickstart/` 移至 `doc/quickstart/zh_CN/`。旧输出目录 `build/docs/quickstart/html/`、`pdf/`、`latex/`、`doctrees/` 不再使用；本次迁移将已有的这些目录归档到 `build/pre-i18n/quickstart/`。其他工作空间中过去生成的旧输出可自行清理；构建不会自动删除它们。

源码核对记录和待确认项见 `MAINTENANCE.md`。机器人操作命令仅作为文档整理，未执行硬件验证。

当前提供 ament_cmake 包结构，未执行 bloom-release 或上传网站。包维护者暂沿用现有驱动中的 Yan / yanxiaojia@elibot.cn；包版本 `0.1.0` 与来源手册版本分开管理。原手册保留所有权利，`package.xml` 暂记为 `Proprietary`；正式发布前由项目方确认维护者、许可及目标平台依赖。

接入 ROS 官方文档托管时仍需单独配置 rosdoc2 入口与 rosdistro 的 `doc` 条目，并验证构建。这里的独立语言站点暂未添加网页语言切换器，bloom 也不会自动发布这些 PDF。

## HTML 主题

HTML 使用仓库内的 `elite` 主题，继承 Sphinx `basic`，无需安装第三方主题包或从外部 CDN 加载样式。布局参考 Elite 技术文档站点：白色顶栏、浅灰色章节目录及页内目录、蓝色选中项和主标题竖线。

- `doc/_themes/elite/layout.html`：共用页面布局、搜索入口和前后章节导航。
- `doc/_static/manual.css`：配色、排版及响应式布局；`manual.js`：移动导航、代码复制和页内目录高亮。
- `doc/_static/elite-logo.png`：本地品牌 Logo；`doc/conf.py`：主题及中、英、法界面文字配置。
- 搜索使用 Sphinx 自带索引。使用 `--format all`，或输出目录中已有对应 PDF 时，显示 PDF 下载入口；只构建 HTML 且无 PDF 时不显示。
- 各语言仍独立构建，页头显示当前语言及文档版本。未启用的译本和其他手册不显示跳转入口。
- PDF 继续使用现有 XeLaTeX 排版，不继承 HTML CSS。正式正文不显示资料来源说明；图片提取元数据作为维护记录保留。
