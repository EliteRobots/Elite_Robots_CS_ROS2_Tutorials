# 消息与服务类型

本章完整列出两个自定义接口包中的 **6 个消息、11 个服务**。以下代码块保留字段类型、常量和顺序，省略源文件注释；`---` 上方为服务请求，下方为响应，空白请求用 `{}` 调用。类型定义与接口的实际校验规则应结合阅读。

## elite_robots_msgs / msg

### Analog

完整类型：`elite_robots_msgs/msg/Analog`。

单个模拟通道：`type` 为通道类型，0 表示电流、1 表示电压；`value` 是控制器反馈值。ROS 层不进行缩放，物理范围应结合控制器配置确认。

```text
uint8 type
float64 value
```

### IOState

完整类型：`elite_robots_msgs/msg/IOState`。

数字数组元素为布尔状态。当前 GPIO 实现中，`standard_out/in` 各 16 项，`config_out/in` 各 8 项，`tool_out/in` 各 4 项；`standard_analog_out/in` 各 2 项，数组下标就是该组通道编号。消息本身是动态数组定义，订阅者应检查长度。消息没有 Header 或时间戳。

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

完整类型：`elite_robots_msgs/msg/RobotMode`。

`mode` 表示机器人模式。UNKNOWN 为未知，NO_CONTROLLER 为无控制器，DISCONNECTED 为断开，CONFIRM_SAFETY 为等待安全确认，BOOTING 为启动中，POWER_OFF/POWER_ON 为下电/上电，IDLE 为空闲，BACKDRIVE 为反驱，RUNNING 为运行，UPDATING_FIRMWARE 为固件更新，WAITING_CALIBRATION 为等待校准。

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

完整类型：`elite_robots_msgs/msg/SafetyMode`。

`mode` 表示安全模式。NORMAL/REDUCED 为正常/缩减，PROTECTIVE_STOP 为保护停止，RECOVERY 为恢复，SAFEGUARD_STOP 为防护停止，SYSTEM_EMERGENCY_STOP/ROBOT_EMERGENCY_STOP 为系统/机器人急停，VIOLATION/FAULT 为违规/故障，其余常量区分关节 ID 校验、未定义状态及不同使能装置停止。按下面的常量精确解析，不应仅把非 NORMAL 值统一解释为故障。

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

完整类型：`elite_robots_msgs/msg/TaskStatus`。

`status` 表示任务状态：UNKNOWN 未知、STOPPED 停止、PAUSED 暂停、PLAYING 运行。PLAYING 的 ROS 数值为 2。

```text
int8 UNKNOWN=-1
int8 STOPPED=0
int8 PAUSED=1
int8 PLAYING=2
int8 status
```

### ToolData

完整类型：`elite_robots_msgs/msg/ToolData`。

`mode` 为工具模式原始代码；`output_voltage`、`output_current`、`temperature` 分别为输出电压、电流与温度，数值直接来自 SDK。模拟类型和数值同样直接转交，不在 ROS 层换算。该消息未定义工具模式枚举，也没有时间戳；不要套用 RobotMode 常量解释工具模式。

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

完整类型：`elite_robots_msgs/srv/GetRobotMode`。

空请求。仅当 `success=true` 时解释 `mode.mode`；失败原因通常在 `message`。

```text
---
bool success
string message
RobotMode mode
```

### GetSafetyMode

完整类型：`elite_robots_msgs/srv/GetSafetyMode`。

空请求。仅当 `success=true` 时解释 `mode.mode`。

```text
---
bool success
string message
SafetyMode mode
```

### GetTaskStatus

完整类型：`elite_robots_msgs/srv/GetTaskStatus`。

空请求。仅当 `success=true` 时解释 `status.status`。

```text
---
bool success
string message
TaskStatus status
```

### SetIO

完整类型：`elite_robots_msgs/srv/SetIO`。

`fun` 选择操作，`pin` 为组内通道号，`analog_type` 仅模拟输出使用，`state` 的含义取决于操作。合法通道和实现限制见[GPIO 服务](controllers.md)。响应没有错误字符串。

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

完整类型：`elite_robots_msgs/srv/SetPayload`。

`mass` 为负载质量，`center_of_gravity` 为相对法兰的重心向量。字段直接传给 SDK。响应没有错误字符串。

```text
float32 mass
geometry_msgs/Vector3 center_of_gravity
---
bool success
```

### SetSpeedSliderFraction

完整类型：`elite_robots_msgs/srv/SetSpeedSliderFraction`。

请求比例数值；本版服务实际范围为 **0.01～1.0**，原类型注释中的 0 下限与实现不一致。响应没有错误字符串。

```text
float64 speed_slider_fraction
---
bool success
```

## elite_robots_dashboard_msgs / srv

### CustomRequest

完整类型：`elite_robots_dashboard_msgs/srv/CustomRequest`。

原始 Dashboard 请求/文本响应；没有 success 字段，异常文本也可能出现在 response 中。

```text
string request
---
string response
```

### IsSaved

完整类型：`elite_robots_dashboard_msgs/srv/IsSaved`。

空请求。success 表示查询成功，is_saved 才是保存状态，二者不能混用。

```text
---
bool success
string message
bool is_saved
```

### Load

完整类型：`elite_robots_dashboard_msgs/srv/Load`。

filename 是控制器端路径；answer 是说明或异常文本，success 是执行结果。

```text
string filename
---
string answer
bool success
```

### Log

完整类型：`elite_robots_dashboard_msgs/srv/Log`。

请求 message 是待写日志文本；响应 message 是返回说明或异常文本。

```text
string message
---
string message
bool success
```

### Popup

完整类型：`elite_robots_dashboard_msgs/srv/Popup`。

arg 是 SDK/控制器的弹窗操作参数，message 是内容；响应 success 与 message 表示结果。ROS 定义没有列出 arg 合法枚举。

```text
string arg
string message
---
bool success
string message
```

## 安装版本核对

```bash
ros2 interface show elite_robots_msgs/srv/SetIO
ros2 interface show elite_robots_msgs/msg/TaskStatus
ros2 interface show elite_robots_dashboard_msgs/srv/Load
```

这些命令读取已加载工作空间的安装接口，而不是任意源码目录；修改源码后未重建或加载了其他 overlay 时，结果可能与本文不同。
