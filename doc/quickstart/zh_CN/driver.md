# 驱动入门

本章使用原手册中的 `eli_cs_robot_driver`，通过服务、话题和动作接口完成基本控制。这里的包名和接口名尚未迁移到当前项目。

## 启动与连接

先完成[网络配置或 ELIBOTSim 启动](robot_setup.md)，并在每个操作终端加载环境：

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
```

### 在示教器上电并释放抱闸

依次点击“打开电源”和“释放抱闸”，确认机器人进入正常模式。

```{admonition} 图片占位 · 原图 4-1～4-3：机器人状态准备
:class: figure-placeholder
待补充打开电源、释放抱闸、正常模式三张图。
建议文件名：`images/fig-4-1-power-on.png` 至 `images/fig-4-3-normal-mode.png`。
```

### 启动驱动

```bash
ros2 launch eli_cs_robot_driver elite_control.launch.py \
  robot_ip:=<robot_ip> \
  cs_type:=<cs_type> \
  headless_mode:=true
```

- `robot_ip`：实体机器人实际 IP；原手册的虚拟示教器场景使用本地计算机 IP。
- `cs_type`：实际机器人型号，例如 `cs66`。
- `headless_mode`：是否启用原手册所述的外部程序控制模式。

启动成功后，RViz 中的机器人姿态应与示教器一致，示教器左上角应显示运行状态。

```{admonition} 图片占位 · 原图 4-4～4-5：姿态对照
:class: figure-placeholder
待补充 RViz 和示教器中的机器人姿态两张图。
建议文件名：`images/fig-4-4-rviz.png`、`images/fig-4-5-pendant.png`。
```

## 服务调用示例

执行服务调用时，应保持驱动节点运行，并另开已加载环境的终端。上电、释放抱闸等服务用于切换机器人状态，不要求提前通过示教器完成同一操作。

### Dashboard 服务

**打开电源：**

```bash
ros2 service call /dashboard_client/power_on std_srvs/srv/Trigger "{}"
```

按原手册说明，机器人状态将由关机切换为待机。

```{admonition} 图片占位 · 原图 4-6：转为待机
:class: figure-placeholder
待补充上电后的示教器状态。建议文件名：`images/fig-4-6-standby.png`。
```

**释放抱闸：**

```bash
ros2 service call /dashboard_client/brake_release \
  std_srvs/srv/Trigger "{}"
```

按原手册说明，机器人状态将变为正常模式。

**查询当前任务状态：**

```bash
ros2 service call /dashboard_client/get_task_status \
  eli_common_interface/srv/GetTaskStatus "{}"
```

```{admonition} 图片占位 · 原图 4-7：任务状态返回结果
:class: figure-placeholder
待补充服务调用结果。建议文件名：`images/fig-4-7-task-status.png`。
```

### PrimaryClient 节点与服务

按原手册示例启动节点，将示例 IP 替换为实际机器人 IP：

```bash
ros2 run eli_cs_robot_driver primary_client \
  --ros-args -p robot_ip:=192.168.1.200
```

另开终端，根据需要选择对应服务调用。以下是独立功能示例，不是要求连续执行的操作流程。

```bash
# 重连机器人通信端口
ros2 service call /primary_client/connect std_srvs/srv/Trigger "{}"

# 解除防护停止
ros2 service call /primary_client/unlock_protective_stop \
  std_srvs/srv/Trigger "{}"

# 重启安全系统
ros2 service call /primary_client/restart_safety std_srvs/srv/Trigger "{}"

# 伺服上电
ros2 service call /primary_client/power_on std_srvs/srv/Trigger "{}"

# 释放电机抱闸
ros2 service call /primary_client/brake_release std_srvs/srv/Trigger "{}"

# 暂停程序
ros2 service call /primary_client/pause std_srvs/srv/Trigger "{}"

# 停止程序
ros2 service call /primary_client/stop std_srvs/srv/Trigger "{}"

# 伺服下电
ros2 service call /primary_client/power_off std_srvs/srv/Trigger "{}"
```

完整接口说明可参考[原手册引用的接口文档](https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver/blob/main/doc/ROS2Interface_CN.md)。本项目独立的接口手册尚未编写。

## 控制器与关节轨迹

`ros2_control` 管理机器人硬件与控制器。原手册介绍了以下接口或控制器：

| 名称 | 作用 |
| --- | --- |
| `speed_scaling_interface` | 读取机器人速度缩放值并传递给控制器 |
| `scaled_joint_command_interface` | 结合速度缩放提供关节状态与命令访问 |
| `speed_scaling_state_controller` | 将当前执行速度缩放值（0～1）发布到话题 |
| `scaled_joint_trajectory_controller` | 根据机器人速度缩放调整轨迹执行进度 |

```{warning}
执行以下轨迹或程序示例前，应确保驱动正在运行、机器人处于运行模式，并确认周围环境安全。示例会使机器人移动。
```

### 查看控制器状态

```bash
ros2 control list_controllers
```

```{admonition} 图片占位 · 原图 4-8：控制器列表
:class: figure-placeholder
待补充控制器名称与状态输出。建议文件名：`images/fig-4-8-controllers.png`。
```

### 通过话题发送轨迹

以下示例向轨迹控制器发布一次消息，关节位置和时间保持原手册数值：

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

### 通过动作发送轨迹

也可使用 `FollowJointTrajectory` 动作。注意原手册该示例的第二个关节目标为 `-1.57`，与上一个话题示例不同。

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

```{admonition} 图片占位 · 原图 4-9：轨迹执行结果
:class: figure-placeholder
待补充执行结果截图。建议文件名：`images/fig-4-9-trajectory-result.png`。
```

## 程序控制示例

以下命令保留原手册中 Python、C++ 两种示例的调用方式。原手册对两者均使用了 `example_safe_joint_move` 这一可执行名，实际包中的名称和参数支持情况需要后续结合版本核对。

### Python 示例

```bash
ros2 run eli_cs_robot_driver example_safe_joint_move \
  --target 0 -1.2 0 -1.57 0 0 \
  --max-vel 0.5 \
  --min-time 2.0 \
  --controller scaled_joint_trajectory_controller
```

原手册参考：[Python 示例源码](https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver/blob/main/eli_cs_robot_driver/example/python/example_safe_joint_move.launch.py)。

### C++ 示例

```bash
ros2 run eli_cs_robot_driver example_safe_joint_move --ros-args \
  -p target:="[0.0,-1.57,0.0,-1.0,-1.57,0.0]" \
  -p max_vel:=0.5 \
  -p min_time:=2.0 \
  -p controller:="scaled_joint_trajectory_controller"
```

原手册参考：[C++ 示例源码](https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver/blob/main/eli_cs_robot_driver/example/cpp/example_safe_joint_move.cpp)。

### 参数含义

| 参数 | 原手册说明 |
| --- | --- |
| `target` | 六个目标关节角度；ROS 参数数组中的整数应写成浮点数，如 `1.0` |
| `max_vel` | 最大关节速度比例，值越大运动越快 |
| `min_time` | 最小运动时间 |
| `controller` | 使用的轨迹控制器名称 |

按原手册说明，程序比较由速度条件计算出的运动时间与 `min_time`，取其中较大者作为实际运动时间。
