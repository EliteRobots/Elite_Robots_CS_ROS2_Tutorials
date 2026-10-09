# 来源与修订记录

## 来源

- 文件：`CS&ES&LS_ROS2软件包快速使用手册_Ver2.16.1.pdf`。
- 原手册版本：Ver2.16.1；封面日期：2026-08-07；PDF 共 46 页。
- 本版最初按原 PDF 重写，现已结合用户修订及当前工作空间源码校对命令与接口。
- 最初仅编写快速手册；现已新增中英文接口手册，其独立源码基线见文末记录；usage 仍预留。

## 章节对应

下表使用 PDF 文件的物理页码，不是原手册正文页脚页码。

| 原文 | PDF 页码 | 新文件 |
| --- | --- | --- |
| 封面、阅读说明 | 1、3 | `doc/quickstart/zh_CN/index.md` |
| 第 1 章概述 | 7～11 | `doc/quickstart/zh_CN/overview.md` |
| 第 2 章机器人端配置 | 13～26 | `doc/quickstart/zh_CN/robot_setup.md` |
| 第 3 章本地环境安装 | 27～32 | `doc/quickstart/zh_CN/installation.md` |
| 第 4.1 节驱动基础教程 | 33～41 | `doc/quickstart/zh_CN/driver.md` |
| 第 4.2 节 MoveIt 2 | 41～42 | `doc/quickstart/zh_CN/moveit.md` |
| 第 4.3 节 Gazebo | 42～44 | `doc/quickstart/zh_CN/gazebo.md` |
| 封底联系方式 | 46 | `doc/quickstart/zh_CN/support.md` |

## 当前源码核对（2026-09-24）

核对基于工作空间文件内容，未执行机器人操作：

- Driver：`Elite_Robots_CS_ROS2_Driver`，Humble 分支；核对 launch 参数、CMake 安装的可执行名、Python/C++ 示例、控制器配置和服务实现。
- Description：`Elite_Robots_CS_ROS2_Description`，Humble 分支；核对型号选项、五轴配置和接收超时默认值。
- GZ Simulation：`Elite_Robots_CS_ROS2_GZ_Simulation`，Humble 分支；核对仿真启动文件、默认控制器与脚本。
- SDK：`Elite_Robots_CS_SDK`；核对容器脚本参数、默认地址、控制软件最低版本声明以及外部控制行为。

主要修正：

1. Python 可执行名改为 `example_safe_joint_move_py`，使用 ROS 参数；C++ 保留 `example_safe_joint_move`。两者 `max_vel` 单位为 rad/s，仅用于估算轨迹时长。
2. MoveIt 使用 `elite_robots_moveit_config/elite_moveit.launch.py`；补全外部控制脚本与轨迹控制器状态要求。
3. 控制器表与当前 YAML 一致，速度缩放广播话题为百分比（0～100）。任务状态 `2` 为 `PLAYING`，脚本发送成功与正在运行分别确认。
4. 说明 `cs_type` 的小写选项、六轴示例限制、容器 IP 与计算机 Local IP 的区别，以及自动选择 Local IP 的行为。
5. ELIBOTSim 默认控制柜 ID 修正为 1，列明脚本默认镜像与 SDK 最低版本声明的差异。
6. Gazebo 正文提供分步启动、标准轨迹控制器选择及按需时钟桥接流程；按用户确认，以 1.0.2 为当前已修复的适配版本。本次未修改相关软件包源码。
7. 保留用户的 ROS apt 软件源安装流程，增加发行版环境和二进制包候选版本检查。ROS 安装参考 [官方 Humble 文档](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)，桥接参考 [ros_gz_bridge Humble 文档](https://github.com/gazebosim/ros_gz/blob/humble/ros_gz_bridge/README.md)。

## 仍需产品或运行环境确认

- 用户提供的 CS/ES/LS 支持范围、Humble/Jazzy 正式支持声明、控制柜网络条件和示教器菜单行为予以保留；本次本地源码核对不等同于这些平台及硬件的实测。
- 当前 launch 未提供 `es*` 型号选项；ES 产品与配置型号之间的对应关系应由产品方明确，正文未自行推断映射。
- SDK README 声明最低控制软件版本 2.15.0，而容器脚本默认镜像为 2.14.5；实际可用镜像标签及版本兼容性需发布方确认。
- ROS 二进制包可能落后于本地源码，需按实际发布版本复核。
- 图片内容按用户要求未分析；历史来源记录不能证明用户替换后的图片仍是原 PDF 内容。
- `package.xml` 维护者和 Proprietary 许可由项目方在发布前确认；未执行 bloom-release。

## 图片维护

正文图片已按当前章节与出现顺序重新编号，文件名与 `:name:` 同步更新，并移除不可见字符。MoveIt、Gazebo 和联系方式分别归入第 5、6、7 章；已删除图片不再出现在当前清单中。

当前正文图片清单见 `doc/quickstart/zh_CN/images/README.md`；当前文件元数据与历史 PDF 提取记录分开保存在 `extraction-manifest.json`。图片内容保持原样，`source-assets/` 辅助资源保留。

## 多语言目录迁移

- 中文正文迁移到 `doc/quickstart/zh_CN/`，内容和章节间相对链接保持不变。
- 语言相关图片放在各语言目录的 `images/`；当前没有共用图片，已移除仅含说明文件的 `doc/quickstart/images/`，后续需要时再创建。
- `doc/documents.json` 按文档及语言管理标题、版本、启用状态。
- `doc/languages.json` 集中管理语言名称、作者、版权及 PDF 字体配置，预设 `zh_CN`、`en`、`fr`。
- 构建脚本增加 `--language`，CMake 增加 `DOCS_LANGUAGE`；默认构建所有已启用的文档/语言组合。
- 成品输出到 `build/docs/<文档>/<语言>/html/` 和 `pdf/<文档>-<语言>.pdf`。
- 最初仅迁移中文正文；现已补充英文 quickstart 及中英文接口手册，法文和 usage 尚未编写。
- `README.md`、本文件及图片目录说明属于仓库维护资料，不加入正式手册目录。

## 文档版本与适配版本（2026-09-24）

- 中文快速手册正式文档版本设为 `1.0.0`，同步 `doc/documents.json`、正文首页及修订记录。原始 PDF 的 `Ver2.16.1` 继续作为来源版本保留。
- 适配版本读取自工作空间各包 `package.xml`：Driver 仓库内七个 ROS 包为 `1.2.0`，Description 为 `1.0.0`，SDK 为 `1.4.7`。
- 按用户确认，Gazebo `1.0.2` 作为当前已修复的适配版本记录，移除正式手册中的计划修复说明。本次未改动 Gazebo 源码或其包版本，也未新增运行验证结论。
- `changelog.md` 加入正式 HTML/PDF，追加在目录末尾以保持原章节及图片编号。本文档包 `elite_robots_cs_tutorials` 的包版本仍为 `0.1.0`，与手册版本独立管理。

## HTML 主题与正文清理

HTML 改为本地 `elite` 主题，继承 Sphinx `basic`，通过模板、CSS 和 JavaScript 提供三栏布局、品牌导航、页内目录、搜索及代码复制。样式参考 https://docs.elibot.cn/cs/1ffff/9a93b ，未引入其站点服务或远程样式依赖。

正式手册已移除原始资料版本、重写说明及“原手册”措辞。历史来源和提取记录仅作为仓库维护资料保留；原有章节、图号及文档版本保持不变。

## 英文快速手册（1.0.0）

- 新增 `doc/quickstart/en/`，章节文件名和顺序与中文一致，翻译全部九个正文文件并启用独立 HTML/PDF 构建。
- 保留适配版本及验证范围，Gazebo 按当前适配版本 1.0.2 记录；翻译不新增硬件验证声明。
- 命令和示例输出直接复用中文源文件，仅翻译注释及 Python 示例中的显示文字；UI 名称采用英文描述，未验证所有版本示教器的英文菜单文字。
- 24 幅正文图片原样复制至英文图片目录，图注及替代文本译为英文，未重新分析图片内容；中文正文仅修正下述目录结构。英文版首页说明截图界面语言保持原样。

- 构建英文版时发现首页二级标题会让 LaTeX 中的正文目录嵌套为下级章节；中英文首页改用带显式锚点的 `rubric`，保持版本链接有效，并恢复独立的八章及对应图号。

## 中文接口手册源码基线（2026-09-24）

用户本次明确指定 `/home/cc/elite_ros_ws/src`，它与 Tutorials 所在的 `/home/cc/project/elite_ros_ws/src` 不是同一份 checkout。接口手册以本次指定目录为准，不沿用快速手册的包版本或 Gazebo 修复结论。三个源码仓库核对时工作树均干净，均为 `humble` 分支：

| 仓库 | HEAD | package.xml 版本 |
| --- | --- | --- |
| Elite_Robots_CS_ROS2_Description | `edbbfdca9220ce264c99ec51d37440ff4fa13a9a` | 1.0.0 |
| Elite_Robots_CS_ROS2_Driver | `ce37530dd197d1ff4669b193f50803acd9622461` | 七包均为 1.0.3 |
| Elite_Robots_CS_ROS2_GZ_Simulation | `241d9836ae4b42eecf48459181c3467523610dce` | 1.0.1 |

核对入口：各 `package.xml`、`CMakeLists.txt`，Description 的 launch/URDF，Driver 的 launch、控制器 YAML、hardware_interface、Dashboard/Primary/script/loader/controller_stopper 源码、控制器实现与参数定义、全部 msg/srv、MoveIt launch/SRDF/Servo 配置、校准与示例，以及 GZ launch/YAML/脚本。标准动作字段辅助核对了本机 `/opt/ros/humble/share/control_msgs/action/FollowJointTrajectory.action`，未将其视为仓库锁定的依赖版本。

接口手册独立注册为 `interfaces/zh_CN` 1.0.0，消息章节完整纳入 6 个 msg、11 个 srv，launch 索引从所核对源码声明提取并配中文语义。未改动这三个仓库、快速手册正文和未编写语言的版本。

本次发现并在接口文档说明的实现限制（非已修复声明）：

- GPIO 速度滑块实际范围为 [0.01, 1.0]，与 srv 注释不一致；IO 数字边界使用 `<= count`，模拟通道校验范围也过宽。
- 异步等待标记为 2.0，等待超时后部分服务仍转为 bool，可能返回 true；要求应用读回状态。
- hardware `joint_efforts_` 来自 `getActualJointCurrent()`，不能按力矩解释。
- 速度缩放广播器比较单次 period，且 `Duration(1.0 / publish_rate_, 0.0)` 存在秒值转换问题，不能保证配置的 100 Hz。
- robot_mode/safety_mode/task_running 只在变化时发布；只有 task_running 设置 transient_local，初始值未变化不保证已发样本。
- 组件进程在 Dashboard 初次连接失败后移除节点；controller stopper 仍等待 Dashboard 查询服务。
- Xacro tool_voltage 参数未被硬件初始化应用，工具通信参数不是已实现的 ROS 串口接口。
- MoveIt/GZ 的 prefix 与 Description 的 tf_prefix 不一致，非空前缀不能直接使用；MoveIt 的 use_sim_time 未同步到 Servo/RViz。
- GZ 1.0.1 组合 launch 引用不存在的 cs_moveit.launch.py；没有启动 /clock 桥；部分 YAML 使用遗留 cs_controllers 插件名。正文提供默认标准控制器的分步启动方式。
- GZ CMake 安装的脚本名为 gz_control.py，源文件注释中的 gz_control 不准确；脚本及驱动单目标示例固定六轴无前缀名称。
- 校准 launch 的 target_filename 映射节点 output_filename，结果不会自动注入模型；驱动 launch 无独立校准路径覆盖项。

仍需确认：模拟输出写入值的量纲/范围、工具模式枚举及工具反馈物理量的控制器版本契约；ROS 封装没有给出完整约束，正文不凭字段名虚构范围。实机、ELIBOTSim、Gazebo、Servo 与非空前缀流程均未运行验证。本次构建验证结果如下。

### 接口手册交付验证

- 执行 `.venv/bin/python scripts/build_docs.py --format all`，中英文 quickstart 与中文 interfaces 的 HTML/PDF 均成功生成（Sphinx 警告作为错误）。
- 针对长接口名调整接口手册表格后，再执行 `--document interfaces --language zh_CN --format all` 成功，最终 PDF 共 42 页。
- 最终接口 PDF 的 XeLaTeX 日志无 Overfull、无 Missing character；保留引擎通用 cmap 提示及少量 Underfull 排版提示，不影响构建。
- 校验接口 HTML 的 14 个页面（含索引/搜索辅助页）中的 672 个本地链接及锚点，全部有效。
- 17 个自定义类型的字段、常量、顺序与指定源码一致；Dashboard/Primary/script/GPIO/自由拖动/速度缩放的自定义端点名称均已覆盖。
- `git diff --check` 通过；未执行机器人控制、实机测试、ELIBOTSim、Gazebo 或 Servo 集成运行。
- 输出：`build/docs/interfaces/zh_CN/html/index.html`、`build/docs/interfaces/zh_CN/pdf/interfaces-zh_CN.pdf`。构建产物未纳入版本管理。

## 英文接口手册（1.0.0，2026-09-28）

- 新增 `doc/interfaces/en/` 全部 12 个章节文件，章节文件名和目录顺序与中文 1.0.0 对齐；启用 `interfaces/en` 独立 HTML/PDF。
- 翻译正文、表格、提示、目录、链接文字、消息字段说明和 launch 参数索引；保留所有 bash/text/yaml 代码块原文，覆盖 6 个 msg、11 个 srv。
- 沿用中文于 2026-09-24 核对的 Description 1.0.0、Driver 1.0.3、GZ 1.0.1 基线及已知限制。本次为翻译，未重新声明代码修复或进行机器人/仿真验证。
- 结合用户关于分支的澄清，英文首页明确 Humble 是源码核对基线，不是要求文档仓库按发行版分支；Jazzy 尚未核对。中文正文及版本号未改动。
- 对照检查：12 个对应文件的标题层级数量一致，bash/text/yaml 代码块逐字相同；英文正文无遗留中文，接口标识和默认值保持不变。

- 构建验证：先独立构建英文接口手册，再执行 `.venv/bin/python scripts/build_docs.py --format all`，四个已启用组合（quickstart/interfaces × zh_CN/en）的 HTML/PDF 均成功；Sphinx 无警告。
- 英文最终 PDF 为 42 页，XeLaTeX 日志无 Overfull 和 Missing character。英文 HTML 共 14 页（含辅助页），672 个本地链接/锚点有效，页面语言均为 en，可见文本无遗留中文。
- 中英文接口手册 toctree 顺序相同；所有中文正文中的技术标识均在对应英文文件中保留。`git diff --check` 通过。
- 英文输出：`build/docs/interfaces/en/html/index.html`、`build/docs/interfaces/en/pdf/interfaces-en.pdf`。构建产物及临时校验脚本未纳入版本管理。

## 多机械臂手册（1.0.0，2026-10-08）

- 用户指定参考 `/home/cc/project/elite_ros_ws/src/Elite_Robots_CS_ROS2_Driver/elite_robots_driver/doc/MultiArm_CN.md`。该目录与旧 interfaces 手册使用的 `/home/cc/elite_ros_ws/src` 不同，不将旧版 1.0.3 的限制套用到本次 1.2.0 文档。
- Driver：humble，HEAD `f36c671`，包版本 1.2.0，核对时工作树干净；Description：HEAD `edbbfdc`，包版本 1.0.0。
- 核对单臂驱动 launch 的 controller_manager_name/spawn_controllers、绝对控制器路径、update rate 节点键；MoveIt launch 的 prefix/tf_prefix、绝对配置路径、kinematics_file/rviz_config_file/prefer_scaled_controller；配套五轴/六轴控制器 YAML、运动学和 RViz 模板及 Description 的 mock 资源。
- 新增独立 `multi_arm/zh_CN` 与 `multi_arm/en`，各六个 Markdown 文件，共享两个完整 Python launch 模板，通过 literalinclude 和 download 同时用于正文与下载。
- 参考中的两段 Python 原样提取，仅将最终绿色日志从“All required controllers are ready.”改为“Arm2 spawner chain exited; verify both controller managers.”：OnProcessExit 不检查退出码，且 arm2 结束不保证 arm1 已完成。
- 正文说明该方案是两个独立单臂规划实例，不提供联合模型、跨臂碰撞检测或同步执行；实际安装变换需单独集成。临时文件 delete=False、模板文本替换依赖固定结构、local_ip 未由包装模板暴露、OMPL/关节限制配置未整体前缀化等边界亦已说明。
- 离线验证两份 Python 语法，运行其中纯配置生成函数：arm1/arm2 × cs63/cs520h × driver/MoveIt 共 8 组控制器 YAML 的键、前缀与关节数通过；两臂的运动学规划组和 RViz namespace/轨迹话题通过。未运行 launch 或连接硬件。
- 中英文 bash/text 代码块一致；修订日期为 2026-10-08，文档版本均为 1.0.0。仅更新构建参数帮助文字以适配动态文档清单，未改动相邻驱动实现及旧手册正文。

- 构建验证：`--format all` 已成功构建六个启用组合的 HTML/PDF；之后仅调整 multi_arm 的 PDF 长代码分页，并重新构建中英文 multi_arm HTML/PDF 成功。最终中文版 25 页，英文版 24 页，均无 Overfull 或 Missing character；Sphinx 无警告。
- 长模板在 HTML 中完整展示，PDF 按连续 32 行分段并保持段内完整，引用同一源文件，不删减代码。两种语言各 8 个 HTML 页面、197 个本地链接/锚点检查通过，下载文件字节与源模板一致。
- `git diff --check` 通过；未执行机器人运动、状态切换、fake hardware 或 MoveIt 集成运行。构建产物与临时检查脚本不入库。
- 输出：`build/docs/multi_arm/<语言>/html/index.html` 和 `build/docs/multi_arm/<语言>/pdf/multi_arm-<语言>.pdf`。

## 多机械臂原文替换（1.0.0，2026-10-09）

- 按用户要求，中文直接采用 `/home/cc/project/elite_ros_ws/src/Elite_Robots_CS_ROS2_Driver/elite_robots_driver/doc/MultiArm_CN.md`，英文直接采用同目录 `MultiArm.md`，替换上次另行编写的正文。来源仓库分支 `humble`，提交 `f36c67135dc300043ff86e5e70fbdc9b36131799`，`elite_robots` 包版本 1.2.0，读取时工作树干净。
- 原文导言保留在各译本 `index.md`，原文六节依次对应 `launch_files.md`、`driver.md`、`startup.md`、`control.md`、`moveit.md`、`single_arm.md`。仅提升章节标题层级并添加 toctree，不叠加自动编号；旧版 overview、operation、changelog 已移除。
- bash/text 代码块改为 MyST `code-block`；两份原文完全相同的 Python 代码提取到共用 examples，以 `literalinclude` 引用，将模板文件名展示转换为同名 download 链接。HTML 保持完整代码，PDF 按连续 32 行分段，无遗漏。驱动模板的最终日志恢复为源文档中的 `All required controllers are ready.`，不保留上次的改写。
- 将上述格式转换还原后，两份文档均与各自源文件逐字一致；共用模板与原文代码一致，Python 静态语法解析通过。本次未重新校对驱动实现，也未执行硬件、fake hardware、MoveIt 或运动操作；上节记录仅描述旧版的历史工作。
- 执行 `.venv/bin/python scripts/build_docs.py --document multi_arm --format all` 成功生成中英文 HTML/PDF，Sphinx 无警告，最终 LaTeX 日志无 Overfull 或 Missing character。LaTeX 仍提示 cmap 在 XeLaTeX 下退出，以及英文构建依赖中的旧 hook 弃用提示。
- 两种语言分别核对 9 个 HTML 页面、144 个本地链接/锚点、2 个下载文件及完整代码展示；下载字节与共用模板一致。已清理本次输出中被替换章节的旧 HTML 和旧模板下载副本，`git diff --check` 通过。
- 成品仍位于 `build/docs/multi_arm/<语言>/html/index.html` 和 `build/docs/multi_arm/<语言>/pdf/multi_arm-<语言>.pdf`；未修改共用构建配置、相邻源码或其他手册。

## 多机械臂手动修订同步（1.0.0，2026-10-09）

- 当前正文基准改为用户手动修订后的 `doc/multi_arm/zh_CN/`，英文同步导言、示例文件存放说明、每个新终端加载工作空间的说明、逐臂控制器查询及轨迹 action 查询、虚拟/真机启动措辞和 MoveIt 标题。此后正文不再与上节记录的外部 Markdown 原文逐字一致。
- 用户删除的单臂启动章节已从英文正文及两种语言的 toctree 同步移除。当前为首页加五节：`launch_files.md`、`driver.md`、`startup.md`、`control.md`、`moveit.md`；README 已更新。上节六节结构仅为迁入时的历史记录。
- 共用 launch 模板未改动，其中 `single_arm_launch` 仍是双臂模板包含单臂入口所需的变量，与删除手册章节无关。
- 项目和环境中的 `elite-ros2-docs` 技能已同步，补充手动修订后的译文基准、章节删除及生成文件残留检查规则；技能格式、相对引用、UI 元数据和两份目录一致性校验通过。
- 中英文六个 Markdown 文件逐一核对，bash/text 代码块、literalinclude 及 toctree 一致。`--document multi_arm --format all` 构建成功，Sphinx 无警告，最终 LaTeX 日志无 Overfull 或 Missing character；未运行硬件、仿真或运动操作。
- 清理两种语言构建输出中的旧单臂章节 HTML 和 doctree，确认当前 HTML、搜索索引及 PDF 源码均不再包含该章节。下载文件与共用模板字节一致，完整代码展示及本地链接/锚点检查通过。

## Tutorials 迁移（1.0.0，2026-10-08）

### 来源与组织

- 用户指定来源：[Elite-Robots/Elite_Robots_CS_Ros2_Tutorials](https://github.com/Elite-Robots/Elite_Robots_CS_Ros2_Tutorials)，main 提交 `6488bbff2c8631c1e076150687df9e7c3605332b`。
- 读取 `README.md`、`README_CN.md`、`tutorials/Elite Robots ROS2 教程.md`、`tutorials/Elite Robots ROS2 tutorials.md`，以及 `hello_moveit/`、`my_elite_robot_cell/` 中的配套实现。按用户要求不保留迁入的独立 LICENSE 文件；示例 package.xml 中的许可声明保留，hello_moveit 的 TODO 声明按源仓库根许可补为 Apache-2.0。
- 注册独立的 `tutorials/zh_CN` 和 `tutorials/en`，各八个 Markdown 文件。结构为 `doc/tutorials/<语言>/<主题>/`，当前主题 `moveit`；通用构建脚本和主题不需增加固定类型分支。扩展约定仅写 README，正式正文无预留章节或未来包规划。
- 两种语言各保留 13 幅原截图，字节未修改，放在各自 `moveit/images/`。截图中的旧路径、界面和旧示例运行效果不作为当前参数依据；正文说明以当前文字和配套文件为准。
- 四个语言无关示例包放在 `doc/tutorials/examples/moveit/`，通过 literalinclude 与单文件下载引用同一份代码。`examples/COLCON_IGNORE` 防止作为文档资源扫描时误识别；教程明确复制两个子目录到独立工作空间后构建。它们随现有 CMake 的 `doc` 资源安装，无需启动节点。

| 原教程范围 | 中英文对应章节 |
| --- | --- |
| README 安装/构建与自定义工作单元概述 | `moveit/index.md`、`moveit/preparation.md` |
| 1. 组装 URDF：工作单元描述、宏与 RViz | `moveit/workcell.md` |
| 2. 启动驱动：ros2_control、标定与包装 launch | `moveit/control.md` |
| 3. MoveIt 配置：Setup Assistant、限制与运行 | `moveit/configuration.md` |
| 4. C++：创建包、节点、位姿/关节目标与执行 | `moveit/cpp.md` |

### 源码核对与修正

以 `/home/cc/project/elite_ros_ws/src` 为本次基线：

- Driver：humble，`f36c67135dc300043ff86e5e70fbdc9b36131799`，ROS 包版本 1.2.0；核对时工作树干净。
- Description：humble，`edbbfdca9220ce264c99ec51d37440ff4fa13a9a`，版本 1.0.0；核对时工作树干净。
- 本机 Humble 的 MoveItConfigsBuilder、launch 生成函数与 C++ 头文件用于确认配置加载和客户端 API。构建使用该工作空间已安装的驱动/模型下层环境；已用 cmp 确认其 `cs_macro.xacro`、`cs.ros2_control.xacro` 和 `elite_control.launch.py` 与上述源码一致。
- 将源文和示例中的 `eli_cs_robot_description`、`eli_cs_robot_driver`、`eli_cs_robot_calibration`、`eli_cs_controllers` 改为实际 `elite_robots_*` 名称。移除示例清单中非 ROS 包名的 SDK 直接依赖，保留驱动声明的传递依赖；修正源码中的 TODO 包描述、许可及依赖。
- 自定义包名保持 `my_elite_robot_cell_*` 与 `hello_moveit`。示例只声明已完整配置的六轴 CS63，不沿用原包装 launch 接受其他型号但缺少对应配置的行为。
- 保留桌子、显示器、墙体和机械臂的结构与资源。补齐场景宏的前缀/安全参数传递，控制 Xacro 使用驱动实际传入的脚本、配方、回连端口和工具参数名；仅添加一个 ros2_control 系统。
- 当前驱动 launch 从 description_package 的 config/cs63 读取参数，不声明原文中的 kinematics_params_file。将模型参数集中维护于示例描述包，控制包 CMake 安装同一来源的副本；标定导出后替换该源文件并重建两个包，确保 MoveIt 与驱动的几何一致。取消原示例中未被使用的独立 my_elite_robot_calibration.yaml。
- fake hardware 默认使用标准 joint_trajectory_controller，实体模式命令明确使用 scaled_joint_trajectory_controller；MoveIt 包装 launch 根据 use_fake_hardware 选择对应 YAML。此参数只决定 MoveIt 映射，不启动硬件。显式选用 OMPL，避免自动加载未使用的规划器。
- 保留原关节限制示例 4.0 rad/s² 和 0.1 缩放，去除“机械臂没有物理加速度限制”和“保守安全值”的泛化结论；说明其为规划示例值，需要结合实际应用确定。
- C++ 示例将零四元数改为单位四元数，指定 world/cs63_tool0，增加执行器线程、当前状态等待、显式关节名、规划/执行结果判断、失败退出及默认仅规划开关。客户端 launch 直接注入同一工作单元 URDF、SRDF 和运动学参数，补全 CMake 与 package.xml。
- 本次未修改相邻驱动、模型仓库或已有 quickstart/interfaces/multi_arm 正文；未执行硬件、fake hardware、Gazebo、MoveIt 节点启动或机器人运动。

### 验证

- 四个示例包通过本机 Humble colcon 编译，包括 hello_moveit C++；构建、安装和日志仅位于 `/tmp/elite-tutorials-validation/`。
- 离线展开显示模型及 fake/实体控制模型，检查唯一 world 根、六轴关节名、单个 ros2_control 系统、两种硬件插件、脚本/配方/IP/端口参数、网格资源路径，以及显示与控制几何相同。
- 用实际 MoveItConfigsBuilder 加载两套控制器配置，核对 URDF、SRDF 链、碰撞排除项引用的连杆、关节限制与 URDF 速度上限、控制器动作及关节集合。检查全部 Python/XML 语法、构造所有 launch 描述，不访问或执行其中节点。
- 两个译本的章节路径、bash/XML 命令及 literalinclude 来源一致；所有 PDF 代码分段连续且覆盖完整源文件。长代码在 PDF 中以 24 行以内的 minipage 分段，HTML 和下载保持完整。

- 最终执行 `.venv/bin/python scripts/build_docs.py --format all`，八个启用组合的 HTML/PDF 全部成功。新增教程 Sphinx 无警告，最终 XeLaTeX 日志无 Overfull、无 Missing character。
- 中文 10 个 HTML 页面共 400 个本地链接/资源引用、英文 10 页共 390 个引用检查通过；每种语言的 10 个代码下载均与源文件字节一致，各 13 幅图片与源仓库字节一致。
- `git diff --check` 通过；未跟踪的新文件另行检查无行尾空格。构建产物、编译输出、临时校验脚本不入库。
- 成品：`build/docs/tutorials/<语言>/html/index.html`、`build/docs/tutorials/<语言>/pdf/tutorials-<语言>.pdf`。本次验证不包括实体机器人或仿真集成运行；Jazzy 未验证。

## Tutorials 示例整包下载（2026-10-08）

- 按用户要求，在中英文 Tutorials 首页、MoveIt 开篇、工作空间准备页及 C++ 章节末尾加入 `hello_moveit.zip` 与 `my_elite_robot_cell.zip` 下载，来源为当前仓库的示例目录。
- `doc/documents.json` 声明下载目录映射，Sphinx `builder-inited` 回调从当前文件生成 ZIP。输出保留一级示例目录，分别包含一个和三个 ROS 包；保留 `.setup_assistant`、模型和配置文件，排除构建目录、Git 和 Python 缓存。压缩包加入 `.gitignore`，不维护源码副本。
- 文档使用本地 MyST download 链接，由 Sphinx 将 ZIP 复制到站点 `_downloads`；没有 GitHub 下载跳转。准备页以下载、解压到同一个工作空间的 src、安装依赖并构建为主流程，保留已有 checkout 的复制方式。PDF 指向 HTML 同名章节的下载入口。
- 验证 ZIP 分别包含 5 和 35 个文件，文件列表及每个文件字节与当前示例一致；解压后分别识别一个和三个 package.xml。测试了隐藏配置保留、缓存排除、源文件修改/删除后更新，以及源文件不变时 ZIP 字节与修改时间稳定。
- 共享配置改动后，八个已启用文档组合的 HTML/PDF 全部构建通过；随后为首页补充链接，仅重建中英文 Tutorials。最终教程 Sphinx 无警告，PDF 无 Overfull 或 Missing character。各语言四个入口页面的两个 ZIP 均为有效的本站下载，下载文件与生成 ZIP 字节一致。

## 提交前清理与技能同步（2026-10-08）

- 删除两份重复的示例 `MIGRATION.md`，迁移来源及适配说明集中保留在本文件；删除未使用的 `pilz_cartesian_limits.yaml`，示例所有规划入口均显式使用 OMPL。
- 核查 DAE 的纹理引用、Xacro/launch 的配置和模型引用、正文图片引用；保留运行和文档需要的资源。ZIP 属于用户需要的下载成品，保持自动生成和 Git 忽略，不纳入提交。
- 清理后重新构建中英文 Tutorials HTML/PDF，两个下载包分别为 4 和 33 个文件，与当前源码逐文件一致；使用当前源目录加载 fake/实体两套 MoveIt 配置通过，不依赖被删除的 Pilz 文件。
- 先更新项目 `skills/elite-ros2-docs/` 的 SKILL.md、源码核对入口及 UI 元数据，增加 Tutorials、整包下载、资源清理和项目优先的技能维护说明；技能验证通过后同步到环境 `/home/cc/.codex/skills/elite-ros2-docs/`，再次验证并核对三个文件一致。
