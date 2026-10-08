# Driver, hardware, and calibration interfaces

## Starting the driver

Load the environment in each terminal, adjusting the workspace path to the actual installation:

```bash
source /opt/ros/humble/setup.bash
source ~/elite_ros_ws/install/setup.bash
```

Physical robots and ELIBOTSim use the same entry point. Replace the model and addresses before running:

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  cs_type:=cs66 robot_ip:=<robot_ip> local_ip:=<local_ip> \
  headless_mode:=true launch_rviz:=false
```

Headless mode sends the external control script directly. If remote control is enabled on the robot, select remote mode and satisfy the robot state conditions for starting a task. In non-headless mode, configure the ROS computer address and script port in the teach pendant's ExternalControl task, then start that task. Script transmission, script execution, and trajectory controller activation are separate states.

The following fake hardware configuration can be used for joint interface integration. `robot_ip` remains required by the launch file, but this mode does not establish a physical robot connection:

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  cs_type:=cs66 robot_ip:=0.0.0.0 use_fake_hardware:=true \
  initial_joint_controller:=joint_trajectory_controller
```

Fake hardware is not a complete controller simulator. This launch version still attempts to start IO and other broadcasters; that does not guarantee realistic service behavior.

## Nodes and executables

All programs below belong to `elite_robots_driver`.

```{list-table}
:header-rows: 1
:widths: 45 55

* - Executable
  - Node or purpose
* - `eli_ros2_control_node`
  - Controller manager process for the physical driver.
* - `eli_components_loader`
  - Loads Dashboard, Primary, and script nodes into one executor.
* - `dashboard_client`
  - Standalone Dashboard component; node name `dashboard_client`.
* - `primary_client`
  - Standalone Primary component; node name `primary_client`.
* - `script_node`
  - Script component; node name `script_sender`.
* - `controller_stopper_node`
  - Stops/resumes motion controllers according to task state; named `controller_stopper` by the launch file.
* - `example_safe_joint_move`
  - C++ example sending a single joint target.
* - `example_safe_joint_move_py`
  - Python example sending a single joint target.
```

With `use_fake_hardware:=true`, the standard `controller_manager/ros2_control_node` is used instead, and neither the component process nor the controller stopper is loaded.

The component process retains the Dashboard node only if its initial connection succeeds. After a failure, `/dashboard_client/*` services may be absent entirely; `/dashboard_client/connect` in that process cannot restore a removed node. Resolve connectivity and restart the component process, or use the standalone entry point while avoiding duplicate nodes.

The controller stopper subscribes to `io_and_status_controller/robot_task_running` and calls the manager's `list_controllers` and `switch_controller` services and Dashboard's `robot_mode`. When the task stops, it preserves the five default state broadcaster/IO controllers and deactivates other active controllers. When the task resumes, it attempts to restore the controllers it stopped. If Dashboard is absent, it waits for that service; the existence of this node alone does not mean its controller protection logic is ready.

## Parameter layers

For the complete `elite_control.launch.py` argument list, see the [Launch argument reference](launch_reference.md). Launch arguments are passed into Xacro and then through `<ros2_control><hardware>` to the hardware plugin. The following are not ordinary node parameters that can be updated live using `ros2 param set`.

Hardware plugin: `ELITE_CS_ROBOT_ROS_DRIVER/EliteCSPositionHardwareInterface`.

- `robot_ip`: required by launch; controller address.
- `local_ip`: default `0.0.0.0`; ROS computer address for reverse connections. The driver converts this default to an empty string so the SDK can select the address automatically.
- `headless_mode`: default `false`; whether to send the external control script directly.
- `reverse_port`: default `50001`; cyclic control communication port on the ROS computer.
- `script_sender_port`: default `50002`; port supplying the script to ExternalControl.
- `trajectory_port`: default `50003`; trajectory communication port on the ROS computer.
- `script_command_port`: default `50004`; script command communication port on the ROS computer.
- `script_filename`: driver resource `resources/external_control.script`; external control script path.
- `input_recipe_filename`: driver resource `resources/input_recipe.txt`; RTSI input recipe path.
- `output_recipe_filename`: driver resource `resources/output_recipe.txt`; RTSI output recipe path.
- `servoj_gain`: default `1000`; servo gain passed to the SDK.
- `servoj_lookahead_time`: default `0.03` s; servo lookahead time.
- `servoj_time`: default `0.008` s; servo cycle parameter.
- `robot_receive_timeout`: default `0.2` s; robot receive timeout, converted to ms when writing commands.

The three servoj parameters and receive timeout come from description macros. This version's top-level driver launch exposes no corresponding overrides. Integrate changes through a custom description file; appending an argument of the same name to the launch command does not establish that it takes effect.

`tool_voltage` defaults to 0 and is passed into the model, but hardware initialization in this version does not read it to set tool voltage. Use the GPIO `set_io` service when needed and verify the result. Although Xacro declares `use_tool_communication`, `tool_parity`, `tool_baud_rate`, `tool_stop_bits`, and `tool_tcp_port`, these do not constitute an implemented ROS tool serial forwarding interface in this version.

## ros2_control resources

Each joint exports `position`, `velocity`, and `effort` state interfaces and `position` and `velocity` command interfaces. Position and velocity control cannot simultaneously occupy the same set of joint resources.

```{important}
This hardware version writes actual joint current into the `effort` state interface. Therefore, `/joint_states.effort` from the physical driver must not be interpreted as joint torque in N·m or used directly to calculate payload. The same field may have different semantics in simulation or other hardware plugins.
```

Other resource names are prefixed with `tf_prefix`:

```{list-table}
:header-rows: 1
:widths: 40 60

* - Resource group
  - State or command
* - `speed_scaling`
  - `speed_scaling_factor` state; `target_speed_fraction_cmd` command.
* - `tcp_fts_sensor`
  - `force.x/y/z` and `torque.x/y/z` states.
* - `tcp_pose`
  - `position.x/y/z` and `orientation.x/y/z/w` states.
* - `gpio`
  - Digital/analog IO, tool data, robot/safety modes, and task state; IO and tool voltage commands.
* - `payload`
  - `mass` and `cog.x/y/z` commands.
* - `resend_external_script`
  - Command to resend the external control script.
* - `hand_back_control`
  - Command to return control.
* - `zero_ftsensor`
  - Force sensor zeroing command.
* - `freedrive_mode`
  - Freedrive start and end commands.
* - `system_interface`
  - `initialized` state.
```

Asynchronous commands also have success feedback resources. Controllers expose these resources as ROS services; applications should normally use the [controller interfaces](controllers.md). `ros2 control list_hardware_interfaces` lists the full resource names and claim status in the current instance.

## Calibration tool

```bash
ros2 launch elite_robots_calibration calibration_correction.launch.py \
  robot_ip:=<robot_ip> target_filename:=/tmp/robot_calibration.yaml
```

This command connects to the robot, reads kinematic information, and writes a local file without sending motion commands. It was not executed for this manual. The executable is `calibration_correction`, and the node name is `cs_calibration`. Launch argument `target_filename` maps to node parameter `output_filename`, defaulting to `robot_calibration.yaml`. Relative paths are resolved against the process working directory.

The parent directory must exist, and an existing file with the same name is overwritten. The program runs once and exits; it provides no persistent application service or topic. Its YAML output does not automatically replace the driver model. In a custom description, point `kinematics_params` to the calibration result and ensure the driver, TF, and MoveIt use the same model. This driver launch version has no separate calibration file argument.
