# Elite Robots ROS 2 Multi-Arm Guide

**ELITE ROBOTS**

Document version: **1.0.0** · Revision date: **2026-10-08**

This manual assembles a dual-arm system from two independent single-arm instances. It covers driver isolation, controller configuration, startup checks, and optional separate MoveIt instances.

```{rubric} Applicable versions
```

Check the version requirements using the following ROS packages:

```{list-table}
:header-rows: 1
:widths: 56 22 22

* - Package to check
  - Humble
  - Jazzy
* - `elite_robots`
  - `≥ 1.2.0`
  - `≥ 1.2.0`
* - `elite_robots_description`
  - `≥ 1.0.0`
  - `≥ 1.0.0`
```

```{rubric} Reading order
```

After [Before you start](overview.md), follow [Dual-arm driver guide](driver.md): get the example, launch it, and check the result, then read the explanation and configuration guidance. Follow the same sequence in the [Dual-arm MoveIt guide](moveit.md) when planning is required. See [Troubleshooting and returning to single-arm operation](operation.md) if needed.

```{toctree}
:maxdepth: 2
:numbered:
:caption: Contents

overview
driver
moveit
operation
changelog
```
