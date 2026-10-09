# Composing Multiple Elite Arms in This Project

This document is self-contained. The two launch files can be created in any
directory; they do not need to be installed into a ROS package:

```{code-block} text
dual_arm_control.launch.py
dual_moveit.launch.py
```

Copy the complete code from the corresponding sections below into those files.
After sourcing the workspace, run them directly by filename from their
directory:

```{code-block} bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py
ros2 launch dual_moveit.launch.py
```

The driver package provides the reusable single-arm entry point:

```{code-block} text
elite_robots_driver/launch/elite_control.launch.py
```

The dual-arm launch file includes it twice and assigns each arm its own
namespace, TF/joint prefix, controller manager, communication ports, and
controllers.

```{toctree}
:maxdepth: 2

launch_files
driver
startup
control
moveit
single_arm
```
