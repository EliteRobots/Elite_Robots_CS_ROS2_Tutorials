# MoveIt 2 与 Servo 接口

## 启动入口和职责

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 launch_servo:=false
```

此入口启动 `move_group`、可选 RViz 和可选 Servo；不启动实体驱动、Gazebo 或 ros2_control 管理器。使用轨迹执行前，先独立启动所选驱动，确保 `/joint_states`、TF 和目标动作服务器就绪。

默认规划组为 `cs_manipulator`，SRDF 链从 `base_link` 到 `tool0`；五轴选择相应 SRDF 和限制文件。规划算法配置使用 OMPL，机器人运动学配置来自 `kinematics.yaml`。

## 轨迹执行映射

默认 `controllers.yaml` 列出两个 `FollowJointTrajectory` 控制器，`action_ns` 均为 `follow_joint_trajectory`：

- `scaled_joint_trajectory_controller`：默认选中：true；动作目标：同名控制器下的轨迹动作。

- `joint_trajectory_controller`：默认选中：false；动作目标：同名控制器下的轨迹动作。


`use_fake_hardware:=true` 在本入口中只把默认执行控制器切换为标准 `joint_trajectory_controller`，不会创建 fake hardware。Gazebo 使用标准控制器时，也可利用这一选项选择正确的动作目标。

`moveit_manage_controllers=false`，所以 MoveIt 不负责加载或切换控制器。默认轨迹执行参数为：允许时长缩放 1.2、额外时间裕量 0.5 s、起始位置容差 0.01 rad。规划成功不等于可以执行；控制器名称、关节名和运行状态必须匹配。

## 标准 MoveIt ROS 接口

本包配置标准 MoveIt 节点，不定义新的规划消息。以下为默认能力常用接口，具体是否启用应以 `ros2 node info /move_group`、`ros2 action list -t` 和 `ros2 service list -t` 为准。

- `/move_action`：类型：`moveit_msgs/action/MoveGroup`；用途：输入运动规划请求和规划选项，返回轨迹与错误码。

- `/execute_trajectory`：类型：`moveit_msgs/action/ExecuteTrajectory`；用途：执行已有 RobotTrajectory，返回执行错误码。

- `/plan_kinematic_path`：类型：`moveit_msgs/srv/GetMotionPlan`；用途：仅计算运动规划。

- `/compute_ik`：类型：`moveit_msgs/srv/GetPositionIK`；用途：逆运动学。

- `/compute_fk`：类型：`moveit_msgs/srv/GetPositionFK`；用途：正运动学。

- `/compute_cartesian_path`：类型：`moveit_msgs/srv/GetCartesianPath`；用途：笛卡尔路径；检查返回完成比例 fraction 和错误码。

- `/get_planning_scene`：类型：`moveit_msgs/srv/GetPlanningScene`；用途：获取场景。

- `/apply_planning_scene`：类型：`moveit_msgs/srv/ApplyPlanningScene`；用途：更新场景。


MoveIt 动作使用 `moveit_msgs/msg/MoveItErrorCodes`，与底层 `FollowJointTrajectory.error_code` 是不同的错误码体系。客户端应分别解析，不要把同一个整数的含义跨接口复用。

场景输入/输出使用 `moveit_msgs/msg/PlanningScene`，轨迹显示使用 `moveit_msgs/msg/DisplayTrajectory`，具体话题由启动能力和命名空间确定。机器人描述发布由 `publish_robot_description` 和 `publish_robot_description_semantic` 控制，默认均为 true。

## Servo 配置接口

`launch_servo` 默认 true；无需实时 Servo 时可显式关闭。配置文件为 `config/cs_servo.yaml`，参数传入节点的 `moveit_servo` 命名空间。

```{list-table}
:header-rows: 1
:widths: 54 46

* - 配置项
  - 默认值与含义
* - `command_in_type`
  - `speed_units`，输入使用物理速度单位
* - `cartesian_command_in_topic`
  - `~/delta_twist_cmds`，`geometry_msgs/msg/TwistStamped`；线速度 m/s、角速度 rad/s
* - `joint_command_in_topic`
  - `~/delta_joint_cmds`，`control_msgs/msg/JointJog`；关节速度 rad/s
* - `joint_topic`
  - `/joint_states`
* - `status_topic`
  - `~/status`，Servo 状态；按所装 MoveIt 版本解释状态码
* - `command_out_topic`
  - `/forward_position_controller/commands`
* - `command_out_type`
  - `std_msgs/Float64MultiArray`，只发布位置
* - `move_group_name`
  - `cs_manipulator`
* - `planning_frame`
  - `base_link`
* - `ee_frame_name`、`robot_link_command_frame`
  - `tool0`
* - `publish_period`
  - 0.004 s，配置目标 250 Hz
* - `incoming_command_timeout`
  - 0.1 s，输入命令超时停止 Servo 输出运动
* - `num_outgoing_halt_msgs_to_publish`
  - 4，停止时重复发送次数
* - `check_collisions`、`collision_check_rate`
  - true、5 Hz
```

`~/` 按 Servo 实际节点名解析，不要按可执行文件名猜测。启动后查询该节点接口及所装版本的启动/暂停服务，并确保 `forward_position_controller` 已激活且无其他控制器争用关节资源。默认驱动只是把它加载为 inactive，启动 Servo 不会自动激活它。

输入应包含有效的时间戳和坐标系，持续发送间隔应小于 0.1 s；不要同时让两个输入源争夺控制。`scale.linear/rotational/joint` 只在 `unitless` 模式使用，当前 `speed_units` 模式不采用这些比例。

## 前缀与仿真时钟限制

本版 MoveIt launch 向 URDF 传入 `prefix`，而 Description URDF 入口使用 `tf_prefix`；SRDF 则使用 `prefix`。默认空前缀可保持一致，非空前缀可能导致 SRDF 与 URDF 名称不匹配。控制器和 Servo YAML 也含未加前缀的固定名称。多机器人集成应提供一致的自定义模型/配置及 launch，不能仅设置 `prefix`。

`use_sim_time` 只传给 `move_group`，没有同时传给此 launch 中的 RViz、Servo。仿真集成应保证参与时间戳处理的节点都使用 `/clock`；默认示例关闭 Servo，按需为 RViz 设置仿真时间。`moveit_config_package` 也不是所有配置的统一替换开关：OMPL 和 Servo YAML 仍固定从 `elite_robots_moveit_config` 读取。
