# 准备与隔离原则

## 方案范围

双臂驱动模板两次包含 `elite_robots_driver/launch/elite_control.launch.py`，为每台机械臂启动独立控制器管理器。可选 MoveIt 模板两次包含 `elite_moveit.launch.py`，各自规划并执行本机械臂的轨迹。

此方案不创建包含两台机械臂的统一机器人模型、联合规划组或同步执行器。两套独立规划场景不会自动感知另一台机械臂；namespace 和前缀也不会自动设置两台机械臂在工作区中的实际安装位置。共享工作空间内的协同运动需要另外建立一致的基座变换、完整碰撞模型及执行协调机制。

## 每台机械臂需要隔离的内容

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - 项目
  - arm1
  - arm2
* - ROS namespace
  - `arm1`
  - `arm2`
* - 关节/TF 前缀
  - `arm1_`
  - `arm2_`
* - 控制器管理器
  - `/arm1/controller_manager`
  - `/arm2/controller_manager`
* - 默认控制器 IP
  - `192.168.1.101`
  - `192.168.1.102`
* - 默认型号
  - `cs63`
  - `cs63`
* - MoveIt 规划组
  - `arm1_cs_manipulator`
  - `arm2_cs_manipulator`
```

ROS namespace 隔离节点、服务、话题和动作；前缀隔离关节、连杆及硬件资源标识。两者需要同时配置。名称前缀不等同于空间变换；默认模型中的共同 `world` 根也不代表已经标定了两臂相对位置。

同一 ROS 计算机上的机器人通信端口也必须避免冲突。四类端口依次为 reverse、script sender、trajectory、script command：arm1 默认使用 50001～50004，arm2 默认使用 50101～50104。

## 环境与文件

先编译工作空间并加载环境：

```bash
cd ~/elite_ros_ws
source /opt/ros/humble/setup.bash
colcon build --packages-up-to elite_robots_driver elite_robots_moveit_config
source install/setup.bash
mkdir -p ~/dual_arm_launch
cd ~/dual_arm_launch
```

`~/elite_ros_ws` 是示例工作空间，按实际位置替换。每个新终端都要重新 source ROS 和工作空间环境。将后续章节的完整代码保存为：

```text
~/dual_arm_launch/
├── dual_arm_control.launch.py
└── dual_moveit.launch.py
```

也可通过章节中的下载链接保存同名文件。下载链接与正文代码引用同一份文件，避免手工复制遗漏。

安装版本检查（只显示参数，不启动机器人）：

```bash
ros2 launch elite_robots_driver elite_control.launch.py --show-args
ros2 launch elite_robots_moveit_config elite_moveit.launch.py --show-args
```

驱动入口必须支持命名空间内的配置键、控制器配置绝对路径、指定管理器和关闭内部 spawner。MoveIt 入口必须支持自定义配置绝对路径，并将 prefix 同时传给 URDF 的 tf_prefix 与 SRDF。若缺少这些能力，应先更新相应源码和安装环境，不能只复制包装模板。

## 场景区别

- 实体机器人：两台控制器地址均应可达，并能回连 ROS 计算机；无头模式下按机器人配置启用远程控制。
- ELIBOTSim：使用两个独立模拟控制器的可达地址，并满足相同的回连及端口条件；不要把两台机械臂都指向同一个控制器实例。
- fake hardware：不连接机器人，用于关节与命名空间集成；它不是完整控制柜模拟器。

本方案使用系统时间，不是 Gazebo 流程，不需要 Gazebo `/clock` 桥。`local_ip` 未由双臂包装模板单独暴露，沿用单臂入口的自动选择行为；多网卡环境若需为每臂指定回连地址，应在自定义包装文件中添加并传递对应参数。
