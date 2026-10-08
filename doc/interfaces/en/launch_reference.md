# Launch argument reference

This chapter lists all launch arguments declared by the entry points in this version. Pass them as `name:=value`; required means there is no default. Empty strings and Boolean strings are parsed further by launch/Xacro and do not imply that corresponding ROS node parameters have the same type. Set arguments at startup; live updates are not guaranteed.

## Model visualization

Entry point: `view_cs.launch.py`.

- `cs_type`: **required**, with no default. Model string; accepted choices are listed for each entry point.
  Choices: `cs63`, `cs63a`, `cs66`, `cs66a`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs630`, `cs520h`, `ls65`.
- `safety_limits`: default `true`. Enables safety limit elements in the model.
- `safety_pos_margin`: default `0.15`. Joint safety position margin, in rad.
- `safety_k_position`: default `20`. Safety limit position coefficient.
- `description_package`: default `elite_robots_description`. Package providing the robot description.
- `description_file`: default `cs.urdf.xacro`. Model Xacro filename.
- `tf_prefix`: default empty string. Prefix for joint, link, and hardware resource names.

## Driver control

Entry point: `elite_control.launch.py`.

- `cs_type`: **required**, with no default. Model string; accepted choices are listed for each entry point.
  Choices: `cs63`, `cs66`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs66a`, `cs520h`, `ls65`.
- `robot_ip`: **required**, with no default. Address of the physical robot or ELIBOTSim controller.
- `local_ip`: default `0.0.0.0`. ROS computer address reachable by the controller for reverse connections.
- `safety_limits`: default `true`. Enables safety limit elements in the model.
- `safety_pos_margin`: default `0.15`. Joint safety position margin, in rad.
- `safety_k_position`: default `20`. Safety limit position coefficient.
- `runtime_config_package`: default `elite_robots_driver`. Controller configuration package providing the config directory.
- `controllers_file`: default `elite_cs_controllers.yaml`. Controller YAML filename in that package's config directory.
- `description_package`: default `elite_robots_description`. Package providing the robot description.
- `description_file`: default `cs.urdf.xacro`. Model Xacro filename.
- `tf_prefix`: default empty string. Prefix for joint, link, and hardware resource names.
- `use_fake_hardware`: default `false`. Selects GenericSystem in the driver entry point; only switches the default trajectory controller in the MoveIt entry point.
- `fake_sensor_commands`: default `false`. Enables sensor command interfaces for fake hardware.
- `headless_mode`: default `false`. Sends the external control script directly.
- `controller_spawner_timeout`: default `10`. Timeout waiting for the controller manager, in s.
- `initial_joint_controller`: default `scaled_joint_trajectory_controller`. Name of the joint controller to load initially.
- `activate_joint_controller`: default `true`. Whether the driver entry point activates the initial joint controller.
- `launch_rviz`: default `true`. Whether to start RViz.
- `tool_voltage`: default `0`. Initial tool voltage passed into the model; not applied during initialization in this version.
- `script_command_port`: default `50004`. Script command port on the ROS computer.
- `reverse_port`: default `50001`. Cyclic control port on the ROS computer.
- `script_sender_port`: default `50002`. ExternalControl script server port.
- `trajectory_port`: default `50003`. Trajectory port on the ROS computer.

## MoveIt

Entry point: `elite_moveit.launch.py`.

- `cs_type`: **required**, with no default. Model string; accepted choices are listed for each entry point.
  Choices: `cs63`, `cs66`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs66a`, `cs520h`, `ls65`.
- `use_fake_hardware`: default `false`. Selects GenericSystem in the driver entry point; only switches the default trajectory controller in the MoveIt entry point.
- `safety_limits`: default `true`. Enables safety limit elements in the model.
- `safety_pos_margin`: default `0.15`. Joint safety position margin, in rad.
- `safety_k_position`: default `20`. Safety limit position coefficient.
- `description_package`: default `elite_robots_description`. Package providing the robot description.
- `description_file`: default `cs.urdf.xacro`. Model Xacro filename.
- `moveit_config_package`: default `elite_robots_moveit_config`. Package providing SRDF, joint limits, and controller files; some other YAML files still come from the default package.
- `moveit_config_file`: default `cs.srdf.xacro`. SRDF Xacro filename.
- `moveit_joint_limits_file`: default `joint_limits.yaml`. MoveIt joint limits YAML filename.
- `moveit_controllers_file`: default `controllers.yaml`. MoveIt action controller mapping YAML filename.
- `warehouse_sqlite_path`: default `~/.ros/warehouse_ros.sqlite` (expanded for the current user). MoveIt warehouse SQLite file path.
- `use_sim_time`: default `false`. Whether move_group uses /clock; this version does not also pass the setting to Servo and RViz.
- `prefix`: default empty string. Prefix passed to the downstream model/SRDF; this version has inconsistent forwarding, as described in the MoveIt/Gazebo chapters.
- `launch_rviz`: default `true`. Whether to start RViz.
- `launch_servo`: default `true`. Whether to start the MoveIt Servo node.
- `publish_robot_description`: default `true`. Whether MoveIt publishes the robot description.
- `publish_robot_description_semantic`: default `true`. Whether MoveIt publishes the semantic description.

## Gazebo control

Entry point: `elite_sim_control.launch.py`.

- `cs_type`: default `cs66`. Model string; accepted choices are listed for each entry point.
  Choices: `cs63`, `cs66`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs66a`, `cs68`, `cs520h`, `ls65`.
- `safety_limits`: default `true`. Enables safety limit elements in the model.
- `safety_pos_margin`: default `0.15`. Joint safety position margin, in rad.
- `safety_k_position`: default `20`. Safety limit position coefficient.
- `runtime_config_package`: default `elite_robots_simulation_gz`. Controller configuration package providing the config directory.
- `controllers_file`: default `cs_controllers.yaml`. Controller YAML filename in that package's config directory.
- `description_package`: default `elite_robots_description`. Package providing the robot description.
- `description_file`: default `cs.urdf.xacro`. Model Xacro filename.
- `initial_positions_file`: default empty string. Simulation initial position YAML; selected by model when empty.
- `prefix`: default empty string. Prefix passed to the downstream model/SRDF; this version has inconsistent forwarding, as described in the MoveIt/Gazebo chapters.
- `start_joint_controller`: default `true`. Whether the simulation entry point starts the initial joint controller; this is not headless mode.
- `initial_joint_controller`: default `joint_trajectory_controller`. Name of the joint controller to load initially.
- `launch_rviz`: default `true`. Whether to start RViz.

## Combined Gazebo and MoveIt

Entry point: `elite_sim_moveit.launch.py`.

- `cs_type`: default `cs66`. Model string; accepted choices are listed for each entry point.
  Choices: `cs63`, `cs66`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs66a`, `cs68`, `cs520h`, `ls65`.
- `safety_limits`: default `true`. Enables safety limit elements in the model.
- `runtime_config_package`: default `elite_robots_simulation_gz`. Controller configuration package providing the config directory.
- `controllers_file`: default `cs_controllers.yaml`. Controller YAML filename in that package's config directory.
- `description_package`: default `elite_robots_description`. Package providing the robot description.
- `description_file`: default `cs.urdf.xacro`. Model Xacro filename.
- `moveit_config_package`: default `elite_robots_moveit_config`. Package providing SRDF, joint limits, and controller files; some other YAML files still come from the default package.
- `moveit_config_file`: default `cs.srdf.xacro`. SRDF Xacro filename.
- `moveit_joint_limits_file`: default `joint_limits.yaml`. MoveIt joint limits YAML filename.
- `moveit_controllers_file`: default `controllers.yaml`. MoveIt action controller mapping YAML filename.
- `prefix`: default empty string. Prefix passed to the downstream model/SRDF; this version has inconsistent forwarding, as described in the MoveIt/Gazebo chapters.

## Calibration

Entry point: `calibration_correction.launch.py`.

- `robot_ip`: **required**, with no default. Address of the physical robot or ELIBOTSim controller.
- `target_filename`: default `robot_calibration.yaml`. Calibration output file; maps to node parameter output_filename.

## Single-target motion example

Entry point: `example_safe_joint_move.launch.py`.

- `cpp_py`: default `cpp`. Example implementation: cpp or py.
- `target`: **required**, with no default. Target joint array, in rad.
- `max_vel`: default `0.5`. Velocity used to estimate trajectory duration, in rad/s.
- `min_time`: default `20.0`. Minimum trajectory duration, in s.
- `controller`: default `scaled_joint_trajectory_controller`. Target action controller name for the example.

## Standard trajectory loop example

Entry point: `example_joint_trajectory_controller.launch.py`.

- `robot_model`: default empty string. Example configuration selection; cs66a uses dedicated YAML, other values use the ordinary configuration.

## Scaled trajectory loop example

Entry point: `example_scaled_joint_trajectory_controller.launch.py`.

- `robot_model`: default empty string. Example configuration selection; cs66a uses dedicated YAML, other values use the ordinary configuration.

## Conditional replacement of default files

- For Driver models ending in h, the default controller file becomes `elite_cs_controllers_5f.yaml` and the default model uses `urdf_5f`.
- MoveIt also switches the default SRDF, joint limits, and controller configuration to `cs_5f.srdf.xacro`, `joint_limits_5f.yaml`, and `controllers_5f.yaml`.
- Gazebo uses `cs_controllers_5f.yaml` and the five-axis model. An empty initial position path selects the corresponding h/a/ordinary model file.
- Conditional replacement generally applies only to default filenames. When passing custom filenames, provide consistent axis counts, joint names, models, and controller configurations.

## Example entry point with no declared arguments

`example_forward_velocity_controller.launch.py` declares no user launch arguments. It starts a standard test publisher and loads test YAML from the package. It neither loads the velocity controller nor performs controller switching. Likewise, trajectory loop examples require the target controller to be ready and are not intended as general application clients.
