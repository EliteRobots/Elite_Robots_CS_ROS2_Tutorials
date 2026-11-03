# Getting started with the driver

## Startup and connection

First complete [network setup or ELIBOTSim startup](robot_setup.md), then make sure each terminal has the environment required by your installation method.

An apt installation only requires the ROS 2 environment; a source installation also requires the corresponding workspace. If you added the required `source` commands to `~/.bashrc` as described in the installation chapter, new Bash terminals load them automatically, so you do not need to run them again. If the environment was not loaded automatically, or the terminal was already open before you configured `.bashrc`, follow {ref}`Terminal environment setup <terminal-environment>` to load it manually.

### Start the driver

```bash
ros2 launch elite_robots_driver elite_control.launch.py robot_ip:=<robot_ip> cs_type:=<cs_type> headless_mode:=true
```

- `robot_ip`: Reachable IP address of the physical robot or ELIBOTSim container.
- `cs_type`: Actual robot model, such as `cs66`.
- `headless_mode`: Enables headless operation. The driver sends the external control script, so you do not need to add an external control node manually on the teach pendant.
- `local_ip`: Optional address of the ROS computer, which must be reachable from the robot. The default, `0.0.0.0`, automatically selects the local address used to connect to the robot. With multiple network interfaces or a virtual machine, append `local_ip:=<local_ip>` to select it explicitly.

Once robot state is received, the robot pose in RViz should match the teach pendant. Displaying the pose does not mean that motion is ready: complete the power-on, brake-release, and external control script startup steps below.

```{figure} images/fig-4-1-rviz.png
:name: fig-4-1-rviz
:alt: Robot pose in RViz
:width: 90%
:align: center

Robot pose in RViz
```

```{figure} images/fig-4-2-pendant.png
:name: fig-4-2-pendant
:alt: Robot pose on the teach pendant
:width: 90%
:align: center

Robot pose on the teach pendant
```

## Service call examples

Keep the driver node running and use another terminal with the environment sourced to call services. Services such as power-on and brake release change the robot state; you do not need to perform the same operation on the teach pendant beforehand.

### Take control of the robot

**Power on:**

```bash
ros2 service call /dashboard_client/power_on std_srvs/srv/Trigger "{}"
```

A successful call produces output like this:

```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

The robot changes from powered off to standby.

```{figure} images/fig-4-3-standby.png
:name: fig-4-3-standby
:alt: Robot in standby
:width: 90%
:align: center

Robot in standby
```

**Release the brakes:**

```bash
ros2 service call /dashboard_client/brake_release std_srvs/srv/Trigger "{}"
```

A successful call produces output like this:

```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

The robot enters normal mode.

```{figure} images/fig-4-4-normal-mode.png
:name: fig-4-4-normal-mode
:alt: Robot in normal mode
:width: 90%
:align: center

Robot in normal mode
```

**Start the external control script:**

The following operation applies to the headless mode enabled in this chapter. This service stops the current task and sends the external control script again.

```bash
ros2 service call /io_and_status_controller/resend_external_script std_srvs/srv/Trigger "{}"
```

A successful call produces output like this:

```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

A successful service response means that the script was sent. Confirm that the teach pendant then shows the running state, and use the task status query below to confirm that the script is executing.

```{figure} images/fig-4-5-running-mode.png
:name: fig-4-5-running-mode
:alt: Robot in the running state
:width: 90%
:align: center

Robot in the running state
```

**Query the current task status:**

```bash
ros2 service call /dashboard_client/get_task_status elite_robots_msgs/srv/GetTaskStatus "{}"
```

A successful call produces output like this:

```
requester: making request: elite_robots_msgs.srv.GetTaskStatus_Request()

response:
elite_robots_msgs.srv.GetTaskStatus_Response(success=True, message='', status=elite_robots_msgs.msg.TaskStatus(status=2))
```

```{note}
1. `status=2` means the task is executing (`PLAYING`); `0` means stopped and `1` means paused. Driver-controlled motion depends on the external control script continuing to run.
2. A log message containing `Socket timed out waiting for command on reverse_socket` means that the script timed out waiting for control commands. The current robot description defaults `robot_receive_timeout` to 0.2 s (200 ms); the actual value depends on the hardware configuration. Check the ROS computer's load, scheduling latency, and network connection. Use a real-time kernel if necessary.
3. If services under `/dashboard_client/` are missing, check the driver startup log and Dashboard network connection. The node is not loaded if the Dashboard connection fails.
```

```{figure} images/fig-4-6-control-timeout.png
:name: fig-4-6-control-timeout
:alt: Control command receive timeout
:width: 90%
:align: center

Control command receive timeout
```

## Controllers and joint trajectories

`ros2_control` manages robot hardware and controllers.

```{list-table}
:header-rows: 1
:widths: 52 48

* - Controller / broadcaster
  - Purpose
* - `joint_state_broadcaster`
  - Publish joint states.
* - `io_and_status_controller`
  - Provide IO, robot state, and external control script services.
* - `speed_scaling_state_broadcaster`
  - Publish speed scaling on `~/speed_scaling` as a percentage (0–100).
* - `scaled_joint_trajectory_controller`
  - Adjust trajectory progress according to the robot's speed scaling.
* - `forward_position_controller`
  - Receive joint position commands directly; inactive by default.
* - `freedrive_controller`
  - Provide freedrive control; inactive by default.
* - `tcp_pose_broadcaster`
  - Publish the TCP pose.
* - `force_torque_sensor_broadcaster`
  - Publish force/torque data.
```

These names correspond to the default configuration. The full speed scaling topic name is `/speed_scaling_state_broadcaster/speed_scaling`, with type `std_msgs/msg/Float64`. The internal hardware scaling value is between 0 and 1 and is converted to a percentage for publication.

```{warning}
Before running the following trajectory or program examples, make sure the driver is running, the robot is in the running state, and the surrounding area is safe. These examples move the robot.
```

### Check controller states

```bash
ros2 control list_controllers
```

A successful command produces output like this:

```
speed_scaling_state_broadcaster    elite_robots_controllers/SpeedScalingStateBroadcaster         active
tcp_pose_broadcaster               pose_broadcaster/PoseBroadcaster                              active
joint_state_broadcaster            joint_state_broadcaster/JointStateBroadcaster                 active
forward_position_controller        position_controllers/JointGroupPositionController             inactive
scaled_joint_trajectory_controller elite_robots_controllers/ScaledJointTrajectoryController      active
io_and_status_controller           elite_robots_controllers/GPIOController                       active
freedrive_controller               elite_robots_controllers/FreedriveController                  inactive
force_torque_sensor_broadcaster    force_torque_sensor_broadcaster/ForceTorqueSensorBroadcaster  active
```

### Send a trajectory through a topic

The following example publishes one message to the trajectory controller. Target angles are in radians and times are in seconds. The topic, action, and program examples assume a six-axis robot such as the CS66 with no joint-name prefix. CS520H is a five-axis model and cannot use these six-joint examples unchanged. If you configure a prefix, also update the joint names.

```bash
ros2 topic pub --once \
  /scaled_joint_trajectory_controller/joint_trajectory \
  trajectory_msgs/msg/JointTrajectory "
joint_names:
  - shoulder_pan_joint
  - shoulder_lift_joint
  - elbow_joint
  - wrist_1_joint
  - wrist_2_joint
  - wrist_3_joint
points:
  - positions: [0.0, -1.0, 1.0, -1.5, 1.5, 0.0]
    time_from_start: {sec: 2}
"
```

If execution succeeds, the robot moves to joint angles `[0.0, -1.0, 1.0, -1.5, 1.5, 0.0]`.

### Send a trajectory through an action

You can also use the `FollowJointTrajectory` action:

```bash
ros2 action send_goal \
  /scaled_joint_trajectory_controller/follow_joint_trajectory \
  control_msgs/action/FollowJointTrajectory "
trajectory:
  joint_names:
    - shoulder_pan_joint
    - shoulder_lift_joint
    - elbow_joint
    - wrist_1_joint
    - wrist_2_joint
    - wrist_3_joint
  points:
    - positions: [0.0, -1.57, 1.0, -1.5, 1.5, 0.0]
      time_from_start: {sec: 2}
"
```

After successful execution, the robot reaches the specified target joint positions.

```{figure} images/fig-4-7-trajectory-result.png
:name: fig-4-7-trajectory-result
:alt: Trajectory execution result
:width: 90%
:align: center

Trajectory execution result
```

## Programmatic control examples

### Python example

```bash
ros2 run elite_robots_driver example_safe_joint_move_py --ros-args \
  -p target:="[0.0,-1.2,0.0,-1.57,0.0,0.0]" \
  -p max_vel:=0.5 \
  -p min_time:=2.0 \
  -p controller:="scaled_joint_trajectory_controller"
```

Reference: [Python example source](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver/blob/humble/elite_robots_driver/example/python/example_safe_joint_move.py).

### C++ example

```bash
ros2 run elite_robots_driver example_safe_joint_move --ros-args \
  -p target:="[0.0,-1.57,0.0,-1.0,-1.57,0.0]" \
  -p max_vel:=0.5 \
  -p min_time:=2.0 \
  -p controller:="scaled_joint_trajectory_controller"
```

Reference: [C++ example source](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver/blob/humble/elite_robots_driver/example/cpp/example_safe_joint_move.cpp).

### Parameters

```{list-table}
:header-rows: 1
:widths: 25 75

* - Parameter
  - Description
* - `target`
  - Six target joint angles (rad); write integers in ROS parameter arrays as floating-point values, such as `1.0`
* - `max_vel`
  - Joint speed (rad/s) used to estimate trajectory duration; a positive value is recommended
* - `min_time`
  - Minimum trajectory duration (s); use a positive value
* - `controller`
  - Name of the trajectory controller to use
```

```{note}
When `max_vel > 0`, the program sets the target point's `time_from_start` to the larger of `min_time` and the maximum joint angle difference divided by `max_vel`. When `max_vel <= 0`, it uses `min_time` directly. This estimates trajectory duration; it does not impose a hard limit on instantaneous velocity during interpolation. Actual execution also depends on controller speed scaling and other factors.
```
