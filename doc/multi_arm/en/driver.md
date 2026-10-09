# Dual-arm driver guide

## Prepare the example files

Create `~/dual_arm_launch` to hold the example launch files:

```bash
mkdir -p ~/dual_arm_launch
cd ~/dual_arm_launch
```

Download {download}`dual_arm_control.launch.py <../examples/dual_arm_control.launch.py>` into this directory, or save the complete code at the end of this chapter as `~/dual_arm_launch/dual_arm_control.launch.py`. Launch the file directly by name; it does not need to be installed in a ROS package.

Choose either fake hardware or physical dual-arm operation from the following startup examples.

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

## How the dual-arm driver works

The template reads the driver controller YAML for each arm's model. Models ending in `h` use `elite_cs_controllers_5f.yaml`; others use `elite_cs_controllers.yaml`. It qualifies top-level node keys with the arm's absolute names, replaces `$(var tf_prefix)` with its prefix, and writes a temporary file.

`PushRosNamespace` places single-arm nodes in their namespace. `controller_manager_name` addresses the correct manager. `spawn_controllers=false` disables the single-arm internal spawners so the wrapper can start controllers explicitly. The single-arm entry point also uses the corresponding manager key in the update rate YAML.

Within each arm, spawners run sequentially for joint states, IO, speed scaling, force/torque, TCP pose, scaled trajectories, direct position, and freedrive. The last two use `--inactive`; the others request activation. The two arms' startup chains are independent and may run concurrently.

```{important}
Sequencing uses `OnProcessExit` without checking the preceding exit code. Completion of arm2's last spawner does not mean arm1 has finished or that all controllers are active. The final log in this template only reports that the startup chain exited. Query both managers using the checks earlier in this chapter.
```

With fake hardware, GPIO command interfaces may not satisfy activation requirements and `io_and_status_controller` may remain inactive. Inspect logs and hardware interfaces to distinguish mock limitations from namespace errors. The same IO activation failure on physical hardware should not be treated as expected.

## What must be isolated per arm

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - Item
  - arm1
  - arm2
* - ROS namespace
  - `arm1`
  - `arm2`
* - Joint/TF prefix
  - `arm1_`
  - `arm2_`
* - Controller manager
  - `/arm1/controller_manager`
  - `/arm2/controller_manager`
* - Default controller IP
  - `192.168.1.101`
  - `192.168.1.102`
* - Default model
  - `cs63`
  - `cs63`
* - MoveIt planning group
  - `arm1_cs_manipulator`
  - `arm2_cs_manipulator`
```

ROS namespaces isolate nodes, services, topics, and actions. Prefixes isolate joint, link, and hardware resource identifiers. Configure both. A name prefix is not a spatial transform, and the shared `world` root in the default models does not mean the relative arm positions have been calibrated.

Robot communication ports on the same ROS computer must also be distinct. The four port types are reverse, script sender, trajectory, and script command: arm1 defaults to 50001–50004 and arm2 to 50101–50104.

## Parameters and configuration

Override these defaults on the command line:

- `arm1_ip`, `arm2_ip`: `192.168.1.101`, `192.168.1.102`.
- `arm1_cs_type`, `arm2_cs_type`: both `cs63`, validated by each single-arm entry point.
- `use_fake_hardware`: `false`; shared by both arms in this template.
- `headless_mode`: `true`; shared by both arms.
- `controller_spawner_timeout`: `30` s; manager wait timeout, not a motion execution timeout.
- `arm1_reverse_port`, `arm1_script_sender_port`, `arm1_trajectory_port`, `arm1_script_command_port`: `50001`, `50002`, `50003`, `50004` respectively.
- Corresponding arm2 arguments start with `arm2_` and default to `50101`, `50102`, `50103`, `50104`.

Namespaces and joint prefixes are fixed in the template as arm1/arm1_ and arm2/arm2_; they are not overridable launch arguments. A third arm requires another arm group, unique prefix, IP, four ports, and a corresponding MoveIt instance.

Temporary YAML files use `NamedTemporaryFile(delete=False)` and are not removed automatically at shutdown. Retain them for debugging and clean them up once no longer used. Text substitutions depend on the current YAML structure; recheck generated output after changing custom file structures.

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

The dual-arm wrapper does not expose separate `local_ip` arguments and retains single-arm automatic address selection. If multiple network interfaces require explicit per-arm addresses, add and forward the corresponding arguments in your custom wrapper.

## Complete example code

````{only} html
```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
```
````

````{only} latex

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 1-32
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 33-64
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 65-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 97-128
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 129-160
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 161-192
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 193-224
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 225-229
```

```{raw} latex
\end{minipage}\par\medskip
```

````
