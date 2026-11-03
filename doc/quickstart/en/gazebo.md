# Gazebo: Physics simulation

Gazebo simulates robot motion and physical behavior. You can also add obstacles to test motion planning, collision detection, and obstacle avoidance algorithms.

```{note}
1. The current simulation package supports ROS 2 Humble only.
2. This procedure does not require a physical robot or a running ELIBOTSim instance.
3. Install or build `elite_robots_simulation_gz` before proceeding.
4. This chapter uses a CS66 with the default joint names and `joint_trajectory_controller`. The `gz_control.py` example uses six joints and cannot be used unchanged with a five-axis configuration.
```

The two workflows below provide script-based control and interactive MoveIt 2 control. Choose the one you need.

## Control the Gazebo robot programmatically

An apt installation only requires the ROS 2 environment; a source installation also requires the corresponding workspace. If you added the required `source` commands to `~/.bashrc` as described in the installation chapter, new Bash terminals load them automatically, so you do not need to run them again. If it is not loaded, see {ref}`Terminal environment setup <terminal-environment>`. Once the environment is ready, start the simulation:

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py cs_type:=cs66
```

Gazebo should load the robot model.

```{figure} images/fig-6-1-gazebo.png
:name: fig-6-1-gazebo
:alt: Gazebo startup result
:width: 90%
:align: center

Gazebo startup result
```

Open another terminal with the environment loaded as described above, then run the control example:

```bash
ros2 run elite_robots_simulation_gz gz_control.py --example
```

For other programmatic control options, see the [script source](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_GZ_Simulation/blob/humble/scripts/gz_control.py).

## Control the Gazebo robot with MoveIt 2

The following steps start Gazebo and MoveIt 2 separately. Check that each terminal has the environment for your installation method as described above. If `.bashrc` loaded it automatically, you do not need to run `source` again. If the simulation from the previous section is still running, stop it before switching to this workflow.

**Terminal 1: Start Gazebo without its bundled RViz instance.**

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py \
  cs_type:=cs66 launch_rviz:=false
```

**Terminal 2: Check the simulation clock.**

```bash
ros2 topic echo /clock --once
```

You should receive increasing timestamps while Gazebo runs. If no `/clock` messages arrive, press `Ctrl+C` to stop waiting, install and start the bridge, and leave this terminal running:

```bash
sudo apt install ros-humble-ros-gz-bridge
ros2 run ros_gz_bridge parameter_bridge \
  '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
```

This is a one-way bridge from Gazebo to ROS; see the [ros_gz_bridge documentation](https://github.com/gazebosim/ros_gz/blob/humble/ros_gz_bridge/README.md). Do not start a duplicate bridge if a clock publisher is already present.

**Terminal 3: Start MoveIt 2.**

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 use_sim_time:=true use_fake_hardware:=true
```

In the current `elite_moveit.launch.py`, `use_fake_hardware:=true` selects the standard `joint_trajectory_controller`, matching Gazebo's default controller. This MoveIt launch file does not itself start fake hardware. `use_sim_time:=true` makes MoveIt and RViz use the Gazebo clock.

Set a target pose in RViz and use **Plan** or **Plan & Execute**, as described in the [MoveIt 2 chapter](moveit.md). In this workflow, motion is executed by the simulated robot in Gazebo.
