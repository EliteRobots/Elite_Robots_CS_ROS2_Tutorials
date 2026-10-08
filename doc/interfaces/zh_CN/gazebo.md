# Gazebo 仿真接口

## 独立控制入口

```bash
ros2 launch elite_robots_simulation_gz elite_sim_control.launch.py \
  cs_type:=cs66 initial_joint_controller:=joint_trajectory_controller \
  launch_rviz:=false
```

本版启动空场景 `empty.sdf`，生成实体 `cs`，用 Description 的 `sim_ignition=true` 选择 `ign_ros2_control/IgnitionSystem`。`robot_state_publisher` 使用仿真时间，默认加载 `joint_state_broadcaster` 和标准 `joint_trajectory_controller`。

Gazebo 的接口不经过机器人控制柜，不提供 `/dashboard_client/*`、`/primary_client/*` 或实体 GPIO 服务。控制器 YAML 中出现某个名称也不代表对应插件已加载。

## 控制器与时间

仿真 `controller_manager` 配置更新率 **500 Hz**；默认轨迹动作是 `/joint_trajectory_controller/follow_joint_trajectory`，类型与实体驱动相同。默认路径容差各关节 **0.2 rad**，目标容差 **0.1 rad**，停止速度容差 **0.2 rad/s**，`goal_time=0.0`。

ROS `/clock` 类型为 `rosgraph_msgs/msg/Clock`。本版 launch 没有启动时钟桥，先确认是否已有发布者和实际数据：

```bash
ros2 topic info /clock
ros2 topic echo /clock --once
```

若没有数据，在单独终端启动当前 Humble/Ignition 环境的单向桥：

```bash
ros2 run ros_gz_bridge parameter_bridge \
  '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock'
```

不同 Gazebo/ros_gz 安装版本可能使用 `gz.msgs.Clock` 类型名或 world 下的时钟话题，需按安装版本和仿真实际话题确认并调整映射。时钟停在零或暂停时，依赖仿真时间的规划、TF 和动作可能等待或超时。避免对同一时钟重复建立桥。

## 与 MoveIt 分步组合

在 Gazebo 控制已启动、时钟与关节状态已确认后，另开终端：

```bash
ros2 launch elite_robots_moveit_config elite_moveit.launch.py \
  cs_type:=cs66 use_sim_time:=true use_fake_hardware:=true \
  launch_servo:=false
```

此处 `use_fake_hardware=true` 用来选择标准轨迹控制器，Gazebo 仍是实际运动仿真来源。若使用 RViz，启动后为此节点设置同一时间源：

```bash
ros2 param set /rviz2_moveit use_sim_time true
```

本版同时提供 `elite_sim_moveit.launch.py`，但它引用的 `cs_moveit.launch.py` 在配套 MoveIt 包中不存在；实际文件名为 `elite_moveit.launch.py`。因此本文不将该组合入口作为可直接运行的流程。其声明参数仍列在[启动参数索引](launch_reference.md)，便于迁移或维护已有调用。

## 初始位置、五轴与前缀

`cs_type` 默认 `cs66`。`initial_positions_file` 留空时，普通型号使用 `initial_positions.yaml`，以 `a` 结尾的型号使用 `initial_positions_a_type.yaml`，以 `h` 结尾的型号使用 `initial_positions_h_type.yaml`。显式覆盖时传入 YAML 文件路径。

五轴默认使用 `urdf_5f` 与 `cs_controllers_5f.yaml`；必须发送五个关节的轨迹。六轴示例脚本不适用于五轴。

此 launch 的 `prefix` 被传给 Xacro，但模型入口接收的是 `tf_prefix`，控制器 YAML 也使用固定关节名。默认空前缀是本手册的示例条件，多机器人需自定义一致的模型、控制器和命名空间。

## gz_control.py 客户端

安装后的可执行名为 **`gz_control.py`**，节点名 `sdk_gz_bridge`。CMake 未将脚本重命名为 `gz_control`。

```bash
ros2 run elite_robots_simulation_gz gz_control.py --help
```

CLI 使用 argparse，不是 ROS `-p` 参数：

```{list-table}
:header-rows: 1
:widths: 40 60

* - 参数
  - 含义
* - `--controller NAME`
  - 默认 `joint_trajectory_controller`，组成绝对动作名 `/<NAME>/follow_joint_trajectory`
* - `--example`
  - 发送内置六轴轨迹，立即产生仿真运动
* - `--from-yaml PATH`
  - 读取轨迹点文件；与 example 同时指定时优先读取文件
```

YAML 为列表，每项 `positions` 必须有 6 个数，单位 rad；`duration` 为该段持续时间，单位 s，省略时取 3.0。程序累加每段 duration 得到 `time_from_start`。应用应保证各段时间为正，脚本没有充分验证所有轨迹合法性。

以下只展示数据格式，位置需替换为已检查的目标：

```yaml
- positions: [0.0, -1.57, 0.0, -1.57, 0.0, 0.0]
  duration: 3.0
- positions: [0.1, -1.57, 0.0, -1.57, 0.0, 0.0]
  duration: 2.0
```

发送到仿真控制器：

```bash
ros2 run elite_robots_simulation_gz gz_control.py \
  --from-yaml /tmp/waypoints.yaml
```

脚本最多等待动作服务器 10 s，然后等待目标接受和执行结果。进程返回码 0 表示结果 `error_code=0`，1 表示参数或文件解析错误，2 表示发送/执行失败。脚本固定使用无前缀的六轴关节名，未显式配置仿真时间，也不提供取消、五轴或多机器人命名配置；复杂应用应自行实现动作客户端。

## 本版非默认配置限制

仿真 YAML 中的 IO、速度缩放、力广播和缩放轨迹条目仍引用 `cs_controllers/...` 插件名，与 Driver 实际导出的插件名不一致。默认只启动关节状态和标准轨迹控制器，不应直接激活这些遗留条目。即使改名，仿真系统也不自动拥有实体硬件的 GPIO、速度缩放等资源。
