# 概述

ROS（Robot Operating System，机器人操作系统）是一组用于开发机器人应用的软件库和工具。ROS 2 在通信机制、实时性等方面扩展了 ROS 1 的能力。

ROS 2 程序通常按软件包（package）组织，在工作空间（workspace）中使用 `colcon` 构建。软件包中的节点（node）通过不同通信机制协作：

| 通信方式 | 本软件包中的用途 |
| --- | --- |
| 话题（Topic） | 持续发布机器人状态，或发送控制消息 |
| 服务（Service） | 执行上电、状态查询等请求与响应操作 |
| 动作（Action） | 执行轨迹等需要持续运行、反馈和结果的任务 |

## 主要功能

- **机器人驱动与控制接口**：向机器人控制器发送指令并接收状态反馈。
- **自定义控制器**：提供适配 ELITE 机器人的控制器。
- **MoveIt 2 集成**：支持运动规划、运动学求解、碰撞检测与轨迹执行。
- **RViz 可视化**：显示机器人模型、关节状态和规划结果，辅助预览运动与交互控制。
- **Gazebo 物理仿真**：在仿真环境中测试机器人运动、控制程序及场景交互。

## 软件包列表

```{list-table}
:header-rows: 1
:widths: 52 48

* - 软件包
  - 用途
* - `elite_robots`
  - 提供一个统一安装入口的元软件包，用于安装 Elite Robots 的 ROS 2 软件包。
* - `elite_robots_msgs`
  - 机器人状态、IO 及服务等自定义消息接口。
* - `elite_robots_dashboard_msgs`
  - Dashboard 相关消息与服务接口；部分 Dashboard 服务使用 `elite_robots_msgs`
* - `elite_robots_controllers`
  - 机器人控制器实现
* - `elite_robots_calibration`
  - 从实体机器人读取标定数据
* - `elite_robots_description`
  - 机器人描述文件和模型
* - `elite_robots_driver`
  - 通信、硬件接口、驱动与示例
* - `elite_cs_series_sdk`
  - 驱动依赖的机器人 C++ 通信 SDK
* - `elite_robots_simulation_gz`
  - Gazebo 仿真配置与示例（仅限 Humble）
* - `elite_robots_moveit_config`
  - MoveIt 2 配置与示例
```

## 支持的平台与硬件要求

支持的机器人型号：
- CS系列：CS63, CS63a, CS66, CS68, CS612, CS616, CS618F, CS620, CS625, CS630, CS66A, CS520H
- ES系列：ES63, ES63a, ES66, ES68, ES612, ES616, ES618F, ES620, ES625, ES630, ES66A, ES520H
- LS系列：LS65

正式测试和支持的平台:
- **Ubuntu 22.04 (Jammy Jellyfish)+ ROS 2 Humble**
- **Ubuntu 24.04 (Noble Numbat)+ ROS 2 Jazzy**

本手册命令以 Humble 为例。Jazzy 环境应使用对应发行版的软件包与源码分支，不要混用 Humble 的安装命令。

`cs_type` 是启动文件接受的配置名称，当前驱动和描述包允许：`cs63`、`cs63a`、`cs66`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs630`、`cs66a`、`cs520h`、`ls65`。名称区分大小写；当前启动文件没有 `es66` 等 `es*` 选项，ES 系列请先确认对应的型号配置。Gazebo 支持的选项以其启动文件为准。

MoveIt 2 规划和 RViz 可视化需要一定内存。GPU 不是本手册基础控制流程的必需条件。

## 常用 ROS 2 命令

以下命令中的包名、节点名、接口类型及路径均需替换为实际值。

### 节点

```bash
# 查询软件包及安装路径
ros2 pkg list
ros2 pkg prefix <package_name>

# 启动程序或 launch 文件
ros2 run <package_name> <executable_name>
ros2 launch <package_name> <file.launch.py>

# 查看节点
ros2 node list
ros2 node info <node_name>
```

在启动程序的终端按 `Ctrl+C` 可停止该前台程序。

### 话题与接口

```bash
ros2 topic --help
ros2 topic list
ros2 topic echo /<topic_name>
ros2 topic info /<topic_name>
ros2 topic type /<topic_name>
ros2 interface show <interface_type>
```

`topic type` 返回接口类型名称；查看消息字段时使用 `interface show`。

### 服务、参数与数据记录

```bash
ros2 service --help
ros2 service list
ros2 service call <service_name> <service_type> '<arguments>'

ros2 param list
ros2 param get <node_name> <param_name>
ros2 param set <node_name> <param_name> <value>

ros2 bag record /<topic_name>
ros2 bag play <bag_path>
```

### 控制器与硬件接口

```bash
ros2 control list_controllers
ros2 control list_controller_types
ros2 control list_hardware_components
ros2 control list_hardware_interfaces
```

这些命令分别用于查看控制器及状态、可用控制器类型、已注册硬件组件，以及 position、velocity 等硬件接口。
