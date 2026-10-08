# Elite Robots ROS 2 Multi-Arm Guide

**ELITE ROBOTS**

Document version: **1.0.0** · Revision date: **2026-10-08**

This manual assembles a dual-arm system from two independent single-arm instances. It covers driver isolation, controller configuration, startup checks, and optional separate MoveIt instances. Complete launch files are included and can be started from any directory after building and sourcing the workspace.

```{rubric} Applicable versions and validation scope
```

This edition was checked against the ROS 2 Humble sources: Driver packages **1.2.0** and Description **1.0.0**. The single-arm entry point must provide `controller_manager_name` and `spawn_controllers`; MoveIt must provide arguments including `kinematics_file`, `rviz_config_file`, and `prefer_scaled_controller`. Matching package names or an older interface manual do not establish that an installed version supports these features.

Source and documentation checks were performed; physical robot, fake hardware, and MoveIt integration tests were not run. The corresponding Jazzy versions have not been reviewed. This guide does not use the older interface reference's Driver 1.0.3 baseline.

```{rubric} Reading order
```

Read [Preparation and isolation](overview.md), save the [dual-arm driver template](driver.md), and follow [Startup and checks](operation.md). Add the [MoveIt template](moveit.md) if planning is required.

```{toctree}
:maxdepth: 2
:numbered:
:caption: Contents

overview
driver
operation
moveit
changelog
```
