# Before you start

## Scope of the setup

The driver template includes `elite_robots_driver/launch/elite_control.launch.py` twice, starting a separate controller manager for each arm. The optional MoveIt template includes `elite_moveit.launch.py` twice; each instance plans and executes trajectories for its own arm.

This setup does not create a combined robot model, a joint planning group spanning both robots, or a synchronized executor. Independent planning scenes do not automatically know about the other arm. Namespaces and prefixes also do not establish physical mounting positions. Coordinated motion in a shared workspace requires consistent base transforms, a complete collision model, and execution coordination.

## Environment and files

Install the Elite Robots ROS 2 driver correctly. If it is not installed, follow the relevant installation chapter in the Quick Start Guide. Source ROS and the workspace in each terminal used below.

Check installed arguments without starting a robot:

```bash
ros2 launch elite_robots_driver elite_control.launch.py --show-args
ros2 launch elite_robots_moveit_config elite_moveit.launch.py --show-args
```

The driver entry point must support namespaced configuration keys, absolute controller configuration paths, a specified manager, and disabling its internal spawners. MoveIt must support absolute custom configuration paths and pass prefix to both URDF tf_prefix and SRDF. If these capabilities are absent, update and rebuild the relevant packages; copying the wrapper alone is insufficient.

## Operating scenarios

- Physical robots: both controllers must be reachable and able to connect back to the ROS computer. Enable remote control as required by robot configuration when using headless mode.
- ELIBOTSim: use reachable addresses of two independent simulated controllers, with the same reverse connection and port requirements. Do not point both arms to the same controller instance.
- Fake hardware: no robot connection; useful for joint and namespace integration, but not a complete controller simulator.
