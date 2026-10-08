# Startup and checks

## Dual-arm fake hardware

In a terminal with the environment sourced, enter the saved file directory and launch:

```bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=true \
  headless_mode:=false \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

This creates mock hardware without connecting to robots. The template uses scaled trajectory controllers; the MoveIt wrapper explicitly selects the same controllers rather than inheriting the standard-controller assumption of older single-arm fake examples.

## Physical dual-arm setup

After confirming both robot addresses and reverse connectivity, launch from the same directory:

```bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=false \
  headless_mode:=true \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

Replace the example IPs with actual addresses. Headless mode sends the external control script directly and requires appropriate remote mode and robot operating state. With `headless_mode=false`, configure each teach pendant's ExternalControl task with the ROS computer address and its corresponding script sender port, then run each task.

If ports conflict, override both sets:

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

Do not start duplicate instances while drivers using the same ports are still running. Ports, namespaces, and node names must avoid conflicts.

## Check each arm separately

Source the environment in another terminal and run read-only checks:

```bash
ros2 control list_controllers -c /arm1/controller_manager
ros2 control list_controllers -c /arm2/controller_manager
ros2 control list_hardware_interfaces -c /arm1/controller_manager
ros2 control list_hardware_interfaces -c /arm2/controller_manager
ros2 action list -t
ros2 topic echo /arm1/joint_states --once
ros2 topic echo /arm2/joint_states --once
```

Confirm each arm's joint state broadcaster and scaled trajectory controller are active, with the expected joint prefixes. Six-axis robots have six joints; `cs520h` has five, without wrist_3_joint. Forward position and freedrive being inactive is expected in this template.

Trajectory actions are:

```text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

Both use `control_msgs/action/FollowJointTrajectory`. Goals for arm1 must use joint_names such as `arm1_shoulder_pan_joint`; arm2 names use `arm2_`. Positions use rad, and times are cumulative from trajectory start. Arrays must correspond to joint names.

An existing action does not prove the robot is ready to move. Physical robots also require a valid external control connection, task state, active controller, and a checked motion envelope. This manual performs no motion validation and provides no target positions intended to fit arbitrary dual-arm layouts.

## Troubleshooting and returning to single-arm operation

- Manager wait timeout: inspect namespaces, manager full names, generated YAML node keys, and the sourced installation.
- Action exists but rejects a goal: inspect active state, prefixes, five/six-axis counts, and timing fields.
- Fake IO is inactive: check missing mock resources and logs; independently verify trajectory controller state. Do not substitute the final log line for a state query.
- Physical robot does not enter external control: check each IP, reverse connection address, port set, remote mode, and task.

The template does not modify the single-arm entry point. After stopping dual-arm instances, single-arm operation remains available:

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

The single-arm default is `/controller_manager`, with controllers spawned by its own launch file.
