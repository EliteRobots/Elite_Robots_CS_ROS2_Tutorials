# MoveIt 2：规划与执行

本章以 **CS66** 为例，通过 MoveIt 2 在 RViz 中规划并执行机器人运动。

## 准备机器人

完成[本地环境安装](installation.md)，连接实体机器人或启动 ELIBOTSim，并确保示教器中的机器人处于正常模式。

## 启动驱动

在已加载 ROS 2 和工作空间环境的终端中执行：

```bash
ros2 launch eli_cs_robot_driver elite_control.launch.py \
  robot_ip:=<robot_ip> \
  headless_mode:=true \
  launch_rviz:=false \
  cs_type:=cs66
```

将 `<robot_ip>` 替换为实体机器人 IP；原手册的虚拟示教器场景使用本地计算机 IP。这里关闭驱动自带的 RViz，随后使用 MoveIt 2 启动的界面。

## 启动 MoveIt 2

另开终端并加载环境，然后执行：

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
ros2 launch eli_cs_robot_moveit_config cs_moveit.launch.py cs_type:=cs66
```

确认 RViz 中的机器人姿态与示教器一致。原手册建议：如不一致，可重启机器人驱动与 MoveIt 2 节点。

## 规划并执行

1. 在 RViz 中拖动机器人末端执行器的交互标记，设置目标位置。
2. 点击 **Plan**，生成并查看规划轨迹。
3. 需要实际运动时，点击 **Plan & Execute**，完成规划与执行。

```{warning}
Plan & Execute 会执行机器人运动。执行前确认机器人周围环境安全。
```

```{admonition} 图片占位 · 原图 4-10：生成轨迹
:class: figure-placeholder
待补充 RViz 的交互标记与规划按钮截图。
建议文件名：`images/fig-4-10-moveit-planning.png`。
```

执行时，示教器中的机器人状态应同步显示运动过程。

原手册进一步参考：[ELITE Robots ROS 2 教程](https://github.com/Elite-Robots/Elite_Robots_CS_Ros2_Tutorials/blob/main/tutorials/Elite%20Robots%20ROS2%20%E6%95%99%E7%A8%8B.md)。独立 usage 手册将在后续补充，本章仅覆盖快速入门。
