# Controller interfaces

## Default loading and activation

The driver update rate defaults to **125 Hz**. The states below are the initial states requested by launch. The controller stopper, hardware connectivity, or startup failures may change them; query the controller manager for actual states.

```{list-table}
:header-rows: 1
:widths: 58 42

* - Controller name
  - Default state and purpose
* - `joint_state_broadcaster`
  - Active; joint states.
* - `io_and_status_controller`
  - Active; IO, tool, and runtime state services/topics.
* - `speed_scaling_state_broadcaster`
  - Active; speed scaling state.
* - `force_torque_sensor_broadcaster`
  - Active; TCP force/torque.
* - `tcp_pose_broadcaster`
  - Active; TCP pose from controller feedback.
* - `scaled_joint_trajectory_controller`
  - Default initial joint controller; activation is controlled by `activate_joint_controller`.
* - `forward_position_controller`
  - Loaded as inactive; direct joint position commands.
* - `freedrive_controller`
  - Loaded as inactive; freedrive.
* - `joint_trajectory_controller`
  - Configured in YAML, not additionally loaded by default; selectable as the initial controller.
* - `forward_velocity_controller`
  - Configured in YAML, not additionally loaded by default; load as needed.
```

Custom plugins are `elite_robots_controllers/GPIOController`, `SpeedScalingStateBroadcaster`, `ScaledJointTrajectoryController`, and `FreedriveController` (the last three also use the `elite_robots_controllers/` prefix). The remaining plugins come from ros2_controllers.

```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 service list -t
ros2 action list -t
```

The controller manager uses standard `controller_manager_msgs/srv/*` services, including `/controller_manager/list_controllers` (`ListControllers`), `list_hardware_interfaces` (`ListHardwareInterfaces`), `load_controller` (`LoadController`), `configure_controller` (`ConfigureController`), `switch_controller` (`SwitchController`), and `unload_controller` (`UnloadController`). Before switching, inspect request fields for the installed version and current resource claims. Switching controllers may immediately change the source of motion commands.

## Joint states, force, and TCP pose

- `/joint_states`: `sensor_msgs/msg/JointState`; contains `name`, `position`, `velocity`, and `effort`. Associate entries by name rather than assuming an array order.
- `/dynamic_joint_states`: `control_msgs/msg/DynamicJointState`; dynamic interface states from the standard joint state broadcaster.
- `/force_torque_sensor_broadcaster/ft_data`: `geometry_msgs/msg/WrenchStamped`; TCP force/torque, with configured frame `tool0`.
- `/tcp_pose_broadcaster/pose`: `geometry_msgs/msg/PoseStamped`; controller TCP pose, with configured reference frame `base`.
- `/tf`: `tf2_msgs/msg/TFMessage`; when TF publication is enabled on the pose broadcaster, its child frame is `tool0_controller`.

Frame names also receive the configured prefix. Force and torque use N and N·m; pose position uses m and orientation uses a quaternion. See [hardware resources](driver.md) for the special meaning of hardware `effort` feedback. Standard broadcaster interfaces and QoS depend on the installed ros2_controllers version; inspect them with `ros2 topic info -v`.

## Trajectory control actions

Default physical driver action:

```text
/scaled_joint_trajectory_controller/follow_joint_trajectory
control_msgs/action/FollowJointTrajectory
```

The standard trajectory controller uses `/joint_trajectory_controller/follow_joint_trajectory`. Both also receive the private `~/joint_trajectory` topic (`trajectory_msgs/msg/JointTrajectory`). Prefer an action when the application needs goal acceptance, feedback, and completion results. The standard controller base class provides trajectory state interfaces. Use `ros2 node info /<controller>` to inspect `~/controller_state`, compatibility state topics, and the `~/query_state` service in the installed version.

### Goals and feedback

- `trajectory.joint_names`: all controlled joint names, corresponding to the position arrays. Default `allow_partial_joints_goal=false` requires 5 names for five-axis robots and 6 for six-axis robots.
- `trajectory.points[].positions`: rad. Optional `velocities` use rad/s and `accelerations` rad/s². Nonempty arrays must match the joint name count.
- `trajectory.points[].time_from_start`: cumulative time from the trajectory start, strictly increasing and expressed using `sec` and `nanosec`.
- `trajectory.header.stamp`: start time. A zero timestamp requests starting as soon as possible; a nonzero timestamp must use the controller's clock.
- `path_tolerance`, `goal_tolerance`, and `goal_time_tolerance`: path, goal, and completion time tolerances. Controller defaults apply when omitted.
- Feedback contains `joint_names` and `desired`, `actual`, and `error` trajectory points. This robot uses the ordinary joint `trajectory`; planar/floating joint trajectories are not needed.

Standard result `error_code` values are: 0 success, -1 invalid goal, -2 mismatched joint names, -3 old start timestamp, -4 path tolerance violated, and -5 goal tolerance violated. On failure, also inspect `error_string` and the final action status. Request cancellation through the ROS action client; successful submission of a cancellation request does not prove that the robot has stopped.

Default driver YAML sets each joint's path tolerance to **0.9 rad**, goal tolerance to **0.1 rad**, stopped velocity tolerance to **0.2 rad/s**, and `goal_time=0.0`. The configured trajectory state publication rate is 100 Hz and the action monitoring rate is 20 Hz. Gazebo uses a different path tolerance; see [simulation interfaces](gazebo.md). These are software configuration values, not robot safety limits.

### Speed scaling

The scaled trajectory controller reads `speed_scaling/speed_scaling_factor` and adjusts trajectory progression accordingly. Parameter `speed_scaling_interface_name` specifies the resource name. For fake hardware and Gazebo, use the standard trajectory controller and a matching MoveIt action target.

`/speed_scaling_state_broadcaster/speed_scaling` uses `std_msgs/msg/Float64` and publishes the hardware fraction multiplied by 100, as a percentage. Parameter `state_publish_rate` defaults to 100.0. However, this implementation compares each individual update `period` without accumulating elapsed time and has a seconds conversion issue. A precise 100 Hz publication rate cannot be guaranteed. Applications should measure frequency and data freshness.

## Direct joint commands

Both `/forward_position_controller/commands` and `/forward_velocity_controller/commands` are subscription interfaces of type `std_msgs/msg/Float64MultiArray`. `data` follows the joint order in YAML and represents rad and rad/s respectively. The message contains no joint names, timestamp, or arrival time.

Direct commands provide no trajectory action result and do not automatically generate a motion plan with timing constraints. Velocity applications should update commands continuously and implement stopping behavior; do not assume that stopping publication automatically sets velocity to zero. Load and activate the appropriate controller first, and stop controllers occupying the same joint command interfaces.

## GPIO state topics

All private interfaces below use the prefix `/io_and_status_controller/`:

- `io_states`: `elite_robots_msgs/msg/IOState`; publishes digital and analog IO on each controller update.
- `tool_data`: `elite_robots_msgs/msg/ToolData`; publishes tool mode, voltage, current, temperature, and analog IO on each update.
- `robot_mode`: `elite_robots_msgs/msg/RobotMode`; publishes when the mode changes.
- `safety_mode`: `elite_robots_msgs/msg/SafetyMode`; publishes when the safety mode changes.
- `robot_task_running`: `std_msgs/msg/Bool`; publishes on state changes; true when the task is PLAYING and the external control connection is valid.

The first four use `SystemDefaultsQoS`. `robot_task_running` additionally uses `transient_local` durability, allowing matching late subscribers to receive retained samples. An initial sample is not guaranteed if the value has not changed at initialization. Robot mode and safety mode topics are not periodic heartbeats; use Dashboard query services when an immediate state query is required.

## GPIO services

These services also use `/io_and_status_controller/` and are created when the GPIO controller activates.

### set_io

Type `elite_robots_msgs/srv/SetIO`. Request fields: `int8 fun`, `int8 pin`, `int8 analog_type`, and `float64 state`. Response: `bool success`.

```{list-table}
:header-rows: 1
:widths: 8 35 22 35

* - fun
  - Function
  - pin
  - state
* - 1
  - Standard digital output
  - 0–15
  - 0 or 1
* - 2
  - Configurable digital output
  - 0–7
  - 0 or 1
* - 3
  - Tool digital output
  - 0–3
  - 0 or 1
* - 4
  - Standard analog output
  - 0–1
  - Output value passed to the RTSI recipe
* - 5
  - Tool voltage
  - Unused; examples use 0
  - 0, 12, or 24 V
```

For analog output, `analog_type=0` selects current and `1` selects voltage. Digital output and tool voltage do not use this field. The ROS layer neither converts units nor validates the analog `state` range, and the type definition provides no numeric range. Consult the controller RTSI recipe specification; do not assume that a physical readback value can be used directly as a write value.

This version's digital channel check admits the channel count itself as an upper bound, and its analog check does not correctly restrict output to two channels. Clients must validate against the ranges above; do not probe hardware with out-of-range indices. After a successful response, read back `io_states` or `tool_data` to verify the change.

### set_speed_slider

Type `elite_robots_msgs/srv/SetSpeedSliderFraction`. Request `float64 speed_slider_fraction`, with actual accepted range **[0.01, 1.0]**; response `bool success`. For example, 0.25 means 25%. Zero is rejected; do not use this service to implement stopping.

### set_payload

Type `elite_robots_msgs/srv/SetPayload`. Request `float32 mass` and `geometry_msgs/Vector3 center_of_gravity` specify payload mass and center of gravity relative to the flange frame. Response: `bool success`. These are normally configured in kg and m; the ROS layer passes them directly to the SDK without additional conversion or range checks. Use confirmed payload parameters before calling.

### Trigger services

All use `std_srvs/srv/Trigger`: empty request `{}`, response `bool success` and `string message`.

```{list-table}
:header-rows: 1
:widths: 40 60

* - Suffix
  - Function and conditions
* - `resend_external_script`
  - Resends the external control script in headless mode. Success does not mean the task has reached PLAYING.
* - `hand_back_control`
  - Makes the external control program return control; current ROS motion may terminate.
* - `zero_ftsensor`
  - Zeros the force/torque sensor; availability depends on robot configuration.
```

### Asynchronous result limitations

Parameter `check_io_successfull_retries` defaults to 10, with 50 ms between checks. The code exits when the retry count exceeds the limit (about 0.55 s by default, excluding scheduling delays). After a timeout, some callbacks still convert the nonzero waiting flag to `true`. Thus, `success=true` alone does not prove the underlying command completed. Check state readback and logs as well, particularly with fake hardware. Preserve the spelling `successfull` in the parameter name.

## Freedrive

`/freedrive_controller/enable_freedrive` is a subscription of type `std_msgs/msg/Bool`, queue depth 10. Start/end requests are processed only when the controller is active.

`data=true` requests freedrive and should be sent continuously as a keepalive; `data=false` requests termination. Parameter `inactive_timeout` defaults to **1 s**. A wall-clock timer resets on received commands; a timeout requests exit from freedrive. The topic has no completion response.

Stop conflicting joint motion control before starting. To finish, send false and confirm that the robot has exited freedrive before switching controllers. This version's `on_deactivate` mainly clears internal state and the timer; deactivating the controller alone is not confirmation that the underlying exit command completed.
