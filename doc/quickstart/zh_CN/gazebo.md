# Gazebo：物理仿真

Gazebo 可以模拟机器人运动与物理行为，也可通过添加障碍物测试运动规划、碰撞检测和避障算法。

```{note}
1. 当前仿真包仅支持 ROS 2 Humble。
2. 该流程不需要连接实体机器人或提前启动 ELIBOTSim。
3. 已安装或编译 `elite_robots_simulation_gz` 包。
4. 本章以 CS66、默认关节名和 `joint_trajectory_controller` 为例；`gz_control.py` 示例使用六个关节，不适用于未经修改的五轴配置。
```

以下两种方式分别用于脚本控制和 MoveIt 2 交互控制，按需要选择其一。

## 使用程序控制 Gazebo 机器人

在已加载 ROS 2 与工作空间环境的终端中启动仿真：

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py cs_type:=cs66
```

Gazebo 应加载机器人模型。

```{figure} images/fig-6-1-gazebo.png
:name: fig-6-1-gazebo
:alt: Gazebo 启动结果
:width: 90%
:align: center

Gazebo 启动结果
```

另开已加载环境的终端，运行控制示例：

```bash
ros2 run elite_robots_simulation_gz gz_control.py --example
```

更多程序控制方式可参考[引用的脚本源码](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_GZ_Simulation/blob/humble/scripts/gz_control.py)。

## 使用 MoveIt 2 控制 Gazebo 机器人

当前工作空间的 `elite_sim_moveit.launch.py` 仍引用旧的 `cs_moveit.launch.py`，与当前 MoveIt 包不匹配。使用以下分步方式启动，每个终端都先加载 ROS 2 和工作空间环境；若前一节仿真仍在运行，先停止它再切换到本流程。

**终端一：启动 Gazebo，关闭其附带的 RViz。**

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py \
  cs_type:=cs66 launch_rviz:=false
```

**终端二：检查仿真时钟。**

```bash
ros2 topic echo /clock --once
```

Gazebo 运行时应收到递增的时间。当前仿真启动文件未显式配置时钟桥接；若没有 `/clock` 消息，按 `Ctrl+C` 退出等待，安装并启动桥接，保持该终端运行：

```bash
sudo apt install ros-humble-ros-gz-bridge
ros2 run ros_gz_bridge parameter_bridge \
  '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
```

这里使用 Gazebo 到 ROS 的单向桥接，见 [ros_gz_bridge 文档](https://github.com/gazebosim/ros_gz/blob/humble/ros_gz_bridge/README.md)。已有时钟发布者时不要重复启动桥接。

**终端三：启动 MoveIt 2。**

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 use_sim_time:=true use_fake_hardware:=true
```

在当前 `elite_moveit.launch.py` 中，`use_fake_hardware:=true` 用于选择标准的 `joint_trajectory_controller`，与 Gazebo 的默认控制器匹配；该 MoveIt 启动文件本身不会启动虚拟硬件。`use_sim_time:=true` 则让 MoveIt 和 RViz 使用 Gazebo 时钟。

在 RViz 中设置目标位置，然后使用 **Plan** 或 **Plan & Execute**，操作方式与 [MoveIt 2 章节](moveit.md)相同。此时执行对象是 Gazebo 中的仿真机器人。
