# Gazebo simulation interfaces

## Standalone control entry point

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py \
  cs_type:=cs66 initial_joint_controller:=joint_trajectory_controller \
  launch_rviz:=false
```

This version starts the empty world `empty.sdf`, spawns entity `cs`, and sets Description's `sim_ignition=true` to select `ign_ros2_control/IgnitionSystem`. `robot_state_publisher` uses simulation time. By default, `joint_state_broadcaster` and the standard `joint_trajectory_controller` are loaded.

Gazebo interfaces do not pass through the robot controller and provide no `/dashboard_client/*`, `/primary_client/*`, or physical GPIO services. A name appearing in controller YAML does not mean that plugin has been loaded.

## Controllers and time

The simulation `controller_manager` update rate is configured as **500 Hz**. The default trajectory action is `/joint_trajectory_controller/follow_joint_trajectory`, with the same type as the physical driver. Default per-joint path tolerance is **0.2 rad**, goal tolerance **0.1 rad**, stopped velocity tolerance **0.2 rad/s**, and `goal_time=0.0`.

ROS `/clock` uses `rosgraph_msgs/msg/Clock`. This launch version does not start a clock bridge. First check for a publisher and actual data:

```bash
ros2 topic info /clock
ros2 topic echo /clock --once
```

If there is no data, start a one-way bridge for the Humble/Ignition environment in a separate terminal:

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
```

Other Gazebo/ros_gz versions may use the type name `gz.msgs.Clock` or a world-scoped clock topic. Confirm the installed version and actual simulation topic, then adjust the mapping. If the clock remains at zero or is paused, planning, TF, and actions using simulation time may wait or time out. Avoid creating duplicate bridges for the same clock.

## Combining with MoveIt in separate steps

Once Gazebo control is running and clock and joint state data are confirmed, open another terminal:

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 use_sim_time:=true use_fake_hardware:=true \
  launch_servo:=false
```

Here, `use_fake_hardware=true` selects the standard trajectory controller; Gazebo remains the source of motion simulation. If using RViz, set its time source after startup:

```bash
ros2 param set /rviz2_moveit use_sim_time true
```

This version also provides `elite_sim_moveit.launch.py`, but it references `cs_moveit.launch.py`, which does not exist in the accompanying MoveIt package. The actual filename is `elite_moveit.launch.py`. This manual therefore does not present that combined entry point as a directly usable procedure. Its declared arguments remain in the [Launch argument reference](launch_reference.md) to support migration or maintenance of existing calls.

## Initial positions, five-axis models, and prefixes

`cs_type` defaults to `cs66`. When `initial_positions_file` is empty, ordinary models use `initial_positions.yaml`, models ending in `a` use `initial_positions_a_type.yaml`, and models ending in `h` use `initial_positions_h_type.yaml`. To override, supply a YAML file path.

Five-axis models default to `urdf_5f` and `cs_controllers_5f.yaml` and require trajectories containing five joints. Six-axis example scripts are not applicable.

This launch passes `prefix` to Xacro, but the model entry point expects `tf_prefix`, and the controller YAML uses fixed joint names. Examples in this manual assume the default empty prefix. Multiple robots require consistent custom models, controllers, and namespaces.

## gz_control.py client

The installed executable is **`gz_control.py`**, and its node name is `sdk_gz_bridge`. CMake does not rename the script to `gz_control`.

```bash
ros2 run elite_robots_simulation_gz gz_control.py --help
```

The CLI uses argparse, not ROS `-p` parameters:

```{list-table}
:header-rows: 1
:widths: 40 60

* - Argument
  - Meaning
* - `--controller NAME`
  - Default `joint_trajectory_controller`; forms the absolute action name `/<NAME>/follow_joint_trajectory`.
* - `--example`
  - Sends the built-in six-axis trajectory, immediately causing simulated motion.
* - `--from-yaml PATH`
  - Reads a waypoint file; takes precedence if both this option and example are supplied.
```

YAML must be a list. Each `positions` entry contains 6 values in rad; `duration` is that segment's duration in s, defaulting to 3.0 when omitted. The program accumulates segment durations to obtain `time_from_start`. Applications must ensure positive segment durations; the script does not fully validate every aspect of trajectory validity.

The following illustrates the data format only. Replace positions with verified targets:

```yaml
- positions: [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]
  duration: 3.0
- positions: [0.1, -1.57, 0.0, -1.57, 0.0, 0.0]
  duration: 2.0
```

Send to the simulation controller:

```bash
ros2 run elite_robots_simulation_gz gz_control.py \
  --from-yaml /tmp/waypoints.yaml
```

The script waits up to 10 s for the action server, then waits for goal acceptance and the execution result. Exit code 0 indicates result `error_code=0`; 1 indicates an argument or file parsing error; 2 indicates a sending/execution failure. Joint names are fixed to six axes without prefixes. The script does not explicitly configure simulation time or provide cancellation, five-axis, or multiple-robot naming options. More complex applications should implement their own action clients.

## Non-default configuration limitations

Simulation YAML still refers to `cs_controllers/...` plugin names for IO, speed scaling, force broadcasting, and scaled trajectories, which differ from the plugins exported by Driver. Only joint state broadcasting and standard trajectory control start by default. Do not directly activate these legacy entries. Renaming them alone would not give the simulation system physical hardware resources such as GPIO or speed scaling.
