# 机器人描述接口

## 模型展示入口

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs66
```

该入口启动 `joint_state_publisher_gui`、`robot_state_publisher` 和 RViz，用于模型展示。GUI 生成 `/joint_states`；它不连接机器人，也不发送真实运动指令。不要在实体驱动已发布同名关节状态的 ROS 图中再启动此 GUI。

展示入口接受：`cs63`、`cs63a`、`cs66`、`cs66a`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs630`、`cs520h`、`ls65`。

Driver、MoveIt、Gazebo 的本版入口不接受 `cs63a`、`cs630`；模型文件存在不表示所有入口均已支持。没有 `es*` 启动选项，不能自行将 ES 型号映射为某个 CS 型号。

## 关节和坐标系

六轴控制器的关节顺序为：

```text
shoulder_pan_joint
shoulder_lift_joint
elbow_joint
wrist_1_joint
wrist_2_joint
wrist_3_joint
```

五轴 `cs520h` 使用前五项，没有 `wrist_3_joint`。launch 通过型号是否以 `h` 结尾选择五轴文件。若使用非默认自定义文件，需自行保证轴数和名称一致。

常用坐标系：`world` 为模型根，`base_link` 为模型基座，`base` 为控制器基座参考，`flange` 为法兰，`tool0` 为模型工具参考。`base` 与 `base_link` 之间存在固定变换，不能仅因两者均表示基座就互换数值。驱动另提供控制器反馈的 `tool0_controller`；它与模型计算得到的 `tool0` 来源不同。

`tf_prefix:=robot1_` 直接生成 `robot1_shoulder_pan_joint`、`robot1_base_link` 等名称；下划线不会自动添加。

## Xacro 和配置文件

六轴入口为包共享目录下 `urdf/cs.urdf.xacro`，五轴入口为 `urdf_5f/cs.urdf.xacro`。主要参数如下；它们不一定被每个 launch 暴露。

```{list-table}
:header-rows: 1
:widths: 40 60

* - Xacro 参数
  - 含义
* - `name`、`cs_type`
  - 机器人名称与配置型号
* - `tf_prefix`
  - 关节、连杆、硬件资源前缀
* - `joint_limit_params`
  - 关节位置、速度等限制 YAML
* - `kinematics_params`
  - 运动学 YAML，可用于集成校准结果
* - `physical_params`、`visual_params`
  - 惯量等物理参数、网格与外观参数
* - `safety_limits`
  - 写入 URDF safety controller 元素；不代替控制柜安全功能
* - `safety_pos_margin`、`safety_k_position`
  - 安全位置裕量和位置系数，默认 0.15、20
* - `use_fake_hardware`
  - 使用 GenericSystem
* - `fake_sensor_commands`
  - fake hardware 的传感器命令开关
* - `sim_gazebo`、`sim_ignition`
  - 选择相应 Gazebo 系统插件
* - `simulation_controllers`
  - 仿真控制器 YAML 路径
* - `initial_positions_file`
  - 仿真初始关节位置 YAML 路径
```

直接调用六轴 Xacro 时，`cs_type` 默认是 `cs63`，`safety_limits` 默认是 `false`；通过 launch 时应遵守该入口的必填项及默认值，不能把 Xacro 默认值当成 launch 默认值。

`config/<cs_type>/` 下包含 `joint_limits.yaml`、`default_kinematics.yaml`、`physical_parameters.yaml` 和 `visual_parameters.yaml`。Gazebo 默认按型号选择普通、`a` 型或 `h` 型初始位置文件。

## ROS 侧模型接口

`robot_description` 是传给 `robot_state_publisher`、控制器管理器或 MoveIt 节点的 URDF 字符串参数。`/joint_states` 使用 `sensor_msgs/msg/JointState`；`/tf`、`/tf_static` 使用 `tf2_msgs/msg/TFMessage`，分别表示动态和静态坐标变换。

这些接口由 ROS 标准节点提供。以 `ros2 node info /robot_state_publisher` 核对当前安装版本的实际发布和订阅；不要把展示节点的关节状态当作硬件反馈。
