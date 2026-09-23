# Elite Robots ROS 2 文档

采用 **Sphinx + MyST Markdown**。快速手册、usage、接口手册是三个独立文档项目，各有自己的 HTML 目录、导航和 PDF，不合并成一本书。

目前只完成快速手册，内容依据用户提供的 **CS&ES&LS_ROS2软件包快速使用手册_Ver2.16.1.pdf**（2026-08-07）重写，尚未迁移到当前驱动接口。

## 目录与输出

```text
doc/
├── documents.json       # 三份文档的名称、版本、启用状态
├── conf.py              # 共用 Sphinx / 中文 PDF 配置
├── _static/             # HTML 样式
└── quickstart/          # 本次编写的快速手册
    ├── index.md
    ├── overview.md
    ├── robot_setup.md
    ├── installation.md
    ├── driver.md
    ├── moveit.md
    ├── gazebo.md
    ├── support.md
    └── images/          # 后续图片放这里
scripts/build_docs.py    # 独立文档构建入口
CMakeLists.txt           # colcon / ament_cmake 集成
package.xml
```

`usage` 和 `interfaces` 仅在 `documents.json` 中预留，尚未创建正文，默认不构建。显式请求尚未启用的文档会报错，不生成空白 PDF。

| 文档 | HTML 入口 | PDF |
| --- | --- | --- |
| quickstart | `build/docs/quickstart/html/index.html` | `build/docs/quickstart/pdf/quickstart.pdf` |
| usage（后续） | `build/docs/usage/html/index.html` | `build/docs/usage/pdf/usage.pdf` |
| interfaces（后续） | `build/docs/interfaces/html/index.html` | `build/docs/interfaces/pdf/interfaces.pdf` |

HTML 为每份文档独立的多页面站点。PDF 为每份文档独立的一本手册。构建时把 Sphinx 警告视为失败。

## 安装构建依赖

以下命令以 Ubuntu 22.04 为例。

```bash
sudo apt-get install -y python3-venv python3-pip
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
```

生成中文 PDF 还需要：

```bash
sudo apt-get install -y \
  latexmk texlive-xetex texlive-lang-chinese \
  texlive-latex-extra texlive-fonts-recommended \
  fonts-noto-cjk fonts-dejavu-core fonts-lmodern
```

PDF 使用 XeLaTeX、Noto CJK 中文字体、Latin Modern 西文字体和 DejaVu 等宽字体。版本约束以 `requirements.txt` 为准，目标系统自带的旧版 Sphinx/MyST 不一定满足要求。

## 直接构建

在仓库根目录执行：

```bash
# 当前仅生成快速手册的 HTML 与 PDF
.venv/bin/python scripts/build_docs.py --format all

# 仅生成 HTML
.venv/bin/python scripts/build_docs.py --format html

# 仅生成快速手册 PDF
.venv/bin/python scripts/build_docs.py --document quickstart --format pdf

# 可选：只生成 LaTeX，供排版调试
.venv/bin/python scripts/build_docs.py --document quickstart --format latex
```

通过 `--output /path/to/output` 可改变输出根目录。`all` 表示所有已经启用的文档；后续启用另外两份文档后，同一命令将分别产生三套 HTML 和三份 PDF。

HTML 可直接打开对应 `index.html`，也可以启动本地服务器：

```bash
python3 -m http.server 8000 --directory build/docs
```

然后访问 `http://localhost:8000/quickstart/html/`。

## 使用 colcon 构建

ROS 包名为 `elite_robots_cs_tutorials`。默认构建 HTML，PDF 通过 `BUILD_DOCS_PDF` 显式启用。下面假设仓库位于 `~/elite_ros_ws/src/Elite_Robots_CS_ROS2_Tutorials`，且已按上文创建 `.venv`：

```bash
source /opt/ros/humble/setup.bash
cd ~/elite_ros_ws
colcon build --packages-select elite_robots_cs_tutorials \
  --cmake-args \
  -DPython3_EXECUTABLE="$PWD/src/Elite_Robots_CS_ROS2_Tutorials/.venv/bin/python" \
  -DBUILD_DOCS=ON \
  -DBUILD_DOCS_PDF=ON
```

构建产物位于：

```text
build/elite_robots_cs_tutorials/docs/quickstart/html/index.html
build/elite_robots_cs_tutorials/docs/quickstart/pdf/quickstart.pdf
```

默认隔离安装后，成品位于：

```text
install/elite_robots_cs_tutorials/share/elite_robots_cs_tutorials/manuals/quickstart/
```

使用 `--merge-install` 时，安装路径从 `install/share/elite_robots_cs_tutorials/` 开始。

只生成 HTML 时传 `-DBUILD_DOCS_PDF=OFF`；完全跳过文档构建时传 `-DBUILD_DOCS=OFF`。可以通过 `-DDOCS_DOCUMENT=quickstart` 只选择一份文档。CMake 会记住选项，切换模式时应显式设置。

## 添加 usage 或接口手册

1. 创建 `doc/usage/index.md` 或 `doc/interfaces/index.md`，并添加该文档自身的章节和 `toctree`。
2. 在 `doc/documents.json` 中将相应 `enabled` 改为 `true`，填写版本。
3. 运行 `scripts/build_docs.py --format all`，或重新执行 colcon 构建。

无需复制 `conf.py`，也无需把新章节加入快速手册的目录。每次 Sphinx 构建只读取被选中文档的源目录，输出、搜索索引和 PDF 均彼此独立。

## 补充图片

所有原图编号都保留在正文的“图片占位”提示框中。图片补齐后，用 MyST `figure` 替换对应提示框：

````markdown
```{figure} images/fig-4-11-gazebo.png
:name: gazebo-startup
:width: 90%
:alt: Gazebo 场景中的机器人模型

Gazebo 启动结果。
```
````

多张图共用一个占位框时，应分别插入图片。PNG/JPEG 便于同时生成 HTML 和 PDF；无需先创建空图片文件。图片说明见 `doc/quickstart/images/README.md`。

## 来源、维护与发布

原手册与新章节的对应关系、基础错误修正及待核对内容见 `MAINTENANCE.md`。原文命令仅作为文档整理，没有在机器人上执行，也没有下载或执行原文的远程安装脚本。

本目录已提供 ament_cmake 包结构，但未执行 bloom-release 或上传网站。包维护者暂沿用当前驱动中的 Yan / yanxiaojia@elibot.cn；包版本 `0.1.0` 与来源手册版本 `Ver2.16.1` 分开管理。原手册保留所有权利，因此未擅自将其改为开源许可，`package.xml` 暂记为 `Proprietary`。正式发布前需由项目方确认维护者、许可及各目标平台依赖。

当前配置面向独立 Sphinx 和 colcon 构建。后续接入 ROS 官方文档托管时，还需设置 rosdoc2 的入口与 rosdistro 的 `doc` 配置，并验证其统一主题下的输出；bloom 不会自动发布这里的三份 PDF。
