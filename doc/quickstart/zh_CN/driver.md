# 驱动入门

## 启动与连接

先完成[网络配置或 ELIBOTSim 启动](robot_setup.md)，并确认每个操作终端已加载与安装方式对应的环境。

apt 安装只需加载 ROS 2 环境；源码安装还需加载对应工作空间。若已按安装章节将所需 `source` 命令加入 `~/.bashrc`，新开的 Bash 终端会自动加载，无需重复执行。未自动加载或在配置 `.bashrc` 前已经打开的终端，请按{ref}`终端环境加载说明 <terminal-environment>`手动加载。

### 启动驱动

```bash
ros2 launch elite_robots_driver elite_control.launch.py robot_ip:=<robot_ip> cs_type:=<cs_type> headless_mode:=true
```

- `robot_ip`：实体机器人或 ELIBOTSim 容器的可达 IP。
- `cs_type`：实际机器人型号，例如 `cs66`。
- `headless_mode`：是否启用无头模式，启用后由驱动下发外部控制脚本，无需在示教器上手动添加外部控制节点。
- `local_ip`：可选的 ROS 计算机地址，必须能被机器人访问；默认 `0.0.0.0` 表示自动选择连接机器人所用的本机地址。多网卡或虚拟机环境可追加 `local_ip:=<local_ip>` 显式指定。

收到机器人状态后，RViz 中的机器人姿态应与示教器一致。能够显示姿态不代表已经可以执行运动；还需完成下面的上电、释放抱闸和外部控制脚本启动。

```{figure} images/fig-4-1-rviz.png
:name: fig-4-1-rviz
:alt: RViz 显示姿态
:width: 90%
:align: center

RViz 显示姿态
```

```{figure} images/fig-4-2-pendant.png
:name: fig-4-2-pendant
:alt: 示教器中机器人姿态
:width: 90%
:align: center

示教器中机器人姿态
```

## 服务调用示例

执行服务调用时，应保持驱动节点运行，并另开已加载环境的终端。上电、释放抱闸等服务用于切换机器人状态，不要求提前通过示教器完成同一操作。

### 取得机器人控制权

**打开电源：**

```bash
ros2 service call /dashboard_client/power_on std_srvs/srv/Trigger "{}"
```

执行成功将输出如下内容：
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

机器人状态将由关机切换为待机。

```{figure} images/fig-4-3-standby.png
:name: fig-4-3-standby
:alt: 转为待机
:width: 90%
:align: center

转为待机
```

**释放抱闸：**

```bash
ros2 service call /dashboard_client/brake_release std_srvs/srv/Trigger "{}"
```

执行成功将输出如下内容：
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

机器人状态将变为正常模式。
```{figure} images/fig-4-4-normal-mode.png
:name: fig-4-4-normal-mode
:alt: 转为正常模式
:width: 90%
:align: center

转为正常模式
```

**启动外部控制脚本：**

以下操作适用于本章启用的无头模式。该服务会停止当前任务，再重新下发外部控制脚本。

```bash
ros2 service call /io_and_status_controller/resend_external_script std_srvs/srv/Trigger "{}"
```

执行成功将输出如下内容：
```
requester: making request: std_srvs.srv.Trigger_Request()

response:
std_srvs.srv.Trigger_Response(success=True, message='')
```

服务返回成功表示脚本已发送；随后应确认示教器进入“运行中”，并通过下面的任务状态查询确认脚本正在执行。
```{figure} images/fig-4-5-running-mode.png
:name: fig-4-5-running-mode
:alt: 转为运行中
:width: 90%
:align: center

转为运行中
```


**查询当前任务状态：**

```bash
ros2 service call /dashboard_client/get_task_status elite_robots_msgs/srv/GetTaskStatus "{}"
```

执行成功将输出如下内容：
```
requester: making request: elite_robots_msgs.srv.GetTaskStatus_Request()

response:
elite_robots_msgs.srv.GetTaskStatus_Response(success=True, message='', status=elite_robots_msgs.msg.TaskStatus(status=2))
```

```{note}
1. `status=2` 表示任务正在执行（`PLAYING`）；`0` 表示停止，`1` 表示暂停。驱动控制运动依赖外部控制脚本持续运行。
2. 若日志出现 `Socket timed out waiting for command on reverse_socket`，表示脚本等待控制指令超时。当前机器人描述中的 `robot_receive_timeout` 默认值为 0.2 s（200 ms），实际以硬件配置为准。检查 ROS 计算机负载、调度延迟和网络连接，必要时使用实时内核。
3. 如果找不到 `/dashboard_client/` 下的服务，检查驱动启动日志及 Dashboard 网络连接；Dashboard 连接失败时该节点不会加载。
```

```{figure} images/fig-4-6-control-timeout.png
:name: fig-4-6-control-timeout
:alt: 超时接收
:width: 90%
:align: center

超时接收
```

## 控制器与关节轨迹

`ros2_control` 管理机器人硬件与控制器。

```{list-table}
:header-rows: 1
:widths: 52 48

* - 控制器 / 广播器
  - 作用
* - `joint_state_broadcaster`
  - 发布关节状态
* - `io_and_status_controller`
  - 提供 IO、机器人状态及外部控制脚本服务
* - `speed_scaling_state_broadcaster`
  - 将速度缩放发布到 `~/speed_scaling` 话题，单位为百分比（0～100）
* - `scaled_joint_trajectory_controller`
  - 根据机器人速度缩放调整轨迹执行进度
* - `forward_position_controller`
  - 直接接收关节位置命令，默认不激活
* - `freedrive_controller`
  - 提供自由拖动控制，默认不激活
* - `tcp_pose_broadcaster`
  - 发布 TCP 位姿
* - `force_torque_sensor_broadcaster`
  - 发布力 / 力矩数据
```

上述名称对应默认配置。速度缩放话题的完整名称为 `/speed_scaling_state_broadcaster/speed_scaling`，类型为 `std_msgs/msg/Float64`；硬件内部缩放值为 0～1，广播时转换为百分比。

```{warning}
执行以下轨迹或程序示例前，应确保驱动正在运行、机器人处于运行模式，并确认周围环境安全。示例会使机器人移动。
```

### 查看控制器状态

```bash
ros2 control list_controllers
```

执行成功将输出如下内容：
```
speed_scaling_state_broadcaster    elite_robots_controllers/SpeedScalingStateBroadcaster         active
tcp_pose_broadcaster               pose_broadcaster/PoseBroadcaster                              active
joint_state_broadcaster            joint_state_broadcaster/JointStateBroadcaster                 active
forward_position_controller        position_controllers/JointGroupPositionController             inactive
scaled_joint_trajectory_controller elite_robots_controllers/ScaledJointTrajectoryController      active
io_and_status_controller           elite_robots_controllers/GPIOController                       active
freedrive_controller               elite_robots_controllers/FreedriveController                  inactive
force_torque_sensor_broadcaster    force_torque_sensor_broadcaster/ForceTorqueSensorBroadcaster  active
```

### 通过话题发送轨迹

以下示例向轨迹控制器发布一次消息，目标角度单位为 rad，时间单位为 s。话题、动作及后续程序示例均以 CS66 等六轴机器人且未设置关节名前缀为前提。CS520H 为五轴型号，不能直接使用这些六关节示例；设置了前缀时也需同步修改关节名。

```bash
ros2 topic pub --once \
  /scaled_joint_trajectory_controller/joint_trajectory \
  trajectory_msgs/msg/JointTrajectory "
joint_names:
  - shoulder_pan_joint
  - shoulder_lift_joint
  - elbow_joint
  - wrist_1_joint
  - wrist_2_joint
  - wrist_3_joint
points:
  - positions: [0.0, -1.0, 1.0, -1.5, 1.5, 0.0]
    time_from_start: {sec: 2}
"
```

如果成功，机械臂将运动至关节角度为`[0.0, -1.0, 1.0, -1.5, 1.5, 0.0]`处。

### 通过动作发送轨迹

也可使用 `FollowJointTrajectory` 动作。

```bash
ros2 action send_goal \
  /scaled_joint_trajectory_controller/follow_joint_trajectory \
  control_msgs/action/FollowJointTrajectory "
trajectory:
  joint_names:
    - shoulder_pan_joint
    - shoulder_lift_joint
    - elbow_joint
    - wrist_1_joint
    - wrist_2_joint
    - wrist_3_joint
  points:
    - positions: [0.0, -1.57, 1.0, -1.5, 1.5, 0.0]
      time_from_start: {sec: 2}
"
```

成功执行后，机器人将到达对应的目标关节位置。

```{figure} images/fig-4-7-trajectory-result.png
:name: fig-4-7-trajectory-result
:alt: 轨迹执行结果
:width: 90%
:align: center

轨迹执行结果
```

## 程序控制示例

### Python 示例

```bash
ros2 run elite_robots_driver example_safe_joint_move_py --ros-args \
  -p target:="[0.0,-1.2,0.0,-1.57,0.0,0.0]" \
  -p max_vel:=0.5 \
  -p min_time:=2.0 \
  -p controller:="scaled_joint_trajectory_controller"
```

参考：[Python 示例源码](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver/blob/humble/elite_robots_driver/example/python/example_safe_joint_move.py)。

### C++ 示例

```bash
ros2 run elite_robots_driver example_safe_joint_move --ros-args \
  -p target:="[0.0,-1.57,0.0,-1.0,-1.57,0.0]" \
  -p max_vel:=0.5 \
  -p min_time:=2.0 \
  -p controller:="scaled_joint_trajectory_controller"
```

参考：[C++ 示例源码](https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver/blob/humble/elite_robots_driver/example/cpp/example_safe_joint_move.cpp)。

### 参数含义

| 参数 | 说明 |
| --- | --- |
| `target` | 六个目标关节角度（rad）；ROS 参数数组中的整数应写成浮点数，如 `1.0` |
| `max_vel` | 用于估算轨迹时长的关节速度（rad/s），建议设置为正数 |
| `min_time` | 最小轨迹时长（s），应设置为正数 |
| `controller` | 使用的轨迹控制器名称 |

```{note}
当 `max_vel > 0` 时，程序使用 `max(min_time, 最大关节角度差 / max_vel)` 计算目标点的 `time_from_start`。`max_vel <= 0` 时直接使用 `min_time`。这只是轨迹时长估算，不是对插值过程中瞬时速度的硬性限制；实际执行还受控制器速度缩放等因素影响。
```
