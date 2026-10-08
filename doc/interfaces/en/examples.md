# Client examples and interface checks

## Read-only checks after startup

These commands assume ROS and workspace environments have been loaded and the appropriate driver is running. They were not executed against a robot while preparing this manual.

```bash
ros2 node list
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 topic list -t
ros2 service list -t
ros2 action list -t
ros2 topic echo /joint_states --once
ros2 topic info /io_and_status_controller/io_states -v
```

Check joint names and counts, active controller states, interface types, and continuously updating feedback timestamps. `ros2 topic hz` reports only the observed frequency, not a guarantee of underlying real-time behavior. Mode topics publish on changes; a lack of continuous output does not necessarily indicate disconnection.

## Querying robot state

```bash
ros2 service call /dashboard_client/robot_mode \
  elite_robots_msgs/srv/GetRobotMode '{}'

ros2 service call /dashboard_client/get_safety_mode \
  elite_robots_msgs/srv/GetSafetyMode '{}'

ros2 service call /dashboard_client/get_task_status \
  elite_robots_msgs/srv/GetTaskStatus '{}'
```

For each response, check success first, then read mode.mode or status.status. To observe the external control program's running state, subscribe with:

```bash
ros2 topic echo /io_and_status_controller/robot_task_running \
  --qos-durability transient_local
```

This requires a sample to have been published. Dashboard queries and this Bool have different semantics: the former report robot task status, while the latter additionally requires a valid external control connection.

## IO and speed slider request formats

The following commands change robot or peripheral state. Call them only after confirming the purpose of the channels, tool voltage, and operating conditions. These are service format examples, not steps to execute automatically at startup.

Set standard digital output 0 high:

```bash
ros2 service call /io_and_status_controller/set_io \
  elite_robots_msgs/srv/SetIO \
  '{fun: 1, pin: 0, analog_type: 0, state: 1.0}'
```

Set the speed slider to 25%:

```bash
ros2 service call /io_and_status_controller/set_speed_slider \
  elite_robots_msgs/srv/SetSpeedSliderFraction \
  '{speed_slider_fraction: 0.25}'
```

Read back IO/speed state afterward. Service availability, request transmission, a true success response, and an actual state change are separate conditions to check.

## Six-axis motion example programs

The Driver C++ and Python examples read `/joint_states`, reorder current positions by joint name, and send a start point and a target point to the selected controller's `follow_joint_trajectory`. Both programs use fixed, unprefixed six-axis names and do not support `cs520h`.

- `controller`: string; direct execution default `scaled_joint_trajectory_controller`.
- `target`: double[]; required in Python; C++ default `[0.0, -1.2, 0.0, -1.57, 0.0, 0.0]`.
- `max_vel`: double; direct execution default 0.5 rad/s.
- `min_time`: double; direct execution default 2.0 s.

Duration is estimated as `max(max_i(abs(target_i-current_i))/max_vel, min_time)`. `max_vel` is only an input to this estimate, not a hard controller velocity limit. The examples do not perform collision planning. Supply a positive velocity and verified targets.

`example_safe_joint_move.launch.py` defaults `min_time` to **20.0 s**, unlike the 2.0 s default with direct ros2 run. The launch argument `target` is required.

The following example is only for an already running six-axis Gazebo instance with the standard trajectory controller and a verified target. It causes motion:

```bash
ros2 run elite_robots_driver example_safe_joint_move_py --ros-args \
  -p controller:=joint_trajectory_controller \
  -p target:='[0.0, -1.57, 0.0, -1.57, 0.0, 0.0]' \
  -p max_vel:=0.2 -p min_time:=20.0 -p use_sim_time:=true
```

For a physical robot using the scaled trajectory controller, also ensure the external control task is running, robot mode is appropriate, and the controller is active. Recheck the target against the actual environment.

## Application action client workflow

1. Obtain fresh joint states and map them by name. Check the axis count, prefix, target ranges, and clock source.
2. Wait for the expected action server with a connection timeout. A similarly named topic does not prove that the server can execute goals.
3. Build complete joint_names and points with increasing times, and select path and goal tolerances.
4. Check goal acceptance after sending. If rejected, do not continue waiting for motion completion.
5. Receive feedback and track the final action status, error_code, and error_string.
6. On cancellation, disconnection, or an application error, follow an explicit stopping procedure and independently verify robot state.

Set timeouts for responses, execution, and cancellation to avoid waiting indefinitely. A management service stop and an action cancellation operate at different interface layers; coordinate them according to the application's control ownership.

## Common interface issues

```{list-table}
:header-rows: 1
:widths: 40 60

* - Symptom
  - What to check
* - Dashboard services are absent
  - Fake hardware does not load components; the component process may have removed Dashboard after an initial connection failure.
* - A trajectory goal is rejected
  - Inactive controller, wrong joint count/names, inconsistent prefixes, or invalid trajectory timing.
* - MoveIt plans but cannot execute
  - Actual controllers differ from MoveIt defaults; MoveIt does not start the manager automatically.
* - Gazebo planning or TF stalls
  - No publisher/data on `/clock`, or nodes using different time sources.
* - Speed setting fails
  - A percentage such as 25 was used instead of 0.25, or the request is below 0.01.
* - Mode topics do not publish continuously
  - This version publishes only on changes; query a service for current state.
* - IO success is true but output is unchanged
  - Validate channel ranges, check asynchronous timeout logs, and read back actual IO.
* - TCP pose differs from TF
  - Different reference frames, or model tool0 is being compared with controller TCP.
* - A five-axis example reports parameter errors
  - Examples are fixed to six axes; use five-axis configuration and a custom trajectory client.
* - Source changes do not affect interfaces
  - Check the installation path, rebuild status, and terminal overlay order.
```
