# MoveIt 2：规划与执行

本章以 **CS66** 为例，通过 MoveIt 2 在 RViz 中规划并执行机器人运动。

## 准备机器人

完成[本地环境安装](installation.md)，连接实体机器人或启动 ELIBOTSim，并完成远程控制与双向网络配置。

## 启动驱动

在已加载 ROS 2 和工作空间环境的终端中执行：

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=<robot_ip> \
  headless_mode:=true \
  launch_rviz:=false \
  cs_type:=cs66
```

将 `<robot_ip>` 替换为实体机器人或 ELIBOTSim 容器的可达 IP。这里关闭驱动自带的 RViz，随后使用 MoveIt 2 启动的界面。

驱动启动后，按[驱动入门](driver.md)完成上电、释放抱闸、启动外部控制脚本，并确认任务状态为 `PLAYING`、轨迹控制器为 `active`。

## 启动 MoveIt 2

另开终端并加载环境，然后执行：

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py cs_type:=cs66
```

确认 RViz 中的机器人姿态与示教器一致。如不一致，先核对型号、`/joint_states` 和驱动连接状态。实体机器人及 ELIBOTSim 使用默认的 `use_sim_time:=false`；Gazebo 的配置见下一章。

## 规划并执行

1. 在 RViz 中拖动机器人末端执行器的交互标记，设置目标位置。
2. 点击 **Plan**，生成并查看规划轨迹。
3. 需要实际运动时，点击 **Plan & Execute**，完成规划与执行。

```{warning}
Plan & Execute 会执行机器人运动。执行前确认机器人周围环境安全。
```

```{figure} images/fig-5-1-moveit-planning.png
:name: fig-5-1-moveit-planning
:alt: 生成轨迹
:width: 90%
:align: center

生成轨迹
```

执行时，示教器中的机器人状态应同步显示运动过程。
