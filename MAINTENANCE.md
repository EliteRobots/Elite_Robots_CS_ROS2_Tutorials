# 来源与修订记录

## 来源

- 文件：`CS&ES&LS_ROS2软件包快速使用手册_Ver2.16.1.pdf`。
- 原手册版本：Ver2.16.1；封面日期：2026-08-07；PDF 共 46 页。
- 本版最初按原 PDF 重写，现已结合用户修订及当前工作空间源码校对命令与接口。
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

## 当前源码核对（2026-09-24）

核对基于工作空间文件内容，未执行机器人操作或 Gazebo 运行验证：

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
6. GZ 组合启动文件仍引用不存在的 `cs_moveit.launch.py`；正文改用分步启动并选择标准轨迹控制器。当前仿真 launch 未显式桥接 `/clock`，正文补充检查和按需桥接步骤。此次未修改相关软件包源码。
7. 保留用户的 ROS apt 软件源安装流程，增加发行版环境和二进制包候选版本检查。ROS 安装参考 [官方 Humble 文档](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)，桥接参考 [ros_gz_bridge Humble 文档](https://github.com/gazebosim/ros_gz/blob/humble/ros_gz_bridge/README.md)。

## 仍需产品或运行环境确认

- 用户提供的 CS/ES/LS 支持范围、Humble/Jazzy 正式支持声明、控制柜网络条件和示教器菜单行为予以保留；本次本地源码核对不等同于这些平台及硬件的实测。
- 当前 launch 未提供 `es*` 型号选项；ES 产品与配置型号之间的对应关系应由产品方明确，正文未自行推断映射。
- SDK README 声明最低控制软件版本 2.15.0，而容器脚本默认镜像为 2.14.5；实际可用镜像标签及版本兼容性需发布方确认。
- ROS 二进制包可能落后于本地源码，需按实际发布版本复核；Gazebo 分步启动流程尚未运行验证。
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
- 此次仅迁移中文正文，没有创建英文、法文、usage 或接口手册正文。
- `README.md`、本文件及图片目录说明属于仓库维护资料，不加入正式手册目录。

## 文档版本与适配版本（2026-09-24）

- 中文快速手册正式文档版本设为 `1.0.0`，同步 `doc/documents.json`、正文首页及修订记录。原始 PDF 的 `Ver2.16.1` 继续作为来源版本保留。
- 适配版本读取自工作空间各包 `package.xml`：Driver 仓库内七个 ROS 包为 `1.2.0`，Description 为 `1.0.0`，SDK 为 `1.4.7`。
- 按用户指定，Gazebo 适配目标版本记录为 `1.0.2`；当前包声明为 `1.0.1`，修复及运行验证待完成。本次未改动 Gazebo 源码或其包版本。
- `changelog.md` 加入正式 HTML/PDF，追加在目录末尾以保持原章节及图片编号。本文档包 `elite_robots_cs_tutorials` 的包版本仍为 `0.1.0`，与手册版本独立管理。

## HTML 主题与正文清理

HTML 改为本地 `elite` 主题，继承 Sphinx `basic`，通过模板、CSS 和 JavaScript 提供三栏布局、品牌导航、页内目录、搜索及代码复制。样式参考 https://docs.elibot.cn/cs/1ffff/9a93b ，未引入其站点服务或远程样式依赖。

正式手册已移除原始资料版本、重写说明及“原手册”措辞。历史来源和提取记录仅作为仓库维护资料保留；原有章节、图号及文档版本保持不变。
