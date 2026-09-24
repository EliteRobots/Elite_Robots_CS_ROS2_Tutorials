# CS、ES、LS 系列 ROS 2 软件包快速使用手册

**艾利特智能机器人股份有限公司**  
文档版本：**1.0.0** · 修订日期：**2026-09-24**

本手册介绍 ELITE ROS 2 软件包的安装与基本使用，带你完成机器人网络配置、开发环境安装、驱动启动，以及 MoveIt 2 运动规划和 Gazebo 物理仿真。

(适用版本)=
```{rubric} 适用版本
```

本手册 **1.0.0** 对应以下软件包版本（记录日期：2026-09-24）。本次进行了源码核对，尚未进行实机运行验证。

```{list-table}
:header-rows: 1
:widths: 75 25

* - ROS 软件包
  - 适配版本
* - `elite_robots`
  - `1.2.0`
* - `elite_robots_calibration`
  - `1.2.0`
* - `elite_robots_controllers`
  - `1.2.0`
* - `elite_robots_dashboard_msgs`
  - `1.2.0`
* - `elite_robots_driver`
  - `1.2.0`
* - `elite_robots_moveit_config`
  - `1.2.0`
* - `elite_robots_msgs`
  - `1.2.0`
* - `elite_robots_description`
  - `1.0.0`
* - `elite_cs_series_sdk`
  - `1.4.7`
* - `elite_robots_simulation_gz`
  - `1.0.2`
```

- **ROS 与操作系统**：命令以 Ubuntu 22.04 / ROS 2 Humble 为核对基线；项目声明同时支持 Ubuntu 24.04 / ROS 2 Jazzy，本次未对 Jazzy 分支逐项核对。Gazebo 流程仅适用于 Humble。
- **机器人控制软件**：当前 SDK README 声明最低版本为 2.15.0；这不是本手册已完成的兼容性测试范围。ELIBOTSim 镜像选择参见[机器人端配置](robot_setup.md)。
- **版本关系**：文档版本独立于 ROS 包版本和机器人控制软件版本。后续文档变化见[修订记录](changelog.md)。

(阅读说明)=
```{rubric} 阅读说明
```

使用前请核对机器人型号、控制软件版本、ROS 软件包版本和开发环境。软件源中的二进制包可能与上述源码版本不同，请以实际安装版本为准。

建议按以下顺序操作：

1. 阅读[概述](overview.md)，确认支持的平台及软件包组成。
2. 在[机器人端配置](robot_setup.md)中，选择实体机器人或 ELIBOTSim 虚拟示教器，并完成连接测试。
3. 按[本地环境安装](installation.md)准备开发环境并编译驱动。
4. 按[驱动入门](driver.md)启动机器人并尝试基本服务与轨迹控制。
5. 按需要尝试 [MoveIt 2](moveit.md) 或 [Gazebo](gazebo.md)。Gazebo 物理仿真不需要连接实体机器人或启动 ELIBOTSim。

文中 `<robot_ip>`、`<local_ip>`、`<cs_type>` 等表示需要替换的参数，不应连同尖括号直接执行。多终端操作时，每个终端都应加载 ROS 2 和工作空间环境。

```{warning}
执行运动示例前，应确认机器人状态满足要求，并确保机器人周围环境安全。文中的关节位置仅为操作示例，应结合实际工作空间确认后使用。
```

**使用与版权说明**

安装、使用产品前请阅读本手册，并保留以供后续查阅。手册内容会随版本更新，图片仅供参考，应以实际产品为准。

内容或信息如有变更，恕不另行通知；艾利特智能机器人股份有限公司对手册中可能存在的错误，以及因使用本手册及其中所述产品引起的意外或间接伤害概不负责。

Copyright © 2026 ELITE ROBOTS. 保留所有权利。

```{toctree}
:maxdepth: 3
:numbered:
:caption: 目录

overview
robot_setup
installation
driver
moveit
gazebo
support
changelog
```
