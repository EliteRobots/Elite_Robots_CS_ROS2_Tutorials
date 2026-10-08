# 驱动、硬件与校准接口

## 驱动启动

每个终端先加载环境，工作空间路径以实际安装位置为准：

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
```

实体机器人或 ELIBOTSim 使用相同入口，替换型号与地址后运行：

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  cs_type:=cs66 robot_ip:=<robot_ip> local_ip:=<local_ip> \
  headless_mode:=true launch_rviz:=false
```

无头模式直接发送外部控制脚本。机器人启用远程控制功能时应处于远程模式，并满足启动任务的机器人状态条件。非无头模式需在示教器的 ExternalControl 任务中配置 ROS 计算机地址及脚本端口，并启动该任务。脚本发送、脚本运行、轨迹控制器激活是三个不同状态。

fake hardware 可用以下配置进行关节接口集成；`robot_ip` 在 launch 中仍是必填参数，但此模式不建立真实机器人连接：

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  cs_type:=cs66 robot_ip:=0.0.0.0 use_fake_hardware:=true \
  initial_joint_controller:=joint_trajectory_controller
```

fake hardware 不等同于完整控制柜模拟器；本版 launch 仍尝试启动 IO 等广播器，不能据此宣称其服务具有真实语义。

## 节点与可执行程序

所有下列程序均来自 `elite_robots_driver`。

```{list-table}
:header-rows: 1
:widths: 45 55

* - 可执行名
  - 节点/职责
* - `eli_ros2_control_node`
  - 实体驱动使用的控制器管理器进程
* - `eli_components_loader`
  - 在同一执行器中加载 Dashboard、Primary 和脚本节点
* - `dashboard_client`
  - 独立 Dashboard 组件入口；节点名 `dashboard_client`
* - `primary_client`
  - 独立 Primary 组件入口；节点名 `primary_client`
* - `script_node`
  - 脚本组件入口；节点名是 `script_sender`
* - `controller_stopper_node`
  - 根据任务状态停止/恢复运动控制器；launch 中命名为 `controller_stopper`
* - `example_safe_joint_move`
  - C++ 单目标关节轨迹示例
* - `example_safe_joint_move_py`
  - Python 单目标关节轨迹示例
```

`use_fake_hardware:=true` 时改用标准 `controller_manager/ros2_control_node`，不加载组件进程和 controller stopper。

组件进程仅在 Dashboard 初次连接成功时保留其节点。失败后 `/dashboard_client/*` 服务可能完全不存在，不能依靠该进程中的 `/dashboard_client/connect` 恢复已被移除的节点。排除网络问题后重启组件进程，或在避免重复节点的前提下使用独立入口。

controller stopper 订阅 `io_and_status_controller/robot_task_running`，调用管理器的 `list_controllers`、`switch_controller` 以及 Dashboard 的 `robot_mode`。任务停止时保留默认五个状态广播/IO 控制器，停用其他活动控制器；任务恢复时尝试恢复此前停止的控制器。Dashboard 缺失时它会等待对应服务，因此不可仅凭此节点存在判断控制器保护逻辑已就绪。

## 参数层次

`elite_control.launch.py` 的完整参数见[启动参数索引](launch_reference.md)。launch 将参数写入 Xacro，再由 `<ros2_control><hardware>` 传给硬件插件。以下参数不是可直接通过 `ros2 param set` 热更新的普通节点参数。

硬件插件名：`ELITE_CS_ROBOT_ROS_DRIVER/EliteCSPositionHardwareInterface`。

- `robot_ip`：默认/来源：launch 必填；用途：控制器地址。

- `local_ip`：默认/来源：`0.0.0.0`；用途：ROS 计算机回连地址；驱动将此默认值转换为空字符串交给 SDK 自动选择。

- `headless_mode`：默认/来源：`false`；用途：是否直接发送外部控制脚本。

- `reverse_port`：默认/来源：`50001`；用途：ROS 计算机侧周期控制通信端口。

- `script_sender_port`：默认/来源：`50002`；用途：向 ExternalControl 提供脚本的端口。

- `trajectory_port`：默认/来源：`50003`；用途：ROS 计算机侧轨迹通信端口。

- `script_command_port`：默认/来源：`50004`；用途：ROS 计算机侧脚本命令通信端口。

- `script_filename`：默认/来源：驱动 `resources/external_control.script`；用途：外部控制脚本路径。

- `input_recipe_filename`：默认/来源：驱动 `resources/input_recipe.txt`；用途：RTSI 输入配方路径。

- `output_recipe_filename`：默认/来源：驱动 `resources/output_recipe.txt`；用途：RTSI 输出配方路径。

- `servoj_gain`：默认/来源：`1000`；用途：传给 SDK 的伺服增益。

- `servoj_lookahead_time`：默认/来源：`0.03` s；用途：伺服前瞻时间。

- `servoj_time`：默认/来源：`0.008` s；用途：伺服周期参数。

- `robot_receive_timeout`：默认/来源：`0.2` s；用途：机器人接收超时，写指令时换算为 ms。


后三个 servoj 参数及接收超时由描述宏提供，本版顶层驱动 launch 没有对应覆盖项。需要修改时应通过自定义描述文件集成，不能在 launch 命令后追加同名参数就认为已经生效。

`tool_voltage` 默认 0，并被传入模型，但本版硬件初始化未读取该参数来设置工具电压；需要设置时使用 GPIO 的 `set_io` 服务并检查结果。`use_tool_communication`、`tool_parity`、`tool_baud_rate`、`tool_stop_bits`、`tool_tcp_port` 虽在 Xacro 中声明，不构成本版已实现的 ROS 工具串口转发接口。

## ros2_control 资源

每个关节导出 `position`、`velocity`、`effort` 状态接口和 `position`、`velocity` 命令接口。位置/速度控制不能同时占用同一组关节资源。

```{important}
本版硬件将实际关节电流写入 `effort` 状态接口。因此真实驱动的 `/joint_states.effort` 不能按关节力矩 N·m 解释，也不能据此直接计算负载。仿真与其他硬件插件的同名字段语义可能不同。
```

其他资源均在名称前加入 `tf_prefix`：

```{list-table}
:header-rows: 1
:widths: 40 60

* - 资源组
  - 状态或命令
* - `speed_scaling`
  - `speed_scaling_factor` 状态；`target_speed_fraction_cmd` 命令
* - `tcp_fts_sensor`
  - `force.x/y/z`、`torque.x/y/z` 状态
* - `tcp_pose`
  - `position.x/y/z`、`orientation.x/y/z/w` 状态
* - `gpio`
  - 数字/模拟 IO、工具数据、机器人/安全模式、任务状态；IO 和工具电压命令
* - `payload`
  - `mass`、`cog.x/y/z` 命令
* - `resend_external_script`
  - 外部控制脚本重发命令
* - `hand_back_control`
  - 交还控制命令
* - `zero_ftsensor`
  - 力传感器清零命令
* - `freedrive_mode`
  - 自由拖动开始、结束命令
* - `system_interface`
  - `initialized` 状态
```

异步命令还包含对应成功反馈资源。这些资源由控制器封装为 ROS 服务；应用优先使用[控制器接口](controllers.md)。可用 `ros2 control list_hardware_interfaces` 查看当前实例完整的资源名和占用状态。

## 校准工具

```bash
ros2 launch elite_robots_calibration calibration_correction.launch.py \
  robot_ip:=<robot_ip> target_filename:=/tmp/robot_calibration.yaml
```

此命令连接机器人读取运动学信息并写入本地文件，不发送运动指令；本文未执行。可执行名是 `calibration_correction`，节点名为 `cs_calibration`。launch 的 `target_filename` 映射为节点参数 `output_filename`，默认 `robot_calibration.yaml`，相对路径相对于进程工作目录。

输出父目录必须存在；同名文件会被覆盖。该程序执行一次后退出，没有供应用持续调用的业务服务或话题。输出 YAML 不会自动替换驱动模型；需在自定义描述中将 `kinematics_params` 指向校准结果，并让驱动、TF 与 MoveIt 使用一致的模型。本版驱动 launch 没有单独的校准文件参数。
