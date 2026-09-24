# CS, ES and LS Series ROS 2 Quickstart Guide

**ELITE ROBOTS**

Document version: **1.0.0** · Revision date: **2026-09-24**

This guide covers the installation and basic use of the ELITE ROS 2 packages. It walks you through robot network configuration, development environment setup, driver startup, motion planning with MoveIt 2, and physics simulation with Gazebo.

(applicable-versions)=
```{rubric} Applicable versions
```

Version **1.0.0** of this guide applies to the package versions below (recorded on 2026-09-24). The instructions have been checked against the source code; execution on physical hardware has not been verified.

```{list-table}
:header-rows: 1
:widths: 75 25

* - ROS package
  - Applicable version
* - `elite_robots`
  - `1.2.0`
* - `elite_robots_calibration`
  - `1.2.0`
* - `elite_robots_controllers`
  - `1.2.0`
* - `elite_robots_dashboard_msgs`
  - `1.2.0`
* - `elite_robots_driver`
  - `1.2.0`
* - `elite_robots_moveit_config`
  - `1.2.0`
* - `elite_robots_msgs`
  - `1.2.0`
* - `elite_robots_description`
  - `1.0.0`
* - `elite_cs_series_sdk`
  - `1.4.7`
* - `elite_robots_simulation_gz`
  - `1.0.2`
```

- **ROS and operating system**: Commands have been checked against Ubuntu 22.04 / ROS 2 Humble. The project also declares support for Ubuntu 24.04 / ROS 2 Jazzy, but the Jazzy branch has not been checked instruction by instruction for this revision. The Gazebo procedure applies to Humble only.
- **Robot control software**: The current SDK README specifies a minimum version of 2.15.0. This does not represent a compatibility range tested for this guide. See [Robot setup](robot_setup.md) for ELIBOTSim image selection.
- **Versioning**: The document version is independent of the ROS package versions and the robot control software version. See the [Changelog](changelog.md) for document changes.

(how-to-use-this-guide)=
```{rubric} How to use this guide
```

Before you begin, check the robot model, control software version, ROS package versions, and development environment. Binary packages in the package repositories may differ from the source versions listed above; check the versions actually installed.

Follow these steps:

1. Read the [Overview](overview.md) to check supported platforms and package contents.
2. In [Robot setup](robot_setup.md), choose either a physical robot or the ELIBOTSim virtual teach pendant and test the connection.
3. Follow [Local environment setup](installation.md) to prepare the development environment and build the driver.
4. Follow [Getting started with the driver](driver.md) to start the robot and try basic services and trajectory control.
5. Try [MoveIt 2](moveit.md) or [Gazebo](gazebo.md) as needed. Gazebo physics simulation does not require a physical robot or ELIBOTSim.

Values such as `<robot_ip>`, `<local_ip>`, and `<cs_type>` are placeholders. Replace them with actual values and remove the angle brackets before running a command. When using multiple terminals, source the ROS 2 and workspace setup files in each terminal.

Screenshots retain the existing interface language. Captions and instructions are provided in English; menu labels may differ with the selected interface language or software version.

```{warning}
Before running any motion example, ensure that the robot is in the required state and that its surroundings are safe. The joint positions in this guide are examples; check that they are suitable for your actual workspace before using them.
```

**Use and copyright**

Read this guide before installing or using the product, and keep it for future reference. The content may change between versions. Illustrations are for reference; the actual product takes precedence.

Content and information are subject to change without notice. ELITE ROBOTS assumes no responsibility for errors in this guide or for incidental or consequential harm resulting from the use of this guide or the products described in it.

Copyright © 2026 ELITE ROBOTS. All rights reserved.

```{toctree}
:maxdepth: 3
:numbered:
:caption: Contents

overview
robot_setup
installation
driver
moveit
gazebo
support
changelog
```
