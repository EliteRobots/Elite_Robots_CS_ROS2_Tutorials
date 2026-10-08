# Message and service types

This chapter lists all **6 messages and 11 services** in the two custom interface packages. Code blocks preserve field types, constants, and order while omitting source comments. For services, fields above `---` are the request and fields below it the response; call an empty request with `{}`. Read type definitions together with the actual validation rules for each interface.

## elite_robots_msgs / msg

### Analog

Full type: `elite_robots_msgs/msg/Analog`.

A single analog channel. `type` identifies the channel type: 0 for current and 1 for voltage. `value` is controller feedback. The ROS layer applies no scaling; confirm the physical range against controller configuration.

```text
uint8 type
float64 value
```

### IOState

Full type: `elite_robots_msgs/msg/IOState`.

Digital array elements are Boolean states. In the current GPIO implementation, `standard_out/in` each have 16 entries, `config_out/in` 8, `tool_out/in` 4, and `standard_analog_out/in` 2. Each index is the channel number within its group. The message defines dynamic arrays, so subscribers should check their lengths. There is no Header or timestamp.

```text
bool[] standard_out
bool[] config_out
bool[] tool_out
bool[] standard_in
bool[] config_in
bool[] tool_in
Analog[] standard_analog_out
Analog[] standard_analog_in
```

### RobotMode

Full type: `elite_robots_msgs/msg/RobotMode`.

`mode` identifies robot mode. UNKNOWN means unknown; NO_CONTROLLER means no controller; DISCONNECTED means disconnected; CONFIRM_SAFETY means awaiting safety confirmation; BOOTING means starting up; POWER_OFF/POWER_ON mean powered off/on; IDLE means idle; BACKDRIVE means backdrive; RUNNING means running; UPDATING_FIRMWARE means firmware update; WAITING_CALIBRATION means awaiting calibration.

```text
int8 UNKNOWN = -2
int8 NO_CONTROLLER = -1
int8 DISCONNECTED = 0
int8 CONFIRM_SAFETY = 1
int8 BOOTING = 2
int8 POWER_OFF = 3
int8 POWER_ON = 4
int8 IDLE = 5
int8 BACKDRIVE = 6
int8 RUNNING = 7
int8 UPDATING_FIRMWARE = 8
int8 WAITING_CALIBRATION = 9
int8 mode
```

### SafetyMode

Full type: `elite_robots_msgs/msg/SafetyMode`.

`mode` identifies safety mode. NORMAL/REDUCED mean normal/reduced operation; PROTECTIVE_STOP means protective stop; RECOVERY means recovery; SAFEGUARD_STOP means safeguard stop; SYSTEM_EMERGENCY_STOP/ROBOT_EMERGENCY_STOP distinguish system and robot emergency stops; VIOLATION/FAULT mean violation/fault. The remaining constants distinguish joint ID validation, undefined state, and stops associated with different enabling devices. Interpret the constants below precisely rather than treating every non-NORMAL value as a fault.

```text
int8 UNKNOWN = -2
int8 NORMAL = 1
int8 REDUCED = 2
int8 PROTECTIVE_STOP = 3
int8 RECOVERY = 4
int8 SAFEGUARD_STOP = 5
int8 SYSTEM_EMERGENCY_STOP = 6
int8 ROBOT_EMERGENCY_STOP = 7
int8 VIOLATION = 8
int8 FAULT = 9
int8 VALIDATE_JOINT_ID = 10
int8 UNDEFINED_SAFETY_MODE = 11
int8 AUTOMATIC_MODE_SAFEGUARD_STOP = 12
int8 SYSTEM_THREE_POSITION_ENABLING_STOP = 13
int8 TP_THREE_POSITION_ENABLING_STOP = 14
int8 mode
```

### TaskStatus

Full type: `elite_robots_msgs/msg/TaskStatus`.

`status` identifies task status: UNKNOWN, STOPPED, PAUSED, or PLAYING. The ROS numeric value of PLAYING is 2.

```text
int8 UNKNOWN=-1
int8 STOPPED=0
int8 PAUSED=1
int8 PLAYING=2
int8 status
```

### ToolData

Full type: `elite_robots_msgs/msg/ToolData`.

`mode` is the raw tool mode code. `output_voltage`, `output_current`, and `temperature` are output voltage, current, and temperature, passed directly from the SDK. Analog types and values are likewise forwarded without conversion in ROS. This message defines no tool mode enumeration and contains no timestamp; do not interpret tool mode using RobotMode constants.

```text
uint8 mode
float64 output_voltage
float64 output_current
float64 temperature
uint8 analog_input_type
float64 analog_input
uint8 analog_output_type
float64 analog_output
```

## elite_robots_msgs / srv

### GetRobotMode

Full type: `elite_robots_msgs/srv/GetRobotMode`.

Empty request. Interpret `mode.mode` only if `success=true`. The failure reason is normally in `message`.

```text
---
bool success
string message
RobotMode mode
```

### GetSafetyMode

Full type: `elite_robots_msgs/srv/GetSafetyMode`.

Empty request. Interpret `mode.mode` only if `success=true`.

```text
---
bool success
string message
SafetyMode mode
```

### GetTaskStatus

Full type: `elite_robots_msgs/srv/GetTaskStatus`.

Empty request. Interpret `status.status` only if `success=true`.

```text
---
bool success
string message
TaskStatus status
```

### SetIO

Full type: `elite_robots_msgs/srv/SetIO`.

`fun` selects the operation, `pin` is the channel number within its group, and `analog_type` is used only for analog output. The meaning of `state` depends on the operation. See [GPIO services](controllers.md) for valid channels and implementation limitations. The response has no error string.

```text
int8 FUN_SET_DIGITAL_OUT = 1
int8 FUN_SET_CONFIGURE_OUT = 2
int8 FUN_SET_TOOL_DIG_OUT = 3
int8 FUN_SET_ANALOG_OUT = 4
int8 FUN_SET_TOOL_VOLTAGE = 5
int8 STATE_OFF = 0
int8 STATE_ON = 1
int8 STATE_TOOL_VOLTAGE_0V = 0
int8 STATE_TOOL_VOLTAGE_12V = 12
int8 STATE_TOOL_VOLTAGE_24V = 24
int8 ANALOG_CURRENT = 0
int8 ANALOG_VOLTAGE = 1
int8 fun
int8 pin
int8 analog_type
float64 state
---
bool success
```

### SetPayload

Full type: `elite_robots_msgs/srv/SetPayload`.

`mass` is payload mass and `center_of_gravity` is the center of gravity vector relative to the flange. Fields are passed directly to the SDK. The response has no error string.

```text
float32 mass
geometry_msgs/Vector3 center_of_gravity
---
bool success
```

### SetSpeedSliderFraction

Full type: `elite_robots_msgs/srv/SetSpeedSliderFraction`.

Requests a fractional value. The actual service range in this version is **0.01–1.0**; the lower limit of 0 in the original type comment differs from the implementation. The response has no error string.

```text
float64 speed_slider_fraction
---
bool success
```

## elite_robots_dashboard_msgs / srv

### CustomRequest

Full type: `elite_robots_dashboard_msgs/srv/CustomRequest`.

Raw Dashboard request and text response. There is no success field, and response may contain exception text.

```text
string request
---
string response
```

### IsSaved

Full type: `elite_robots_dashboard_msgs/srv/IsSaved`.

Empty request. success indicates query success, whereas is_saved indicates whether the data is saved; these fields are not interchangeable.

```text
---
bool success
string message
bool is_saved
```

### Load

Full type: `elite_robots_dashboard_msgs/srv/Load`.

filename is a controller-side path. answer contains explanatory or exception text, and success indicates the operation result.

```text
string filename
---
string answer
bool success
```

### Log

Full type: `elite_robots_dashboard_msgs/srv/Log`.

The request message contains the text to log. The response message contains returned information or exception text.

```text
string message
---
string message
bool success
```

### Popup

Full type: `elite_robots_dashboard_msgs/srv/Popup`.

arg specifies the SDK/controller popup operation and message is its content. Response success and message describe the result. The ROS definition lists no valid arg enumeration.

```text
string arg
string message
---
bool success
string message
```

## Checking the installed version

```bash
ros2 interface show elite_robots_msgs/srv/SetIO
ros2 interface show elite_robots_msgs/msg/TaskStatus
ros2 interface show elite_robots_dashboard_msgs/srv/Load
```

These commands read installed interfaces from the loaded workspace, not an arbitrary source directory. Results may differ from this manual if sources were changed without rebuilding or a different overlay is loaded.
