# 3. Build and start

If you installed the ROS 2 driver packages by building from source, source the
workspace setup file in every new terminal. Here, the workspace is assumed to
be at `~/elite_ros_ws`:

```{code-block} bash
cd ~/elite_ros_ws

source install/setup.bash
```

Using two virtual arms:

```{code-block} bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=true \
  headless_mode:=false \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

Using two real arms:

```{code-block} bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=false \
  headless_mode:=true \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

With `headless_mode:=true`, each robot must be in remote-control mode. If
ports conflict, override them directly, for example:

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
