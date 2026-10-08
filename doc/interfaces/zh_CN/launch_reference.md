# 启动参数索引

本章列出本版入口声明的全部 launch 参数。通过 `名称:=值` 传入；必填表示入口没有默认值。空字符串与布尔字符串会在 launch/Xacro 中继续解析，不代表对应 ROS 节点参数具有相同类型。参数应在启动时确定，不承诺热更新。

## 模型展示

入口：`view_cs.launch.py`。

- `cs_type`：默认 **必填**。型号字符串；各入口允许值见后文。
  允许值：`cs63`、`cs63a`、`cs66`、`cs66a`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs630`、`cs520h`、`ls65`。
- `safety_limits`：默认 `true`。启用模型中的安全限制元素。
- `safety_pos_margin`：默认 `0.15`。关节安全位置裕量，rad。
- `safety_k_position`：默认 `20`。安全限制位置系数。
- `description_package`：默认 `elite_robots_description`。提供模型描述的包。
- `description_file`：默认 `cs.urdf.xacro`。模型 Xacro 文件名。
- `tf_prefix`：默认 空字符串。关节、连杆和硬件资源名的前缀。

## 驱动控制

入口：`elite_control.launch.py`。

- `cs_type`：默认 **必填**。型号字符串；各入口允许值见后文。
  允许值：`cs63`、`cs66`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs66a`、`cs520h`、`ls65`。
- `robot_ip`：默认 **必填**。机器人或 ELIBOTSim 控制器地址。
- `local_ip`：默认 `0.0.0.0`。ROS 计算机供控制器回连的地址。
- `safety_limits`：默认 `true`。启用模型中的安全限制元素。
- `safety_pos_margin`：默认 `0.15`。关节安全位置裕量，rad。
- `safety_k_position`：默认 `20`。安全限制位置系数。
- `runtime_config_package`：默认 `elite_robots_driver`。提供 config 目录的控制器配置包。
- `controllers_file`：默认 `elite_cs_controllers.yaml`。上述包内 config 目录下的控制器 YAML 文件名。
- `description_package`：默认 `elite_robots_description`。提供模型描述的包。
- `description_file`：默认 `cs.urdf.xacro`。模型 Xacro 文件名。
- `tf_prefix`：默认 空字符串。关节、连杆和硬件资源名的前缀。
- `use_fake_hardware`：默认 `false`。驱动入口中切换 GenericSystem；MoveIt 入口中仅切换默认轨迹控制器。
- `fake_sensor_commands`：默认 `false`。fake hardware 的传感器命令开关。
- `headless_mode`：默认 `false`。直接发送外部控制脚本。
- `controller_spawner_timeout`：默认 `10`。等待控制器管理器的超时，s。
- `initial_joint_controller`：默认 `scaled_joint_trajectory_controller`。初始加载的关节控制器名。
- `activate_joint_controller`：默认 `true`。驱动入口是否激活初始关节控制器。
- `launch_rviz`：默认 `true`。是否启动 RViz。
- `tool_voltage`：默认 `0`。传入模型的初始工具电压；本版初始化未实际应用。
- `script_command_port`：默认 `50004`。ROS 计算机侧脚本命令端口。
- `reverse_port`：默认 `50001`。ROS 计算机侧周期控制端口。
- `script_sender_port`：默认 `50002`。ExternalControl 脚本服务端口。
- `trajectory_port`：默认 `50003`。ROS 计算机侧轨迹端口。

## MoveIt

入口：`elite_moveit.launch.py`。

- `cs_type`：默认 **必填**。型号字符串；各入口允许值见后文。
  允许值：`cs63`、`cs66`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs66a`、`cs520h`、`ls65`。
- `use_fake_hardware`：默认 `false`。驱动入口中切换 GenericSystem；MoveIt 入口中仅切换默认轨迹控制器。
- `safety_limits`：默认 `true`。启用模型中的安全限制元素。
- `safety_pos_margin`：默认 `0.15`。关节安全位置裕量，rad。
- `safety_k_position`：默认 `20`。安全限制位置系数。
- `description_package`：默认 `elite_robots_description`。提供模型描述的包。
- `description_file`：默认 `cs.urdf.xacro`。模型 Xacro 文件名。
- `moveit_config_package`：默认 `elite_robots_moveit_config`。提供 SRDF、关节限制和控制器文件的包；部分其他 YAML 仍固定取自默认包。
- `moveit_config_file`：默认 `cs.srdf.xacro`。SRDF Xacro 文件名。
- `moveit_joint_limits_file`：默认 `joint_limits.yaml`。MoveIt 关节限制 YAML 文件名。
- `moveit_controllers_file`：默认 `controllers.yaml`。MoveIt 动作控制器映射 YAML 文件名。
- `warehouse_sqlite_path`：默认 `~/.ros/warehouse_ros.sqlite`（展开当前用户目录）。MoveIt warehouse SQLite 文件路径。
- `use_sim_time`：默认 `false`。是否让 move_group 使用 /clock；本版未同步传给 Servo 与 RViz。
- `prefix`：默认 空字符串。传给下游模型/SRDF 的前缀；本版存在传递不一致，见 MoveIt/Gazebo 章节。
- `launch_rviz`：默认 `true`。是否启动 RViz。
- `launch_servo`：默认 `true`。是否启动 MoveIt Servo 节点。
- `publish_robot_description`：默认 `true`。是否让 MoveIt 发布机器人描述。
- `publish_robot_description_semantic`：默认 `true`。是否让 MoveIt 发布语义描述。

## Gazebo 控制

入口：`elite_sim_control.launch.py`。

- `cs_type`：默认 `cs66`。型号字符串；各入口允许值见后文。
  允许值：`cs63`、`cs66`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs66a`、`cs68`、`cs520h`、`ls65`。
- `safety_limits`：默认 `true`。启用模型中的安全限制元素。
- `safety_pos_margin`：默认 `0.15`。关节安全位置裕量，rad。
- `safety_k_position`：默认 `20`。安全限制位置系数。
- `runtime_config_package`：默认 `elite_robots_simulation_gz`。提供 config 目录的控制器配置包。
- `controllers_file`：默认 `cs_controllers.yaml`。上述包内 config 目录下的控制器 YAML 文件名。
- `description_package`：默认 `elite_robots_description`。提供模型描述的包。
- `description_file`：默认 `cs.urdf.xacro`。模型 Xacro 文件名。
- `initial_positions_file`：默认 空字符串。仿真初始位置 YAML；空值时按型号选择。
- `prefix`：默认 空字符串。传给下游模型/SRDF 的前缀；本版存在传递不一致，见 MoveIt/Gazebo 章节。
- `start_joint_controller`：默认 `true`。仿真入口是否启动初始关节控制器，不是无头模式。
- `initial_joint_controller`：默认 `joint_trajectory_controller`。初始加载的关节控制器名。
- `launch_rviz`：默认 `true`。是否启动 RViz。

## Gazebo 与 MoveIt 组合

入口：`elite_sim_moveit.launch.py`。

- `cs_type`：默认 `cs66`。型号字符串；各入口允许值见后文。
  允许值：`cs63`、`cs66`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs66a`、`cs68`、`cs520h`、`ls65`。
- `safety_limits`：默认 `true`。启用模型中的安全限制元素。
- `runtime_config_package`：默认 `elite_robots_simulation_gz`。提供 config 目录的控制器配置包。
- `controllers_file`：默认 `cs_controllers.yaml`。上述包内 config 目录下的控制器 YAML 文件名。
- `description_package`：默认 `elite_robots_description`。提供模型描述的包。
- `description_file`：默认 `cs.urdf.xacro`。模型 Xacro 文件名。
- `moveit_config_package`：默认 `elite_robots_moveit_config`。提供 SRDF、关节限制和控制器文件的包；部分其他 YAML 仍固定取自默认包。
- `moveit_config_file`：默认 `cs.srdf.xacro`。SRDF Xacro 文件名。
- `moveit_joint_limits_file`：默认 `joint_limits.yaml`。MoveIt 关节限制 YAML 文件名。
- `moveit_controllers_file`：默认 `controllers.yaml`。MoveIt 动作控制器映射 YAML 文件名。
- `prefix`：默认 空字符串。传给下游模型/SRDF 的前缀；本版存在传递不一致，见 MoveIt/Gazebo 章节。

## 校准

入口：`calibration_correction.launch.py`。

- `robot_ip`：默认 **必填**。机器人或 ELIBOTSim 控制器地址。
- `target_filename`：默认 `robot_calibration.yaml`。校准输出文件；映射为节点参数 output_filename。

## 单目标运动示例

入口：`example_safe_joint_move.launch.py`。

- `cpp_py`：默认 `cpp`。示例实现选择，cpp 或 py。
- `target`：默认 **必填**。目标关节数组，rad。
- `max_vel`：默认 `0.5`。用于估算轨迹时长的速度，rad/s。
- `min_time`：默认 `20.0`。轨迹最短时长，s。
- `controller`：默认 `scaled_joint_trajectory_controller`。示例动作目标控制器名。

## 标准轨迹循环示例

入口：`example_joint_trajectory_controller.launch.py`。

- `robot_model`：默认 空字符串。示例配置选择；cs66a 使用专用 YAML，其他值使用普通配置。

## 缩放轨迹循环示例

入口：`example_scaled_joint_trajectory_controller.launch.py`。

- `robot_model`：默认 空字符串。示例配置选择；cs66a 使用专用 YAML，其他值使用普通配置。

## 默认文件的条件替换

- Driver 型号以 h 结尾时，默认控制器文件改为 `elite_cs_controllers_5f.yaml`，默认模型切换到 `urdf_5f`。
- MoveIt 同时将默认 SRDF、关节限制和控制器配置切换到 `cs_5f.srdf.xacro`、`joint_limits_5f.yaml`、`controllers_5f.yaml`。
- Gazebo 使用 `cs_controllers_5f.yaml` 和五轴模型；空初始位置路径会按 h/a/普通型号选择相应文件。
- 条件替换通常只针对默认文件名。传入自定义文件名时，应自行提供一致的轴数、关节名、模型及控制器配置。

## 无声明参数的示例入口

`example_forward_velocity_controller.launch.py` 不声明用户 launch 参数，启动标准测试发布器并加载包内测试 YAML。它不是速度控制器的加载入口，也不包含实际控制器切换。循环轨迹示例同样应在目标控制器就绪后使用，不宜作为通用应用客户端。
