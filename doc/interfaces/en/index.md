# Elite Robots ROS 2 Interface Reference

**ELITE ROBOTS**  
Document version: **1.0.0** · Revision date: **2026-09-28** · English

This manual describes the launch interfaces, parameters, topics, services, and actions for robot description, drivers, controllers, MoveIt 2, and Gazebo. It is intended for developers connecting robots through ROS 2, building applications, and integrating control systems.

```{rubric} Scope
```

The interface descriptions were checked against the ROS 2 Humble source branches: `elite_robots_description` **1.0.0**, the seven ROS packages in the Driver repository **1.0.3**, and `elite_robots_simulation_gz` **1.0.1**. This describes the source baseline, not a branching requirement for the documentation repository. The corresponding Jazzy versions have not been checked. Defaults and launch filenames in other versions may differ. The document version is independent of package versions.

Source review and documentation build checks have been completed. Operation with a physical robot, ELIBOTSim, or Gazebo has not been validated. Standard ROS controller and MoveIt interfaces also depend on the installed dependency versions; perform the [interface checks](examples.md) when deploying.

```{rubric} Reading paths
```

- To find a feature, start with [Packages and interface conventions](overview.md).
- To implement a client, read [Controller interfaces](controllers.md), [Robot management interfaces](dashboard.md), and [Message and service types](messages.md).
- To integrate launch files, use the [Launch argument reference](launch_reference.md) and distinguish launch arguments, node parameters, and hardware parameters.
- To use simulation, follow the separate launch steps in [Gazebo interfaces](gazebo.md) for this version.

```{toctree}
:maxdepth: 3
:numbered:
:caption: Contents

overview
description
driver
controllers
dashboard
messages
moveit
gazebo
examples
launch_reference
changelog
```
