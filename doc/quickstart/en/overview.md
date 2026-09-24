# Overview

ROS (Robot Operating System) is a set of software libraries and tools for developing robot applications. ROS 2 extends ROS 1 with improvements to communication, real-time capabilities, and other areas.

ROS 2 applications are typically organized into packages and built in a workspace using `colcon`. Nodes within these packages interact through several communication mechanisms:

| Mechanism | Use in these packages |
| --- | --- |
| Topic | Continuously publish robot state or send control messages |
| Service | Perform request/response operations, such as powering on or querying status |
| Action | Execute tasks such as trajectories that need ongoing execution, feedback, and a result |

## Main features

- **Robot driver and control interfaces**: Send commands to the robot controller and receive state feedback.
- **Custom controllers**: Provide controllers adapted to ELITE robots.
- **MoveIt 2 integration**: Support motion planning, kinematics, collision detection, and trajectory execution.
- **RViz visualization**: Display robot models, joint states, and planning results to preview motion and support interactive control.
- **Gazebo physics simulation**: Test robot motion, control programs, and interaction with simulated environments.

## Package list

```{list-table}
:header-rows: 1
:widths: 52 48

* - Package
  - Purpose
* - `elite_robots`
  - Metapackage providing a single installation entry point for the Elite Robots ROS 2 packages.
* - `elite_robots_msgs`
  - Custom message and service interfaces for robot state, IO, and related operations.
* - `elite_robots_dashboard_msgs`
  - Dashboard message and service interfaces; some Dashboard services use `elite_robots_msgs`.
* - `elite_robots_controllers`
  - Robot controller implementations.
* - `elite_robots_calibration`
  - Read calibration data from a physical robot.
* - `elite_robots_description`
  - Robot description files and models.
* - `elite_robots_driver`
  - Communication, hardware interfaces, the driver, and examples.
* - `elite_cs_series_sdk`
  - C++ robot communication SDK used by the driver.
* - `elite_robots_simulation_gz`
  - Gazebo simulation configuration and examples (Humble only).
* - `elite_robots_moveit_config`
  - MoveIt 2 configuration and examples.
```

## Supported platforms and hardware requirements

Supported robot models:

- CS series: CS63, CS63a, CS66, CS68, CS612, CS616, CS618F, CS620, CS625, CS630, CS66A, CS520H
- ES series: ES63, ES63a, ES66, ES68, ES612, ES616, ES618F, ES620, ES625, ES630, ES66A, ES520H
- LS series: LS65

Platforms declared as formally tested and supported by the project:

- **Ubuntu 22.04 (Jammy Jellyfish) + ROS 2 Humble**
- **Ubuntu 24.04 (Noble Numbat) + ROS 2 Jazzy**

The commands in this guide use Humble. For Jazzy, use the packages and source branches for that distribution; do not mix them with Humble installation commands.

`cs_type` is the configuration name accepted by the launch file. The current driver and description packages accept `cs63`, `cs63a`, `cs66`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs630`, `cs66a`, `cs520h`, and `ls65`. Names are case-sensitive. The current launch files do not provide `es*` options such as `es66`; confirm the matching model configuration before using an ES-series robot. Check the Gazebo launch file for its supported options.

Allow sufficient memory for MoveIt 2 planning and RViz visualization. A GPU is not required for the basic control procedures in this guide.

## Common ROS 2 commands

Replace the package names, node names, interface types, and paths below with actual values.

### Nodes

```bash
# List packages and their installation paths
ros2 pkg list
ros2 pkg prefix <package_name>

# Run an executable or launch file
ros2 run <package_name> <executable_name>
ros2 launch <package_name> <file.launch.py>

# Inspect nodes
ros2 node list
ros2 node info <node_name>
```

Press `Ctrl+C` in the terminal that started a foreground process to stop it.

### Topics and interfaces

```bash
ros2 topic --help
ros2 topic list
ros2 topic echo /<topic_name>
ros2 topic info /<topic_name>
ros2 topic type /<topic_name>
ros2 interface show <interface_type>
```

`topic type` returns the interface type name. Use `interface show` to inspect its message fields.

### Services, parameters, and data recording

```bash
ros2 service --help
ros2 service list
ros2 service call <service_name> <service_type> '<arguments>'

ros2 param list
ros2 param get <node_name> <param_name>
ros2 param set <node_name> <param_name> <value>

ros2 bag record /<topic_name>
ros2 bag play <bag_path>
```

### Controllers and hardware interfaces

```bash
ros2 control list_controllers
ros2 control list_controller_types
ros2 control list_hardware_components
ros2 control list_hardware_interfaces
```

These commands list controllers and their states, available controller types, registered hardware components, and hardware interfaces such as position and velocity.
