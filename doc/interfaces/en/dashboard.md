# Robot management and script interfaces

## Dashboard node

The default node name is `dashboard_client`, and all services use private `~/...` names. Standalone entry point:

```bash
ros2 run elite_robots_driver dashboard_client \
  --ros-args -p robot_ip:=<robot_ip>
```

The driver launch normally starts this node through the component process, so a second standalone instance is unnecessary. The standalone node's `robot_ip` defaults to `192.168.51.244`; this is only a code default. Explicitly provide the actual controller address. Changing the parameter alone does not establish a new connection; the `connect` callback reads the current parameter and connects.

A service response reports the command or query return value. Requests such as power-on, brake release, and task playback require further checks of robot mode, safety state, and task status.

## Dashboard service directory

### Trigger services

All services below use `std_srvs/srv/Trigger`, with full names `/dashboard_client/<suffix>`. The request is empty; the response contains `success` and `message`.

```{list-table}
:header-rows: 1
:widths: 40 60

* - Suffix
  - Function
* - `power_on`
  - Power on the robot.
* - `power_off`
  - Power off the robot.
* - `brake_release`
  - Release the brakes.
* - `play`
  - Run the current task.
* - `pause`
  - Pause the current task.
* - `stop`
  - Stop the current task.
* - `shutdown`
  - Shut down the controller system.
* - `reboot`
  - Reboot the controller system.
* - `unlock_protective_stop`
  - Request release of a protective stop.
* - `close_safety_dialog`
  - Close the safety dialog.
* - `quit`
  - Close the Dashboard connection.
* - `restart_safety`
  - Restart the safety system.
* - `connect`
  - Connect to Dashboard using the current `robot_ip`.
* - `get_task_path`
  - Query the current task path; returned in `message`.
```

Callbacks for `shutdown`, `reboot`, and `quit` return true if the SDK call does not throw an exception. They do not wait for shutdown, reboot, or state transitions to finish. In `get_task_path`, `message` carries query data and must not always be treated as error text.

### Query services

- `/dashboard_client/get_task_status`: `elite_robots_msgs/srv/GetTaskStatus`; successful query data in `status.status`.
- `/dashboard_client/robot_mode`: `elite_robots_msgs/srv/GetRobotMode`; successful query data in `mode.mode`.
- `/dashboard_client/get_safety_mode`: `elite_robots_msgs/srv/GetSafetyMode`; successful query data in `mode.mode`.
- `/dashboard_client/is_task_saved`: `elite_robots_dashboard_msgs/srv/IsSaved`; successful query data in `is_saved`.
- `/dashboard_client/is_configuration_saved`: `elite_robots_dashboard_msgs/srv/IsSaved`; successful query data in `is_saved`.

All have empty requests and responses that also contain `success` and `message`. Check `success` before interpreting data. ROS task status constants are -1 unknown, 0 stopped, 1 paused, and 2 playing. The node maps SDK enums to ROS definitions; do not compare SDK numeric values directly with the response.

### File and interaction services

Service prefix: `/dashboard_client/`. Type package: `elite_robots_dashboard_msgs`.

- `load_task`: `srv/Load`; request `filename`; response `answer`, `success`.
- `load_configure`: `srv/Load`; request `filename`; response `answer`, `success`.
- `popup`: `srv/Popup`; request `arg`, `message`; response `success`, `message`.
- `log`: `srv/Log`; request `message`; response `message`, `success`.
- `custom_request`: `srv/CustomRequest`; request `request`; response `response`.

`filename` is the task or configuration file path on the robot controller, not on the ROS computer. These services do not upload files. `popup.arg` is passed unchanged to the SDK. The controller protocol defines the popup operation strings; the ROS type declares no enumeration of valid strings.

`custom_request` sends a raw Dashboard command and returns text, with no `success` field. SDK exception text is also written to `response`. Applications must parse protocol responses and identify errors instead of merely checking for nonempty text.

## Primary node

The standalone executable and default node name are both `primary_client`. Parameter `robot_ip` defaults to `192.168.51.244` and should be set explicitly. The node provides these `std_srvs/srv/Trigger` services through the Primary channel:

```text
/primary_client/power_on
/primary_client/power_off
/primary_client/brake_release
/primary_client/pause
/primary_client/stop
/primary_client/unlock_protective_stop
/primary_client/restart_safety
/primary_client/connect
```

Functions match their names. Response `success` comes from the SDK return value; on an exception it is false and `message` is populated. There are no Primary ROS services named `play`, `robot_mode`, or `get_task_status`. Do not reuse the entire Dashboard service directory by substituting the prefix.

Unlike Dashboard in the component process, Primary is still added to the executor after an initial connection failure, so `connect` can retry the connection. Controller permissions and required states for both channels are determined by the robot.

## Script sender node

Executable `script_node`, default node name `script_sender`, required parameter `robot_ip`:

```bash
ros2 run elite_robots_driver script_node \
  --ros-args -p robot_ip:=<robot_ip>
```

The node subscribes to `/script_sender/script_command` with type `std_msgs/msg/String` and queue depth 1. `data` contains the complete script, preserving newlines and indentation, sent through the Primary channel.

There is no result topic, service response, or action feedback. Transmission success is reported only in node logs; execution effects must be observed independently. Starting the node also sends a connection notification script containing `textmsg`, so it is not a purely read-only monitor.

An arbitrary script may change or replace the current robot task. Do not send uncoordinated motion scripts while trajectory control is executing. This manual describes the interface without providing motion script examples that would compete with the external control script.
