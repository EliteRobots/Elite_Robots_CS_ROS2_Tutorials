---
name: elite-ros2-docs
description: 维护 Elite_Robots_CS_ROS2_Tutorials 的多语言 MyST 手册、Tutorials 与示例下载；用于编写、翻译或校对快速手册、接口、多机械臂及进阶教程，核对 ROS 2 源码并构建 Sphinx HTML/PDF。不用于实现机器人驱动功能。
---

# Elite ROS 2 文档维护

## 定位仓库与任务

在当前工作空间中定位 `Elite_Robots_CS_ROS2_Tutorials`，以 `package.xml` 中的 `elite_robots_cs_tutorials` 确认仓库；不要依赖固定的 `/home/cc` 路径。以下命令和路径均相对该仓库根目录。

先查看工作树修改及任务涉及的源文件，保留用户已经修改的正文和图片。按需阅读 `README.md` 的构建说明及 `MAINTENANCE.md` 的来源、核对范围和待确认事项。后者属于维护资料，不是产品操作手册，也不应将其中的历史问题当作永久限制。

用户明确要求按原 PDF 重写时遵循原文；要求按当前项目校对时，以指定分支/版本的实际源码为准。区分文档来源、代码核对和运行验证，不能把源码审查描述为实机测试。

用户指定源码目录时优先使用该目录，不自动替换为相邻 checkout。同名仓库可能存在多份且版本不同；在维护记录中记录实际路径、分支、提交及包版本。各手册可采用不同源码基线，不将旧手册中的限制或已修复结论直接套用到新版本。Humble/Jazzy 是源码适用范围，不自动要求文档仓库按发行版分支。

## 文档与语言结构

- 正文位于 `doc/<document>/<language>/`，每个组合以 `index.md` 的 `toctree` 组织章节，独立生成 HTML 站点和 PDF。
- `doc/documents.json` 管理 `quickstart`、`usage`、`interfaces`、`multi_arm`、`tutorials` 等手册及各译本的启用状态和版本。读取实际配置，不因存在预留项而自动编写或启用正文。
- `doc/languages.json` 管理语言元数据及 PDF 字体。新增语言时同时检查此文件和文档清单；配置了语言不等于已有译文。
- 保持不同译本的章节文件名对应；章节链接使用相对路径。修改某个译本不等于其他译本已同步，不应自动提高未更新译本的版本号。
- `doc/conf.py`、`doc/_static/` 和 `scripts/build_docs.py` 是共用构建配置。仅涉及正文时通常无需更改它们。
- `README.md`、`MAINTENANCE.md`、图片清单及 `skills/` 属于仓库维护资料，不加入正式手册的 `toctree`。

新增手册/译本时先完成有效的 `index.md` 和所引用正文，再注册并启用对应组合。构建以清单为准，不为缺失译本生成空白成品或自动回退中文。新增文档类型时按需更新 README 和构建参数帮助文字，不把文档类型硬编码为固定枚举。

翻译以指定语言正文为依据，保持章节顺序、接口标识、消息字段与常量、参数默认值、可执行命令一致；翻译表格、提示和链接文字，保留原有验证范围。可对照代码块、章节覆盖及生成页面的语言检查遗漏；不要把翻译工作描述为重新完成硬件或跨发行版验证。

## Tutorials 与整包下载

Tutorials 解释建模、配置关系和应用开发步骤；quickstart 保持最短启动流程。教程按 `doc/tutorials/<语言>/<主题>/` 组织，通过译本首页和主题 `index.md` 的 toctree 接入。扩展约定写在 README，不在正文加入未来包规划或空章节。源仓库提交、适配修改及验证记录集中在 MAINTENANCE，不为示例重复创建迁移说明或无实际用途的资源清单。

完整示例维护在 `doc/tutorials/examples/<主题>/`。文档内单文件用 literalinclude 和 download 引用；整包下载由 `documents.json` 的 `downloads` 映射声明，键为 ZIP 名称（不带后缀），值为相对该文档根目录的示例目录。`conf.py` 的 builder-inited 回调从当前源码生成 `doc/<document>/downloads/*.zip`，生成目录应忽略提交，不手动维护压缩包副本。

教程首页、主题开篇和末尾保留整包下载，准备页说明解压到同一个工作空间的 `src/`。使用本站 MyST download 链接；PDF 提示从 HTML 同名章节下载。示例修改后重建相关译本，核对 ZIP 文件列表和字节、一级目录、`.setup_assistant` 等隐藏配置及模型资源；确认缓存和构建目录未混入，页面下载与生成包一致。MoveIt 示例适配时按 [教程核对入口](references/source-map.md#moveit-教程示例) 检查模型与控制配置。

## 校对机器人操作内容

涉及包名、可执行名、launch 参数、服务、话题、单位或型号时，按 [源码核对入口](references/source-map.md) 查阅相邻仓库。包名不一定等于仓库名，可执行名也不一定等于源文件名。接口文档同时核对类型定义与回调实现，说明单位、合法范围、名称解析、激活条件、发布行为/QoS 和结果字段；不要只依据注释或字段名推断语义。

将安装、环境加载、启动、状态确认和运动操作写成可跟随的步骤。注明实体机器人、ELIBOTSim 与 Gazebo 各自的地址、时钟及控制器前提；不要互换这些场景的命令。产品支持范围和固件兼容性若无法从代码确认，保留用户提供的依据并将待确认点写入维护记录。

遇到相关软件包本身的问题，在文档任务范围内提供有源码依据的操作方法，并记录限制；修改驱动代码、发布或推送仍须属于用户请求的范围。不要为了验证手册而执行机器人运动或状态切换命令。

## 共用代码示例与多机械臂手册

语言无关的完整模板放在 `doc/<document>/examples/`，各译本用 `literalinclude` 和下载链接引用同一文件，避免重复维护。检查 HTML 下载文件与源文件一致。PDF 长代码需要分段时使用连续且无遗漏的行范围，HTML 和下载仍保留完整代码；不必为一次排版问题改变共用主题或构建引擎。

编写多臂内容时按 [多机械臂核对入口](references/source-map.md#多机械臂组合) 检查包装 launch 与被包含的单臂入口。按实际实现区分独立多实例控制、统一规划场景和协同执行。模板可做语法与纯配置生成检查，覆盖所声明的轴数及前缀组合；不要为了文档验证启动硬件节点或执行运动。

## 图片与编号

语言专用图片放在 `doc/<document>/<language>/images/`，无语言文字的共用资源可按需创建 `doc/<document>/images/` 存放，没有共用资源时不保留占位目录。使用 MyST `figure`，设置唯一的 `:name:`、简明 `:alt:` 和图注。

章节序号取自当前 `toctree` 的顺序，图序号按章节内出现顺序计算。当前中文快速手册采用 `fig-章-序号-说明.png`；显示图号由 Sphinx `numfig` 自动生成，不在图注重复手写。跨文引用图号时使用 `{numref}` 指向标签。

增删或重排图片时，一并检查文件名、`figure` 路径、`:name:`、交叉引用及已有的图片 README、`extraction-manifest.json`；没有清单的教程不必创建清单。主题内图片可放在 `<语言>/<主题>/images/`。避免不可见字符，先核对目标文件名，防止重命名覆盖已有图片。用户只要求整理编号时保留图片字节，无需解读图像内容。

当前提取清单将 `images`（正文现有图片）、`original_extraction`（历史 PDF 提取记录）和 `unused_assets`（辅助资源）分开记录。重命名后更新现有记录，保持原提取记录可追溯；不能因同名就断言用户替换后的图片仍是原图。仅按授权删除资源，未引用的辅助图片不必自动清理。

## 构建与验证

优先使用已有 `.venv`。依赖和字体安装说明见仓库 README；当前 PDF 路径是 MyST → Sphinx → XeLaTeX → PDF，不在普通文档编辑中自行更换引擎。

```bash
.venv/bin/python scripts/build_docs.py \
  --document quickstart --language zh_CN --format all
```

按实际任务替换文档和语言。`--format html` 可单独验证 HTML；共享配置有改动时，构建所有已启用组合：

```bash
.venv/bin/python scripts/build_docs.py --format all
```

输出为 `build/docs/<document>/<language>/html/index.html` 和 `pdf/<document>-<language>.pdf`。CMake/colcon 的 ROS 包名为 `elite_robots_cs_tutorials`，选项为 `BUILD_DOCS`、`BUILD_DOCS_PDF`、`DOCS_DOCUMENT`、`DOCS_LANGUAGE`；具体调用见 README。仅修改维护资料或技能说明时，无需重复构建未改变的正文。

构建脚本将 Sphinx 警告视为失败。按改动检查失效链接、缺图、重复标签、实际生成的图号，以及 LaTeX 日志中的缺字和溢出。长包名/控制器名的表格可使用 MyST `list-table` 的 `:widths:` 调整列宽。不要只凭存在旧成品就声称本次构建成功。

提交前查看 diff 和 `git diff --check`；未跟踪的新文件不会被普通 diff 检查覆盖，暂存后再用 `git diff --cached --check` 检查实际提交内容。用户要求提交时纳入其指定范围；构建产物、虚拟环境及临时检查文件不入库。交付说明给出修改要点、真实验证结果和成品路径；尚未运行的硬件/仿真流程明确说明。

## 技能维护

本技能的受版本管理源文件位于项目 `skills/elite-ros2-docs/`。需要更新时先修改项目版本，验证 frontmatter、相对引用和 `agents/openai.yaml`，再按用户授权同步到环境技能目录，并核对文件一致；不要只改环境副本而漏掉项目提交。
