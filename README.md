# Elite Robots ROS 2 文档

采用 **Sphinx + MyST Markdown**，按 **文档类型 → 语言 → 章节** 组织。每个文档/语言组合独立生成 HTML 站点及 PDF，具有各自的目录、搜索索引和输出路径。

当前中、英文快速手册版本均为 **1.0.0**，适配版本及面向读者的修订记录分别见正文首页和各译本的 `changelog.md`。手册版本独立于 ROS 包版本。

目前已编写中、英文快速手册、接口手册、多机械臂手册及 Tutorials（均为 1.0.0）。接口手册按本次指定源码目录独立核对，版本基线与快速手册不同；核对范围及待验证项见 `MAINTENANCE.md`。

## 目录结构

```text
doc/
├── documents.json            # 每份文档及译本的启用状态、标题和版本
├── languages.json            # 共用语言元数据与字体配置
├── conf.py                   # 共用 Sphinx 配置
├── tutorials/
│   ├── examples/moveit/     # 共用的工作单元和 C++ 示例包
│   ├── en/moveit/           # 英文 MoveIt 教程及配图
│   └── zh_CN/moveit/        # 中文 MoveIt 教程及配图
├── multi_arm/
│   ├── examples/            # 共用完整 launch 模板
│   ├── en/                  # 英文多机械臂手册
│   └── zh_CN/               # 中文多机械臂手册
├── interfaces/
│   ├── en/                  # 英文接口手册及独立目录
│   └── zh_CN/               # 中文接口手册及独立目录
└── quickstart/
    ├── en/                   # 英文正文和独立图片目录
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

英文快速手册位于 `doc/quickstart/en/`，后续法文版放入 `doc/quickstart/fr/`；usage 和接口手册分别使用 `doc/usage/<语言>/`、`doc/interfaces/<语言>/`。保持各译本的章节文件名一致，方便对照维护。

`languages.json` 预设 `zh_CN`、`en`、`fr`，但语言配置不代表已有译文。`documents.json` 中目前启用 `quickstart/zh_CN`、`quickstart/en`、`interfaces/zh_CN`、`interfaces/en`、`multi_arm/zh_CN`、`multi_arm/en`、`tutorials/zh_CN` 和 `tutorials/en`；usage 尚未启用。

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
  make latexmk texlive-xetex texlive-lang-chinese \
  texlive-latex-extra texlive-fonts-recommended \
  fonts-noto-cjk fonts-dejavu-core fonts-lmodern
```

法文 PDF 另需 `texlive-lang-french`，用于 LaTeX 的法语排版与断词支持。其他新增语言也需安装相应的 LaTeX 语言支持包和字体。

PDF 字体由 `languages.json` 配置：西文使用 Latin Modern 和 DejaVu，中文额外使用 Noto CJK；英语、法语配置不加载中文字体。依赖版本约束见 `requirements.txt`。

### Windows 构建

安装本机 Python 依赖（`python -m pip install -r requirements.txt`），并确保 TeX Live 的 `latexmk` 和 `xelatex` 在当前终端的 PATH 中。可在 PowerShell 中检查：

```powershell
where.exe python
where.exe latexmk
where.exe xelatex
python scripts/build_docs.py --format all
```

Windows 下先由 Sphinx 生成 LaTeX，再直接调用 `latexmk` 并检查退出码，无需额外安装 GNU `make`；Linux/WSL 下仍需 `make`。Windows 与 WSL 使用各自的 Python、TeX 工具和字体，请在实际运行构建命令的环境中检查依赖。修改 PATH 后需重新打开终端。中文及西文字体要求与上文相同。PDF 表格使用 `booktabs` 样式，避免 Sphinx 8 与 TeX Live 2026 的 `colorrows` 兼容问题。

## 直接构建

```bash
# 所有已启用的文档及译本；目前为中、英文 quickstart、interfaces、multi_arm 和 tutorials
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
| 英文快速手册 | `build/docs/quickstart/en/html/index.html` | `build/docs/quickstart/en/pdf/quickstart-en.pdf` |
| 中文接口手册 | `build/docs/interfaces/zh_CN/html/index.html` | `build/docs/interfaces/zh_CN/pdf/interfaces-zh_CN.pdf` |
| 英文接口手册 | `build/docs/interfaces/en/html/index.html` | `build/docs/interfaces/en/pdf/interfaces-en.pdf` |
| 中文多机械臂手册 | `build/docs/multi_arm/zh_CN/html/index.html` | `build/docs/multi_arm/zh_CN/pdf/multi_arm-zh_CN.pdf` |
| 英文多机械臂手册 | `build/docs/multi_arm/en/html/index.html` | `build/docs/multi_arm/en/pdf/multi_arm-en.pdf` |
| 中文教程 | `build/docs/tutorials/zh_CN/html/index.html` | `build/docs/tutorials/zh_CN/pdf/tutorials-zh_CN.pdf` |
| 英文教程 | `build/docs/tutorials/en/html/index.html` | `build/docs/tutorials/en/pdf/tutorials-en.pdf` |
| 法文使用手册（后续） | `build/docs/usage/fr/html/index.html` | `build/docs/usage/fr/pdf/usage-fr.pdf` |

HTML 是独立多页面站点，PDF 是独立的一本手册。PDF 文件名带语言代码，复制到同一目录时也不会覆盖。构建将 Sphinx 警告视为失败。

### PDF 与下载资源交付

每次成功构建 PDF，都会将该手册中实际引用的本地下载文件整理到同级的 `pdf/downloads/`，无需先构建 HTML。ZIP 使用原文件名，单文件保留 `examples/` 下的包名及目录，避免同名文件覆盖；不使用 HTML `_downloads` 中的哈希目录，也不增加 PDF 内的下载链接。

```text
<输出根目录>/tutorials/zh_CN/pdf/
├── tutorials-zh_CN.pdf
└── downloads/
    ├── hello_moveit.zip
    ├── my_elite_robot_cell.zip
    └── examples/moveit/…       # 按示例包和源目录组织的单文件
<输出根目录>/multi_arm/zh_CN/pdf/
├── multi_arm-zh_CN.pdf
└── downloads/examples/
    ├── dual_arm_control.launch.py
    └── dual_moveit.launch.py
```

交接给 Baklib 上传人员时，直接提供各手册的 `pdf/` 目录即可；PDF 和下载资源都在其中。无下载引用的手册生成空的 `downloads/`。该目录由构建自动刷新，不要放入手工文件，已删除的引用不会留下旧资源。HTML 的下载链接继续使用原 `_downloads`。

默认输出根目录为 `build/docs`，执行 `python scripts/build_docs.py --format all` 即可生成。`--format latex` 仅在 `latex/downloads/` 准备资源，不产生 PDF 交付目录。

可以直接打开 HTML 入口，或启动本地服务器：

```bash
python3 -m http.server 8000 --directory build/docs
```

浏览器访问 `http://localhost:8000/quickstart/zh_CN/html/`。

## 使用 colcon 构建

ROS 包名为 `elite_robots_cs_tutorials`。默认构建所有已启用译本的 HTML；PDF 通过 `BUILD_DOCS_PDF` 启用。

先按上面的“安装构建依赖”准备文档环境。CMake 默认优先使用本仓库的 `.venv/bin/python`，没有该环境时使用找到的 `Python3_EXECUTABLE`。文档解释器独立于 ament 使用的 Python，不需要激活 `.venv`，也不需要覆盖整个包的 `Python3_EXECUTABLE`。

准备好依赖后，在工作空间直接执行 `colcon build` 即可构建 HTML。需要显式选择其他文档环境时，传入 `-DDOCS_PYTHON_EXECUTABLE=/path/to/python`；设为空字符串可恢复自动选择。若所选解释器缺少 Sphinx、MyST 或 Read the Docs 主题，会在 CMake 配置阶段报告该解释器路径及处理方法，不会自动安装依赖。


```bash
source /opt/ros/humble/setup.bash
cd ~/elite_ros_ws
colcon build --packages-select elite_robots_cs_tutorials \
  --cmake-args \
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

## 包版本与手册版本

本仓库采用两层版本管理，不要求所有手册与 ROS 包同步升版：

| 记录位置 | 含义 | 更新时机 |
| --- | --- | --- |
| `package.xml` + 根目录 `CHANGELOG.rst` | 整个 `elite_robots_cs_tutorials` 包的发布版本 | 发布新的文档包时更新，包括正文、示例、构建或依赖的变化 |
| `doc/documents.json` + 各译本首页及修订记录 | 某份手册/译本的内容版本 | 该手册内容发生需要记录的修订时更新；未修改的手册不跟随升版 |
| `MAINTENANCE.md` | 来源、核对范围和构建验证记录 | 维护工作发生时补充，不替代发布说明 |

例如下一次只修订 quickstart，可将包版本与 quickstart 升至 `1.0.1`，其余手册仍为 `1.0.0`；如果只修复 PDF 构建脚本，则只增加包版本，各手册内容版本保持不变。这些数字仅为示例，不代表当前版本已变更。

同一手册的中英文在内容同步时使用相同版本；译文尚未同步时保留其实际内容版本。ROS 包版本、手册版本和手册中列出的驱动/SDK 适配版本是不同概念，不应互相替代。

根目录 `CHANGELOG.rst` 按 [ROS REP-132](https://github.com/ros-infrastructure/rep/blob/master/rep-0132.rst) 组织，版本标题对应 `package.xml`，概述本次包发布包含的手册、示例及构建变化；正文细节仍放在各手册的修订记录中。当前补录 `1.0.0` 基线，不据此宣称已完成 bloom 发布。后续未发布改动先记录在 `Forthcoming` 节，发布时整理为与包版本一致的 `版本号 (YYYY-MM-DD)` 节，并记录发生变化的手册版本。不要覆盖已发布版本的历史记录。

`CHANGELOG.rst` 随包安装到 `share/elite_robots_cs_tutorials/`，不加入各手册正文。

## 新增语言版本

英文版已启用。新增其他语言时，以法文快速手册为例：

1. 创建 `doc/quickstart/fr/index.md` 及章节文件，编写法文内容和该版本的 `toctree`。也要翻译正文标题、图片说明和首页文本；配置不会自动翻译正文。
2. 在 `doc/documents.json` 的 `quickstart.languages` 中新增以下成员：

   ```json
   "fr": {
     "title": "Guide de démarrage ROS 2 pour les séries CS, ES et LS",
     "version": "1.0.0",
     "enabled": true
   }
   ```

3. 执行：

   ```bash
   .venv/bin/python scripts/build_docs.py \
     --document quickstart --language fr --format all
   ```

新增其他语言时，先在 `languages.json` 中添加对应的 Sphinx 语言代码、作者、版权与字体配置。译文尚未准备好时，可将该译本设为 `enabled: false`。

每个译本独立记录版本号，以反映翻译进度；正文首页和修订记录中的文档版本需与清单一致。该方案采用独立 Markdown 译本，不使用 gettext/PO 文件。

## 新增 usage 或接口手册

创建 `doc/usage/<语言>/index.md` 或 `doc/interfaces/<语言>/index.md`，编写相应章节，然后将 `documents.json` 中该文档的 `enabled` 改为 `true`，并在 `languages` 中注册至少一个译本。

不需要复制 `conf.py` 或修改快速手册目录。各手册可独立启用语言；目前 quickstart 和 interfaces 均已启用中文和英文。

## 图片组织

- **语言专用图片**：例如中文界面截图，放在 `doc/quickstart/zh_CN/images/`，正文引用 `images/文件名.png`。当前正文图片使用这种引用方式。
- **共用图片（按需创建）**：当前没有共用图片，因此未保留共用目录。后续需要时创建 `doc/quickstart/images/`，各译本通过 `../images/文件名.png` 引用。Sphinx 构建时会复制到对应 HTML/PDF 输出所需的位置。

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

当前提供 ament_cmake 包结构，未执行 bloom-release 或上传网站。包维护者暂沿用现有驱动中的 Yan / yanxiaojia@elibot.cn；包版本 `1.0.0` 与来源手册版本分开管理。原手册保留所有权利，`package.xml` 暂记为 `Proprietary`；正式发布前由项目方确认维护者、许可及目标平台依赖。

接入 ROS 官方文档托管时仍需单独配置 rosdoc2 入口与 rosdistro 的 `doc` 条目，并验证构建。这里的独立语言站点暂未添加网页语言切换器，bloom 也不会自动发布这些 PDF。

## HTML 主题

HTML 使用 `sphinx-rtd-theme` 的 Read the Docs 基础主题，沿用主题默认布局与样式，主题资源由依赖包提供。依赖在 `requirements.txt` 中声明；CMake 也会检查主题是否已安装。搜索使用 Sphinx 自带索引，各文档和语言继续独立构建。PDF 继续使用 XeLaTeX 排版。

## 英文快速手册

英文版位于 `doc/quickstart/en/`，与中文版本同为 `1.0.0`。正文、图注、替代文本和示例注释已翻译，命令及接口标识保留。24 幅现有截图复制到英文版独立的 `images/` 目录，图片中的界面文字暂保持原样，后续可逐一替换为英文截图。

```bash
.venv/bin/python scripts/build_docs.py --document quickstart --language en --format all
```

未指定语言的默认构建现在会同时生成中文和英文版本。只需中文时传入 `--language zh_CN`，或在 colcon 中设置 `-DDOCS_LANGUAGE=zh_CN`。

## 中文接口手册（1.0.0）

正文位于 `doc/interfaces/zh_CN/`，覆盖 Description、Driver、GZ Simulation 九个 ROS 包的接口。其版本基线是本次指定的 `/home/cc/elite_ros_ws/src`：Description 1.0.0、Driver 1.0.3、Gazebo 1.0.1；不要与快速手册的适配版本混用。

```bash
.venv/bin/python scripts/build_docs.py --document interfaces --language zh_CN --format all
```

入口为 `build/docs/interfaces/zh_CN/html/index.html`，PDF 为 `build/docs/interfaces/zh_CN/pdf/interfaces-zh_CN.pdf`。消息定义和 launch 参数索引已与指定源码核对，硬件及仿真流程尚未运行验证。英文接口手册现已翻译并启用，详见下一节。

## 英文接口手册（1.0.0）

正文位于 `doc/interfaces/en/`，12 个 Markdown 文件与中文接口手册保持相同的章节文件名和目录顺序。译本沿用中文 1.0.0 的 Humble 源码基线、接口限制及验证范围，英文修订日期为 2026-09-28；Jazzy 对应源码尚未核对。命令、字段、常量与参数值保持一致。

```bash
.venv/bin/python scripts/build_docs.py --document interfaces --language en --format all
```

英文入口为 `build/docs/interfaces/en/html/index.html`，PDF 为 `build/docs/interfaces/en/pdf/interfaces-en.pdf`。未指定语言时，接口手册会同时构建中文和英文；使用 `--document interfaces --language en` 仅构建英文接口手册。

## 多机械臂手册（multi_arm，中英文 1.0.0）

正文位于 `doc/multi_arm/zh_CN/` 与 `doc/multi_arm/en/`，最初分别从指定 Driver 仓库 `elite_robots_driver/doc/MultiArm_CN.md` 与 `MultiArm.md` 原文迁入，现以用户修订后的中文正文为同步基准。中英文均包含创建文件、双臂驱动、编译并启动、检查和控制、双臂 MoveIt 五节，已移除单臂启动章节；来源路径与修订记录见 `MAINTENANCE.md`。

```bash
# 中英文 HTML/PDF
.venv/bin/python scripts/build_docs.py --document multi_arm --format all
# 仅英文
.venv/bin/python scripts/build_docs.py --document multi_arm --language en --format all
```

colcon 可设置 `-DDOCS_DOCUMENT=multi_arm -DDOCS_LANGUAGE=all`。两个完整模板放在 `doc/multi_arm/examples/`，正文以 literalinclude 展示，并提供下载链接；修改模板后应重建两种语言。HTML 展示完整代码块；PDF 将同一模板按连续行分段排版，下载文件始终为完整脚本。

共用 launch 模板保留迁入时的原始代码。文档构建不启动实体机器人、fake hardware 或 MoveIt。

## Tutorials（中英文 1.0.0）

正文位于 `doc/tutorials/<语言>/`，各译本通过首页 toctree 组织主题目录。MoveIt 教程位于 `moveit/`，覆盖工作空间准备、自定义工作单元、驱动接入、Setup Assistant、控制器映射、标定和 C++ 规划。它解释配置关系和开发步骤；quickstart 继续承担最短启动流程。

```bash
.venv/bin/python scripts/build_docs.py --document tutorials --format all
```

colcon 使用 `-DDOCS_DOCUMENT=tutorials`。不需要修改通用构建脚本、主题或 CMake 文档类型枚举。新增包的教程时，在每个已有译本下增加主题子目录及 `index.md`，再接入该译本首页 toctree；对应示例放在 `doc/tutorials/examples/<主题>/`。这项组织约定仅用于仓库维护，不写入面向读者的正文。

四个共用示例包位于 `doc/tutorials/examples/moveit/`。它们是文档资源，默认文档构建不启动 ROS 节点；按教程复制到独立工作空间后构建。正文通过 literalinclude 引用源文件并提供单文件下载，HTML 显示完整代码，PDF 按连续行分段。模型参数以示例描述包为唯一维护来源，控制包安装相同数据到驱动要求的路径。

来源仓库、提交、章节对应、截图保留情况和离线验证结果见 `MAINTENANCE.md`。


### 示例整包下载

中英文 MoveIt 教程的开头、工作空间准备页和末尾均提供 `hello_moveit.zip`、`my_elite_robot_cell.zip` 下载。下载内容来自当前仓库 `doc/tutorials/examples/moveit/`，包含模型、配置、源码和隐藏的 `.setup_assistant` 文件。

`doc/documents.json` 中的 `tutorials.downloads` 将压缩包名映射到示例目录；`doc/conf.py` 在 Sphinx 读取正文前重新打包。修改示例后正常构建文档即可更新下载，无需维护第二份源码。ZIP 固定条目时间并排序，源码与权限未变时字节保持一致；排除 Git、Python 缓存及 build/install/log 目录。生成文件位于 `doc/tutorials/downloads/`，已加入 `.gitignore`，由 Sphinx 复制到 HTML 的 `_downloads`，随成品站点提供下载。

PDF 提示读者从 HTML 同名章节下载，不依赖 GitHub 或另一个托管地址。
