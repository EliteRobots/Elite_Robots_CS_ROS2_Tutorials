# 3. 编译并启动

如果你是通过编译安装的方式使用 ROS2 驱动包，请在每个新打开的终端中 source 配置，此处假定工作空间位于 `~/elite_ros_ws`：
```{code-block} bash
cd ~/elite_ros_ws

source install/setup.bash
```

使用虚拟的双臂：

```{code-block} bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=true \
  headless_mode:=false \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

使用真机双臂：

```{code-block} bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=false \
  headless_mode:=true \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

真机使用 `headless_mode:=true` 时，机器人需要启用远程控制模式。
如果端口冲突，也可以直接覆盖，例如：

```{code-block} bash
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
