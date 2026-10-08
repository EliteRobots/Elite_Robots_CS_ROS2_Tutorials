# 软件包与接口约定

## 软件包组成

Description 仓库提供 `elite_robots_description`，负责 URDF/Xacro、网格、关节限制、模型参数和 RViz 展示，无自定义 ROS 消息或硬件控制节点。

Driver 仓库包含以下七个包，版本均为 1.0.3：

```{list-table}
:header-rows: 1
:widths: 48 52

* - ROS 包
  - 职责
* - `elite_robots`
  - 依赖聚合包，无独立业务接口。
* - `elite_robots_driver`
  - ros2_control 硬件插件、管理服务、脚本发送、启动和示例程序。
* - `elite_robots_controllers`
  - IO、速度缩放、缩放轨迹与自由拖动控制器插件。
* - `elite_robots_msgs`
  - 机器人状态消息、IO、负载和状态查询服务类型。
* - `elite_robots_dashboard_msgs`
  - Dashboard 文件、弹窗、日志和自定义命令服务类型。
* - `elite_robots_moveit_config`
  - SRDF、规划、轨迹执行和 Servo 配置。
* - `elite_robots_calibration`
  - 从机器人读取运动学数据并输出校准 YAML 的一次性工具。
```

GZ Simulation 仓库提供 `elite_robots_simulation_gz`，包含 Gazebo 启动、仿真控制器配置和轨迹客户端。它不定义新的消息、服务或动作。

## 接口分层

应用通过 ROS 话题、服务或动作与节点通信；运动控制器通过 ros2_control 的 command/state interface 访问硬件；硬件插件再通过 SDK 与机器人通信。诸如 `gpio/tool_voltage_cmd` 的硬件接口名不是 ROS 话题，不能用 `ros2 topic pub` 直接写入。

Description 生成 `robot_description`；`robot_state_publisher` 将关节状态转换为 TF。MoveIt 读取机器人模型和 `/joint_states`，规划后向轨迹控制器发送动作。Gazebo 用仿真系统插件替代实体硬件插件。

## 名称、方向和命名空间

本文默认没有 ROS 命名空间、没有关节前缀，使用默认节点和控制器名称。发布/订阅方向均相对于提供接口的节点。

- `~/set_io` 是节点私有名称；GPIO 控制器名为 `io_and_status_controller` 时解析为 `/io_and_status_controller/set_io`。
- `~/robot_mode` 在 Dashboard 节点中解析为 `/dashboard_client/robot_mode`，是服务；在 GPIO 控制器中解析为 `/io_and_status_controller/robot_mode`，是话题。
- `tf_prefix` 用于关节、连杆和硬件资源名，不会自动添加 ROS 命名空间。MoveIt/Gazebo launch 的参数名为 `prefix`，存在与模型参数不一致的限制，见对应章节。
- 默认 launch 的 spawner 使用绝对名称 `/controller_manager`。多机器人部署需同时调整管理器名称、ROS 命名空间、关节名、控制器配置和各客户端目标；只设置前缀不足以完成隔离。

## 单位与返回值

关节位置使用 rad，关节速度使用 rad/s，时间使用 s；笛卡尔位置一般使用 m，姿态四元数无量纲。特殊单位在各接口中明确列出。

速度滑块服务接收比例，例如 `0.5` 表示 50%；速度缩放广播话题输出百分数，例如 `50.0`。本版服务实现只接受 **0.01～1.0**，不是类型注释所写的 0～1。

ROS 服务调用成功只说明收到了响应；还必须检查 `success` 等业务字段。动作还应区分目标是否被接受、最终动作状态和结果 `error_code`。脚本话题无结果响应，发布成功不能作为脚本执行成功的依据。

## 运行场景

- 实体机器人：控制端：Elite 硬件插件；地址和时间：机器人地址；系统时间；可用接口：轨迹、状态、IO、管理服务，取决于连接与激活状态。

- ELIBOTSim：控制端：Elite 硬件插件；地址和时间：模拟控制器地址；系统时间；可用接口：同一驱动接口，实际能力受模拟控制器限制。

- fake hardware：控制端：GenericSystem；地址和时间：不连接机器人；系统时间；可用接口：用于关节命令回显；不保证真实 IO/管理行为。

- Gazebo：控制端：IgnitionSystem；地址和时间：无机器人 IP；仿真时间；可用接口：默认关节状态与标准轨迹控制，不提供 Dashboard/Primary。


实体机器人与 ELIBOTSim 中，`robot_ip` 是控制器地址；`local_ip` 是运行 ROS 驱动的计算机上可被控制器访问的地址。Gazebo 不需要这两个地址。
