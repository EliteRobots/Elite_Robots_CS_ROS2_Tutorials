# 控制器接口

## 默认加载与激活

驱动默认更新率为 **125 Hz**。以下是 launch 请求的初始状态；实际状态可能被 controller stopper、硬件连接或启动失败改变，应以管理器查询为准。

```{list-table}
:header-rows: 1
:widths: 58 42

* - 控制器名称
  - 默认状态及职责
* - `joint_state_broadcaster`
  - 激活；关节状态。
* - `io_and_status_controller`
  - 激活；IO、工具和运行状态服务/话题。
* - `speed_scaling_state_broadcaster`
  - 激活；速度缩放状态。
* - `force_torque_sensor_broadcaster`
  - 激活；TCP 力/力矩。
* - `tcp_pose_broadcaster`
  - 激活；控制器反馈 TCP 位姿。
* - `scaled_joint_trajectory_controller`
  - 默认初始关节控制器；由 `activate_joint_controller` 决定是否激活。
* - `forward_position_controller`
  - 加载为 inactive；直接关节位置命令。
* - `freedrive_controller`
  - 加载为 inactive；自由拖动。
* - `joint_trajectory_controller`
  - YAML 已配置，默认不额外加载；可选为初始控制器。
* - `forward_velocity_controller`
  - YAML 已配置，默认不额外加载；可按需加载。
```

自定义插件分别为 `elite_robots_controllers/GPIOController`、`SpeedScalingStateBroadcaster`、`ScaledJointTrajectoryController`、`FreedriveController`（后三者同样带 `elite_robots_controllers/` 前缀）。其余来自 ros2_controllers。

```bash
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 service list -t
ros2 action list -t
```

控制器管理器使用标准 `controller_manager_msgs/srv/*` 服务，例如 `/controller_manager/list_controllers`（`ListControllers`）、`list_hardware_interfaces`（`ListHardwareInterfaces`）、`load_controller`（`LoadController`）、`configure_controller`（`ConfigureController`）、`switch_controller`（`SwitchController`）、`unload_controller`（`UnloadController`）。切换前先确认当前版本的请求字段和资源占用；控制器切换可能立即改变运动指令来源。

## 关节状态、力和 TCP 位姿

- `/joint_states`：类型：`sensor_msgs/msg/JointState`；内容：`name`、`position`、`velocity`、`effort`；按名称关联，勿假定订阅数组顺序。

- `/dynamic_joint_states`：类型：`control_msgs/msg/DynamicJointState`；内容：标准关节状态广播器的动态接口状态。

- `/force_torque_sensor_broadcaster/ft_data`：类型：`geometry_msgs/msg/WrenchStamped`；内容：TCP 力/力矩；配置的 frame 为 `tool0`。

- `/tcp_pose_broadcaster/pose`：类型：`geometry_msgs/msg/PoseStamped`；内容：控制器 TCP 位姿；配置的参考 frame 为 `base`。

- `/tf`：类型：`tf2_msgs/msg/TFMessage`；内容：启用位姿广播器 TF 发布时，子 frame 为 `tool0_controller`。


有前缀时 frame 名同样带前缀。力/力矩字段按 N、N·m 使用；位姿位置按 m、姿态按四元数使用。硬件反馈 `effort` 的特殊语义见[硬件资源](driver.md)。广播器的标准接口与 QoS 以实际安装的 ros2_controllers 为准，可用 `ros2 topic info -v` 核对。

## 轨迹控制动作

默认实体驱动动作：

```text
/scaled_joint_trajectory_controller/follow_joint_trajectory
control_msgs/action/FollowJointTrajectory
```

标准轨迹控制器对应 `/joint_trajectory_controller/follow_joint_trajectory`。两者也接收私有 `~/joint_trajectory` 话题（`trajectory_msgs/msg/JointTrajectory`）；需要目标接受、反馈和完成结果的应用优先使用动作。轨迹状态接口由标准控制器基类提供，可通过 `ros2 node info /<controller>` 核对当前版本的 `~/controller_state`、兼容状态话题和 `~/query_state` 服务。

### 目标与反馈

- `trajectory.joint_names`：全部受控关节名，必须与位置数组对应；默认 `allow_partial_joints_goal=false`，五轴传 5 个，六轴传 6 个。
- `trajectory.points[].positions`：rad；可选 `velocities` 为 rad/s、`accelerations` 为 rad/s²。数组非空时长度应与关节名匹配。
- `trajectory.points[].time_from_start`：从轨迹起点累计的时间，严格递增，使用 `sec`、`nanosec` 表示。
- `trajectory.header.stamp`：开始时间；零时间戳用于尽快开始，非零时间戳必须与控制器时钟一致。
- `path_tolerance`、`goal_tolerance`、`goal_time_tolerance`：路径、目标及完成时间容差；省略时由控制器默认值决定。
- 反馈包含 `joint_names` 以及 `desired`、`actual`、`error` 轨迹点；本机器人使用普通关节 `trajectory`，不需要填平面/浮动关节轨迹。

标准结果的 `error_code`：0 成功；-1 无效目标；-2 关节名不匹配；-3 起始时间已过期；-4 路径容差超限；-5 目标容差超限。失败时同时读取 `error_string` 和动作终态。取消通过 ROS 动作客户端的取消接口发起，不以取消请求发送成功作为机器人已停止的证明。

默认驱动 YAML 中轨迹路径容差为各关节 **0.9 rad**，目标容差 **0.1 rad**，停止速度容差 **0.2 rad/s**，`goal_time=0.0`；轨迹状态配置发布率 100 Hz、动作监视频率 20 Hz。Gazebo 的路径容差不同，见[仿真接口](gazebo.md)。这些默认值是软件配置，不是机器人安全限值。

### 速度缩放

缩放轨迹控制器读取 `speed_scaling/speed_scaling_factor`，据此调整轨迹推进时间。默认资源名由控制器参数 `speed_scaling_interface_name` 指定。fake hardware 和 Gazebo 应使用标准轨迹控制器，并让 MoveIt 的动作目标与之匹配。

`/speed_scaling_state_broadcaster/speed_scaling` 使用 `std_msgs/msg/Float64`，将硬件比例乘 100 后发布，单位为百分比。参数 `state_publish_rate` 默认 100.0，但本版实现直接比较单次 update 的 `period`，没有累计周期，并存在秒值转换问题；不能承诺话题严格以 100 Hz 发布。应用应实测频率和数据新鲜度。

## 直接关节命令

`/forward_position_controller/commands` 与 `/forward_velocity_controller/commands` 均为订阅接口，类型 `std_msgs/msg/Float64MultiArray`，`data` 按 YAML 的关节顺序排列，分别表示 rad 和 rad/s。此消息不带关节名、时间戳或到达时刻。

直接命令没有轨迹动作结果，也不会自动生成带时间约束的运动规划。速度控制应用应连续更新命令并设计停止处理，不能假设停止发布就自动归零。使用前必须加载并激活对应控制器，停止占用相同关节命令接口的控制器。

## GPIO 状态话题

以下私有接口前缀均为 `/io_and_status_controller/`：

- `io_states`：消息类型（包 `elite_robots_msgs`，另行注明除外）：`msg/IOState`；发布行为：每次控制器 update 发布；数字和模拟 IO。

- `tool_data`：消息类型（包 `elite_robots_msgs`，另行注明除外）：`msg/ToolData`；发布行为：每次 update 发布；工具模式、电压、电流、温度、模拟 IO。

- `robot_mode`：消息类型（包 `elite_robots_msgs`，另行注明除外）：`msg/RobotMode`；发布行为：模式发生变化时发布。

- `safety_mode`：消息类型（包 `elite_robots_msgs`，另行注明除外）：`msg/SafetyMode`；发布行为：安全模式发生变化时发布。

- `robot_task_running`：消息类型（包 `elite_robots_msgs`，另行注明除外）：`std_msgs/msg/Bool`；发布行为：状态变化时发布；任务为 PLAYING 且外部控制连接有效时为 true。


前四项使用 `SystemDefaultsQoS`；`robot_task_running` 在其基础上使用 `transient_local` 持久性，后加入的匹配订阅者可以接收已有保留样本。初始化时若值没有变化，不能保证已发布初始样本。机器人模式和安全模式话题不能作为固定频率心跳；需即时查询时使用 Dashboard 查询服务。

## GPIO 服务

服务前缀同样为 `/io_and_status_controller/`，在 GPIO 控制器激活时创建。

### set_io

类型 `elite_robots_msgs/srv/SetIO`。请求包含 `int8 fun`、`int8 pin`、`int8 analog_type`、`float64 state`，响应为 `bool success`。

| fun | 功能 | pin | state |
| --- | --- | --- | --- |
| 1 | 标准数字输出 | 0～15 | 0 或 1 |
| 2 | 可配置数字输出 | 0～7 | 0 或 1 |
| 3 | 工具数字输出 | 0～3 | 0 或 1 |
| 4 | 标准模拟输出 | 0～1 | 传给 RTSI 配方的输出值 |
| 5 | 工具电压 | 不使用，示例填 0 | 0、12 或 24 V |

模拟输出的 `analog_type=0` 表示电流，`1` 表示电压；数字输出和工具电压不使用此字段。ROS 层没有对模拟 `state` 做量纲换算或范围验证，本版类型定义也没有给出其数值范围；应依控制器 RTSI 配方规范确认，不能把读回物理量直接作为写入值。

本版数字通道边界检查允许了计数上界，模拟输出也未正确限定为两个通道。客户端必须按上表校验，不能通过发送越界编号探索硬件。返回成功后应读回 `io_states` 或 `tool_data` 确认实际变化。

### set_speed_slider

类型 `elite_robots_msgs/srv/SetSpeedSliderFraction`。请求 `float64 speed_slider_fraction`，实际允许 **[0.01, 1.0]**；响应 `bool success`。例如 0.25 表示 25%。0 会被拒绝，不应用该服务实现停止。

### set_payload

类型 `elite_robots_msgs/srv/SetPayload`。请求 `float32 mass` 和 `geometry_msgs/Vector3 center_of_gravity`，用于负载质量及相对法兰坐标系的重心；响应 `bool success`。通常按 kg 和 m 配置，ROS 层直接转交 SDK，不额外换算或校验范围。调用前需使用已确认的负载参数。

### Trigger 服务

均使用 `std_srvs/srv/Trigger`：空请求 `{}`，响应 `bool success`、`string message`。

```{list-table}
:header-rows: 1
:widths: 40 60

* - 后缀
  - 功能和条件
* - `resend_external_script`
  - 无头模式下重发外部控制脚本；返回成功不代表任务已进入 PLAYING
* - `hand_back_control`
  - 使外部控制程序交还控制，当前 ROS 运动可能终止
* - `zero_ftsensor`
  - 力/力矩传感器清零；实际能力取决于机器人配置
```

### 异步结果的限制

参数 `check_io_successfull_retries` 默认 10，每次等待间隔 50 ms，代码在重试计数大于上限后退出（默认约 0.55 s，不含调度延迟）。本版部分回调在等待超时后仍把非零等待标记转为 `true`，因此 `success=true` 不能单独证明底层命令完成。应用还需检查状态读回和日志，特别是 fake hardware 场景。控制器参数名的 `successfull` 拼写应按源码原样使用。

## 自由拖动

`/freedrive_controller/enable_freedrive` 为订阅接口，类型 `std_msgs/msg/Bool`，队列深度 10。只有控制器处于 active 时才处理开始/结束请求。

`data=true` 请求自由拖动，并应持续发送作为保活；`data=false` 请求结束。参数 `inactive_timeout` 默认 **1 s**，使用墙上时钟定时器，收到命令后重置；超时后请求退出自由拖动。该话题无完成响应。

开始前应退出相冲突的关节运动控制。结束时先发送 false，并确认机器人已退出拖动，再切换控制器；本版 `on_deactivate` 主要清理内部状态和定时器，不应将仅停用控制器视为已经完成底层退出命令。
