# Gazebo：物理仿真

Gazebo 可以模拟机器人运动与物理行为，也可通过添加障碍物测试运动规划、碰撞检测和避障算法。

```{note}
按原手册要求，启动 Gazebo 仿真前应关闭其他机器人端连接。该流程不需要连接实体机器人或提前启动 ELIBOTSim。
```

以下两种方式分别用于脚本控制和 MoveIt 2 交互控制，按需要选择其一。

## 使用程序控制 Gazebo 机器人

在已加载 ROS 2 与工作空间环境的终端中启动仿真：

```bash
ros2 launch eli_cs_robot_simulation_gz cs_sim_control.launch.py
```

Gazebo 应加载机器人模型。

```{admonition} 图片占位 · 原图 4-11：Gazebo 启动结果
:class: figure-placeholder
待补充 Gazebo 场景中的机器人模型。
建议文件名：`images/fig-4-11-gazebo.png`。
```

另开已加载环境的终端，运行控制示例：

```bash
ros2 run eli_cs_robot_simulation_gz gz_control.py --example
```

更多程序控制方式可参考[原手册引用的脚本源码](https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver/blob/main/eli_cs_robot_simulation_gz/scripts/gz_control.py)。

## 使用 MoveIt 2 控制 Gazebo 机器人

启动 MoveIt 2 与 Gazebo 的组合场景：

```bash
ros2 launch eli_cs_robot_simulation_gz cs_sim_moveit.launch.py
```

在 RViz 中设置目标位置，然后使用 **Plan** 或 **Plan & Execute**，操作方式与 [MoveIt 2 章节](moveit.md)相同。此时执行对象是 Gazebo 中的仿真机器人。
