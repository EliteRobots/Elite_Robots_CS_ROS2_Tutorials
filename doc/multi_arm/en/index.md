# Composing Multiple Elite Arms in This Project

Document version: **1.0.0** · Revision date: **2026-11-03** · English

The document version is independent of the ROS package version. See the [revision history](changelog.md) for changes.

This document is self-contained. The two launch files can be created in any
directory; they do not need to be installed into a ROS package:

```{code-block} text
dual_arm_control.launch.py
dual_moveit.launch.py
```

Copy the complete code from the corresponding sections below into those files,
then run them directly by filename from their directory:

```{code-block} bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py
ros2 launch dual_moveit.launch.py
```

The driver package provides the reusable single-arm entry point
`elite_control.launch.py`. The dual-arm launch file includes it twice and assigns each arm its own
namespace, TF/joint prefix, controller manager, communication ports, and
controllers.

```{toctree}
:maxdepth: 2

launch_files
driver
startup
control
moveit
changelog
```
