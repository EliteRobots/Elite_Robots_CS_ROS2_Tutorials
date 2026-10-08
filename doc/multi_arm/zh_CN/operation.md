# 启动与检查

## fake hardware 双臂

在已加载环境的终端中进入保存目录并启动：

```bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=true \
  headless_mode:=false \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

这只创建 mock 硬件，不连接机器人。模板使用缩放轨迹控制器；后续 MoveIt 也显式选择相同控制器，不沿用旧版单臂 fake 示例的标准控制器假设。

## 实体双臂

确认两台机器人地址及回连网络后，在同一保存目录启动：

```bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=false \
  headless_mode:=true \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

IP 为示例，应替换为实际地址。无头模式直接发送外部控制脚本，需满足远程模式和机器人运行状态条件。若使用 `headless_mode=false`，分别在两台示教器的 ExternalControl 任务中配置 ROS 计算机地址以及对应 script sender 端口，并运行各自任务。

端口冲突时可完整覆盖两组端口：

```bash
ros2 launch dual_arm_control.launch.py \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_reverse_port:=51001 \
  arm1_script_sender_port:=51002 \
  arm1_trajectory_port:=51003 \
  arm1_script_command_port:=51004 \
  arm2_reverse_port:=51101 \
  arm2_script_sender_port:=51102 \
  arm2_trajectory_port:=51103 \
  arm2_script_command_port:=51104
```

不要在默认端口的驱动仍运行时重复启动第二套相同实例。端口、namespace 和节点名都应避免冲突。

## 分别确认两台机械臂

另开终端加载环境，执行只读检查：

```bash
ros2 control list_controllers -c /arm1/controller_manager
ros2 control list_controllers -c /arm2/controller_manager
ros2 control list_hardware_interfaces -c /arm1/controller_manager
ros2 control list_hardware_interfaces -c /arm2/controller_manager
ros2 action list -t
ros2 topic echo /arm1/joint_states --once
ros2 topic echo /arm2/joint_states --once
```

确认每臂关节状态与缩放轨迹控制器 active，关节名具有对应前缀。六轴应有六个关节；`cs520h` 应有五个，没有 wrist_3_joint。前向位置和 freedrive 默认 inactive 是模板的预期配置。

轨迹动作分别为：

```text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

两者类型均为 `control_msgs/action/FollowJointTrajectory`。向 arm1 发送目标时，joint_names 必须使用 `arm1_shoulder_pan_joint` 等前缀名称；arm2 使用 `arm2_`。位置单位为 rad，时间为相对轨迹起点的累计时间；数组必须与关节名称一一对应。

动作存在不等于机器人可运动。真机还需检查外部控制连接、任务状态、控制器激活状态及运动范围。本手册不执行运动验证，也不提供可直接套用到任意双臂布局的目标位置。

## 常见问题与单臂回退

- 管理器等待超时：检查 namespace、管理器全名、生成 YAML 的节点键，以及是否加载了正确的安装环境。
- 找到动作但拒绝目标：检查 active 状态、前缀、五轴/六轴数量及时间字段。
- fake IO 未激活：核对 mock 资源缺失及日志；分别确认轨迹控制器是否正常，勿用最后一行日志代替状态查询。
- 真机未进入外部控制：分别核对 IP、回连地址、端口、远程模式和各自任务。

模板不会修改单臂入口。停止双臂实例后仍可按单臂方式启动：

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

单臂默认使用 `/controller_manager`，由其 launch 自己启动控制器。
