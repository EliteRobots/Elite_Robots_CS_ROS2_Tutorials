# Packages and interface conventions

## Package organization

The Description repository provides `elite_robots_description`: URDF/Xacro files, meshes, joint limits, model parameters, and RViz visualization. It defines no custom ROS messages or hardware control nodes.

The Driver repository contains seven packages, all at version 1.0.3:

```{list-table}
:header-rows: 1
:widths: 48 52

* - ROS package
  - Purpose
* - `elite_robots`
  - Dependency aggregation package with no separate application interface.
* - `elite_robots_driver`
  - ros2_control hardware plugin, management services, script sending, launch files, and examples.
* - `elite_robots_controllers`
  - IO, speed scaling, scaled trajectory, and freedrive controller plugins.
* - `elite_robots_msgs`
  - Robot state messages and IO, payload, and state query service types.
* - `elite_robots_dashboard_msgs`
  - Dashboard file, popup, log, and custom command service types.
* - `elite_robots_moveit_config`
  - SRDF, planning, trajectory execution, and Servo configuration.
* - `elite_robots_calibration`
  - One-shot tool that reads robot kinematics and writes calibration YAML.
```

The GZ Simulation repository provides `elite_robots_simulation_gz`, containing Gazebo launch files, simulation controller configuration, and a trajectory client. It defines no new messages, services, or actions.

## Interface layers

Applications communicate with nodes through ROS topics, services, or actions. Motion controllers access hardware through ros2_control command/state interfaces, and the hardware plugin communicates with the robot through the SDK. A hardware interface name such as `gpio/tool_voltage_cmd` is not a ROS topic and cannot be written directly with `ros2 topic pub`.

Description generates `robot_description`; `robot_state_publisher` converts joint states to TF. MoveIt reads the robot model and `/joint_states`, plans motion, and sends actions to a trajectory controller. Gazebo replaces the physical hardware plugin with a simulation system plugin.

## Names, direction, and namespaces

Unless stated otherwise, this manual assumes no ROS namespace or joint prefix and uses the default node and controller names. Publication and subscription directions are relative to the node providing the interface.

- `~/set_io` is a private node name. With a GPIO controller named `io_and_status_controller`, it resolves to `/io_and_status_controller/set_io`.
- `~/robot_mode` resolves to the service `/dashboard_client/robot_mode` in the Dashboard node, and to the topic `/io_and_status_controller/robot_mode` in the GPIO controller.
- `tf_prefix` prefixes joint, link, and hardware resource names; it does not automatically add a ROS namespace. MoveIt/Gazebo launch files use an argument named `prefix`, with model parameter inconsistencies described in their chapters.
- Default launch spawners use the absolute name `/controller_manager`. Multiple robots require consistent manager names, ROS namespaces, joint names, controller configurations, and client targets. A prefix alone does not provide isolation.

## Units and return values

Joint positions use rad, joint velocities rad/s, and times s. Cartesian positions generally use m, and orientation quaternions are dimensionless. Exceptions are stated for each interface.

The speed slider service accepts a fraction: `0.5` means 50%. The speed scaling topic publishes a percentage, such as `50.0`. The service implementation in this version accepts only **0.01–1.0**, rather than the 0–1 range in the type comment.

A completed ROS service call only confirms that a response was received. Also inspect application fields such as `success`. For actions, distinguish goal acceptance, the final action status, and the result `error_code`. The script topic has no result response; successful publication does not confirm script execution.

## Operating scenarios

- **Physical robot:** Elite hardware plugin; robot controller address and system time. Trajectory, state, IO, and management interfaces depend on connection and activation state.
- **ELIBOTSim:** Elite hardware plugin; simulated controller address and system time. Uses the same driver interfaces, with capabilities limited by the simulated controller.
- **Fake hardware:** GenericSystem; no robot connection and system time. Mirrors joint commands into states; real IO and management behavior is not guaranteed.
- **Gazebo:** IgnitionSystem; no robot IP and simulation time. Provides joint states and standard trajectory control by default, without Dashboard or Primary interfaces.

For physical robots and ELIBOTSim, `robot_ip` is the controller address. `local_ip` is an address of the ROS driver computer that the controller can reach. Gazebo needs neither address.
