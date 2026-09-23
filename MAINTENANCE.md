# 来源与修订记录

## 来源

- 文件：`CS&ES&LS_ROS2软件包快速使用手册_Ver2.16.1.pdf`。
- 原手册版本：Ver2.16.1；封面日期：2026-08-07；PDF 共 46 页。
- 本版是可编辑的 MyST 重写稿，暂按来源内容组织，不按当前驱动实现替换包名与接口。
- 仅编写快速手册；usage 和接口手册仅在构建清单中预留，未生成正文。

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

## 本次做出的基础修正

1. 统一 ROS 2、MoveIt 2、RViz 等写法，重新分段，将 PDF 中跨行的命令恢复为可复制的代码块。
2. ROS 2 命令表中的 `roslaunch` 改为 `ros2 launch`；说明 `ros2 node kill` 非标准 Humble 命令，提供前台进程 `Ctrl+C` 的操作方式。
3. `ros2 topic type` 的说明明确为返回类型名称，消息字段通过 `ros2 interface show` 查看；长破折号形式的帮助选项改为 `--help`。
4. 机器人 TCP 测试脚本按文字说明使用 Local IP，修正原代码中的 `Your.Robot.IP.Addr`。
5. TCP 服务端由仅监听 `localhost` 改为 `--host <local_ip>`，保留 50001 端口和 Hello SDK 测试目的；整理连接关闭、接收超时和中断处理。
6. 说明 `rosdep init` 仅初始化一次、Docker 用户组变更需重新登录、多个终端需分别加载环境。
7. 原仿真脚本帮助头写作 `start_elibot_sim.sh`，正文使用 `start_elibotsim.sh`；本版统一沿用正文名称，并保留原参数默认值。
8. Gazebo 概述保留物理仿真与 ROS 集成用途，精简与快速操作无关的渲染器及物理引擎枚举，不新增支持声明。
9. 保留原手册的关节目标数值，包括话题与动作示例中不同的第二关节目标；将 YAML 改为易读的分行形式。

## 后续需要结合项目核对

- `eli_*` 包名与当前项目结构；本次未迁移。
- CS/ES/LS65 支持范围、控制柜差异、软件 2.14.3 的 headless 网络条件。
- 镜像默认标签 2.14.5 与手册版本 2.16.1 的区别。
- `cc612` 型号字符串、型号大小写及驱动参数。
- 仿真时 `robot_ip` 使用宿主机地址这一前提与实际容器网络模式。
- `/usr/share/gz/setup.bash` 在实际系统中是否存在。
- Python、C++ 示例同名 `example_safe_joint_move`，以及原链接指向 Python launch 文件的差异。
- `max_vel` 的单位/比例语义和程序实际实现。
- ROS、Docker、Gazebo、fishros 安装方式及原文外部链接是否仍适用于发布时的目标环境。本次未联网更新原文安装流程。
- SDK 安装需衔接另一本 C++ SDK 手册；来源未提供具体命令，未自行补写。
- 所有机器人指令仅整理为文字，没有做硬件验证。
- 当前 `package.xml` 的维护者借用现有驱动信息；许可保留原手册所有权利声明，发布前由项目方确认。

## 图片清单

正文全部使用可同时构建到 HTML/PDF 的文本占位，不依赖缺失图片。

- 原图 1-1：软件包结构。
- 原图 2-1～2-4：远程控制设置。
- 原图 2-5～2-8：任务和脚本编辑。
- 原图 2-9～2-10：脚本保存。
- 原图 2-11：测试任务运行。
- 原图 2-12：仿真脚本位置。
- 原图 2-13～2-14：镜像与虚拟示教器。
- 原图 3-1：ROS 2 安装验证。
- 原图 4-1～4-3：上电、抱闸、正常模式。
- 原图 4-4～4-5：RViz 与示教器姿态。
- 原图 4-6：待机状态。
- 原图 4-7：任务状态结果。
- 原图 4-8：控制器列表。
- 原图 4-9：轨迹执行结果。
- 原图 4-10：MoveIt 2 规划。
- 原图 4-11：Gazebo 启动。
- 封底公众号二维码。

共保留原正文 27 幅编号图片以及 1 处二维码占位。封面品牌排版以文字封面代替，不提取原图。


## 多语言目录迁移

- 中文正文迁移到 `doc/quickstart/zh_CN/`，内容和章节间相对链接保持不变。
- 语言相关图片放在各语言目录的 `images/`；无语言文字的共用图片放在 `doc/quickstart/images/`。
- `doc/documents.json` 按文档及语言管理标题、版本、启用状态。
- `doc/languages.json` 集中管理语言名称、作者、版权及 PDF 字体配置，预设 `zh_CN`、`en`、`fr`。
- 构建脚本增加 `--language`，CMake 增加 `DOCS_LANGUAGE`；默认构建所有已启用的文档/语言组合。
- 成品输出到 `build/docs/<文档>/<语言>/html/` 和 `pdf/<文档>-<语言>.pdf`。
- 此次仅迁移中文正文，没有创建英文、法文、usage 或接口手册正文。
- `README.md`、本文件及图片目录说明属于仓库维护资料，不加入正式手册目录。
