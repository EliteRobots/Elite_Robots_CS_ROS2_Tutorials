# MoveIt 2 and Servo interfaces

## Launch entry point and responsibilities

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 launch_servo:=false
```

This entry point starts `move_group`, optional RViz, and optional Servo. It does not start the physical driver, Gazebo, or a ros2_control manager. Before executing trajectories, start the selected driver separately and ensure `/joint_states`, TF, and the target action server are ready.

The default planning group is `cs_manipulator`, with an SRDF chain from `base_link` to `tool0`. Five-axis models select the corresponding SRDF and limit files. Planning uses OMPL, and robot kinematics configuration comes from `kinematics.yaml`.

## Trajectory execution mapping

The default `controllers.yaml` lists two `FollowJointTrajectory` controllers, both with `action_ns` set to `follow_joint_trajectory`:

- `scaled_joint_trajectory_controller`: selected by default (`true`); targets the trajectory action under the controller of the same name.
- `joint_trajectory_controller`: not selected by default (`false`); targets the trajectory action under the controller of the same name.

In this entry point, `use_fake_hardware:=true` only switches the default execution controller to the standard `joint_trajectory_controller`; it does not create fake hardware. This option can also select the correct action target when Gazebo uses the standard controller.

With `moveit_manage_controllers=false`, MoveIt does not load or switch controllers. Default trajectory execution settings are 1.2 allowed duration scaling, 0.5 s additional time margin, and 0.01 rad start position tolerance. Successful planning does not imply executable motion: controller names, joint names, and runtime state must match.

## Standard MoveIt ROS interfaces

This package configures standard MoveIt nodes and defines no new planning messages. The following interfaces are commonly provided by the default capabilities. Check actual availability with `ros2 node info /move_group`, `ros2 action list -t`, and `ros2 service list -t`.

- `/move_action`: `moveit_msgs/action/MoveGroup`; accepts a motion planning request and planning options, and returns a trajectory and error code.
- `/execute_trajectory`: `moveit_msgs/action/ExecuteTrajectory`; executes an existing RobotTrajectory and returns an execution error code.
- `/plan_kinematic_path`: `moveit_msgs/srv/GetMotionPlan`; computes a motion plan only.
- `/compute_ik`: `moveit_msgs/srv/GetPositionIK`; inverse kinematics.
- `/compute_fk`: `moveit_msgs/srv/GetPositionFK`; forward kinematics.
- `/compute_cartesian_path`: `moveit_msgs/srv/GetCartesianPath`; Cartesian path generation. Check both the returned completion fraction and error code.
- `/get_planning_scene`: `moveit_msgs/srv/GetPlanningScene`; retrieves the scene.
- `/apply_planning_scene`: `moveit_msgs/srv/ApplyPlanningScene`; updates the scene.

MoveIt actions use `moveit_msgs/msg/MoveItErrorCodes`, a different error code system from the underlying `FollowJointTrajectory.error_code`. Parse each separately; the same integer does not necessarily have the same meaning across interfaces.

Scene input/output uses `moveit_msgs/msg/PlanningScene`, and trajectory display uses `moveit_msgs/msg/DisplayTrajectory`. Topic names depend on the enabled capabilities and namespace. Robot description publication is controlled by `publish_robot_description` and `publish_robot_description_semantic`, both true by default.

## Servo configuration interfaces

`launch_servo` defaults to true; disable it explicitly if real-time Servo is not needed. Configuration is in `config/cs_servo.yaml`, passed under the node's `moveit_servo` parameter namespace.

```{list-table}
:header-rows: 1
:widths: 54 46

* - Setting
  - Default and meaning
* - `command_in_type`
  - `speed_units`; input uses physical velocity units.
* - `cartesian_command_in_topic`
  - `~/delta_twist_cmds`, `geometry_msgs/msg/TwistStamped`; linear velocity in m/s, angular velocity in rad/s.
* - `joint_command_in_topic`
  - `~/delta_joint_cmds`, `control_msgs/msg/JointJog`; joint velocity in rad/s.
* - `joint_topic`
  - `/joint_states`
* - `status_topic`
  - `~/status`; interpret Servo status codes using the installed MoveIt version.
* - `command_out_topic`
  - `/forward_position_controller/commands`
* - `command_out_type`
  - `std_msgs/Float64MultiArray`; publishes positions only.
* - `move_group_name`
  - `cs_manipulator`
* - `planning_frame`
  - `base_link`
* - `ee_frame_name`, `robot_link_command_frame`
  - `tool0`
* - `publish_period`
  - 0.004 s; configured target rate 250 Hz.
* - `incoming_command_timeout`
  - 0.1 s; stops Servo motion output on input timeout.
* - `num_outgoing_halt_msgs_to_publish`
  - 4; repeated halt publications.
* - `check_collisions`, `collision_check_rate`
  - true, 5 Hz.
```

`~/` resolves against the actual Servo node name; do not infer it from the executable name. After startup, inspect the node interfaces and the installed version's start/pause services. Ensure `forward_position_controller` is active and no other controller competes for the joint resources. The default driver only loads it as inactive; starting Servo does not activate it automatically.

Inputs need valid timestamps and frames, and continuous command intervals should be below 0.1 s. Avoid competing input sources. `scale.linear/rotational/joint` applies only in `unitless` mode; the current `speed_units` mode does not use these factors.

## Prefix and simulation clock limitations

This MoveIt launch version passes `prefix` to URDF, while the Description URDF entry point uses `tf_prefix`; SRDF uses `prefix`. The default empty prefix keeps names consistent, but a nonempty prefix may produce mismatches between SRDF and URDF. Controller and Servo YAML also contain fixed names without prefixes. Multiple robots require consistent custom models, configuration, and launch files; setting `prefix` alone is insufficient.

`use_sim_time` is passed only to `move_group`, not to RViz or Servo in this launch file. Simulation integration must ensure all nodes handling timestamps use `/clock`. The example disables Servo and sets simulation time on RViz as needed. `moveit_config_package` does not replace every configuration source: OMPL and Servo YAML are still loaded specifically from `elite_robots_moveit_config`.
