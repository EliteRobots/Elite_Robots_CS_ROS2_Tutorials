# MoveIt 2: Planning and execution

This chapter uses a **CS66** to plan and execute robot motion in RViz with MoveIt 2.

## Prepare the robot

Complete [Local environment setup](installation.md), connect a physical robot or start ELIBOTSim, and configure remote control and bidirectional network communication.

## Start the driver

In a terminal with ROS 2 and the workspace environment sourced, run:

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=<robot_ip> \
  headless_mode:=true \
  launch_rviz:=false \
  cs_type:=cs66
```

Replace `<robot_ip>` with the reachable IP address of the physical robot or ELIBOTSim container. The driver's own RViz instance is disabled here; you will use the interface launched by MoveIt 2.

After starting the driver, follow [Getting started with the driver](driver.md) to power on, release the brakes, and start the external control script. Confirm that the task status is `PLAYING` and the trajectory controller is `active`.

## Start MoveIt 2

Open another terminal, source the environment, and run:

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py cs_type:=cs66
```

Confirm that the robot pose in RViz matches the teach pendant. If it does not, first check the model, `/joint_states`, and driver connection status. Physical robots and ELIBOTSim use the default `use_sim_time:=false`; see the next chapter for Gazebo configuration.

## Plan and execute

1. Drag the interactive marker at the robot's end effector in RViz to set the target pose.
2. Click **Plan** to generate and inspect a planned trajectory.
3. When you are ready to move the robot, click **Plan & Execute** to plan and execute the motion.

```{warning}
Plan & Execute moves the robot. Make sure the robot's surroundings are safe before executing.
```

```{figure} images/fig-5-1-moveit-planning.png
:name: fig-5-1-moveit-planning
:alt: Generated trajectory
:width: 90%
:align: center

Generated trajectory
```

During execution, the robot state shown on the teach pendant should reflect the motion.
