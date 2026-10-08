# Preparation and isolation

## Scope of the setup

The driver template includes `elite_robots_driver/launch/elite_control.launch.py` twice, starting a separate controller manager for each arm. The optional MoveIt template includes `elite_moveit.launch.py` twice; each instance plans and executes trajectories for its own arm.

This setup does not create a combined robot model, a joint planning group spanning both robots, or a synchronized executor. Independent planning scenes do not automatically know about the other arm. Namespaces and prefixes also do not establish physical mounting positions. Coordinated motion in a shared workspace requires consistent base transforms, a complete collision model, and execution coordination.

## What must be isolated per arm

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - Item
  - arm1
  - arm2
* - ROS namespace
  - `arm1`
  - `arm2`
* - Joint/TF prefix
  - `arm1_`
  - `arm2_`
* - Controller manager
  - `/arm1/controller_manager`
  - `/arm2/controller_manager`
* - Default controller IP
  - `192.168.1.101`
  - `192.168.1.102`
* - Default model
  - `cs63`
  - `cs63`
* - MoveIt planning group
  - `arm1_cs_manipulator`
  - `arm2_cs_manipulator`
```

ROS namespaces isolate nodes, services, topics, and actions. Prefixes isolate joint, link, and hardware resource identifiers. Configure both. A name prefix is not a spatial transform, and the shared `world` root in the default models does not mean the relative arm positions have been calibrated.

Robot communication ports on the same ROS computer must also be distinct. The four port types are reverse, script sender, trajectory, and script command: arm1 defaults to 50001–50004 and arm2 to 50101–50104.

## Environment and files

Build and source the workspace first:

```bash
cd ~/elite_ros_ws
source /opt/ros/humble/setup.bash
colcon build --packages-up-to elite_robots_driver elite_robots_moveit_config
source install/setup.bash
mkdir -p ~/dual_arm_launch
cd ~/dual_arm_launch
```

Replace the example workspace `~/elite_ros_ws` with the actual location. Source ROS and the workspace in each new terminal. Save the complete code in the following chapters as:

```text
~/dual_arm_launch/
├── dual_arm_control.launch.py
└── dual_moveit.launch.py
```

Alternatively, save the files using the download links in those chapters. Downloads and displayed code reference the same files to prevent omissions during manual copying.

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

This setup uses system time. It is not a Gazebo procedure and needs no Gazebo `/clock` bridge. The dual-arm wrapper does not expose separate `local_ip` arguments and retains single-arm automatic address selection. If multiple network interfaces require explicit per-arm addresses, add and forward the corresponding arguments in your custom wrapper.
