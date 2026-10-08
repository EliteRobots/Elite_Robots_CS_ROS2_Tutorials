# Elite Robots ROS 2 接口手册

**艾利特智能机器人股份有限公司**  
文档版本：**1.0.0** · 修订日期：**2026-09-24** · 中文

本手册面向使用 ROS 2 接入机器人、开发应用和集成控制系统的开发者，说明机器人描述、驱动、控制器、MoveIt 2 与 Gazebo 的启动接口、参数、话题、服务和动作。

```{rubric} 适用范围
```

接口基线为 Humble 分支：`elite_robots_description` **1.0.0**、Driver 仓库七个 ROS 包 **1.0.3**、`elite_robots_simulation_gz` **1.0.1**。本文记录这些版本的实际接口行为，不能直接套用其他版本的默认值或启动文件名。文档版本独立于软件包版本。

本版已完成源码核对和文档构建检查，尚未进行实体机器人、ELIBOTSim 或 Gazebo 运行验证。ROS 自带控制器与 MoveIt 的接口还受实际安装的依赖版本影响；部署时应按[接口自检](examples.md)确认。

```{rubric} 阅读路径
```

- 查找某个功能：从[软件包与接口约定](overview.md)进入对应章节。
- 编写客户端：先阅读[控制器接口](controllers.md)、[机器人管理接口](dashboard.md)和[消息与服务类型](messages.md)。
- 集成启动文件：查阅[启动参数索引](launch_reference.md)，区分 launch 参数、节点参数与硬件参数。
- 接入仿真：阅读 [Gazebo 接口](gazebo.md)，使用该版本可用的分步启动方式。

```{toctree}
:maxdepth: 3
:numbered:
:caption: 目录

overview
description
driver
controllers
dashboard
messages
moveit
gazebo
examples
launch_reference
changelog
```
