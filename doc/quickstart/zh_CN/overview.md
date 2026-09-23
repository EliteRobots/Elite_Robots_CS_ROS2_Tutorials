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

## 软件包结构

以下名称沿用原手册的软件包结构。

```{admonition} 图片占位 · 原图 1-1：ELITE ROS 2 软件包结构
:class: figure-placeholder
待补充软件包关系图。建议文件名：`images/fig-1-1-package-structure.png`。
```

| 软件包 | 用途 |
| --- | --- |
| `eli_common_interface` | 共用的服务与消息接口 |
| `eli_dashboard_interface` | Dashboard 节点使用的接口 |
| `eli_cs_controllers` | 机器人控制器实现 |
| `eli_cs_robot_calibration` | 从实体机器人读取标定数据 |
| `eli_cs_robot_description` | 机器人描述文件和模型 |
| `eli_cs_robot_driver` | 通信、硬件接口、驱动与示例 |
| `eli_cs_robot_simulation_gz` | Gazebo 仿真配置与示例 |
| `eli_cs_robot_moveit_config` | MoveIt 2 配置与示例 |

## 支持的平台与硬件要求

原手册的适用范围为 **CS、ES 系列全部机型及 LS65**；正式测试和支持的平台为 **Ubuntu 22.04（Jammy Jellyfish）+ ROS 2 Humble**。

| 组件 | 原手册建议 |
| --- | --- |
| CPU | 64 位 Intel i5 / i7 或同等 AMD 处理器，推荐多核 |
| 内存 | 至少 8 GB，推荐 16 GB |
| 存储 | 至少 30 GB 可用空间，建议 SSD |
| GPU | 可选；支持 CUDA 的 NVIDIA GPU 可用于需要加速的感知应用 |

MoveIt 2 规划和 RViz 可视化需要一定内存。GPU 不是本手册基础控制流程的必需条件。

## 常用 ROS 2 命令

以下命令中的包名、节点名、接口类型及路径均需替换为实际值。

### 工作空间与节点

```bash
# 构建工作空间并加载环境
cd ~/elite_ros_ws
colcon build
source install/setup.bash

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

在启动程序的终端按 `Ctrl+C` 可停止该前台程序。原手册中的 `ros2 node kill` 不是 ROS 2 Humble 的标准命令；`roslaunch` 属于 ROS 1，ROS 2 应使用 `ros2 launch`。

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
