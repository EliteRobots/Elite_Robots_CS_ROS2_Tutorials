# Connect ros2_control and the robot driver

## Add control information

`my_elite_robot_cell_controlled.urdf.xacro` creates the same scene, then calls `cs_ros2_control` to add the hardware plugin and state and command interfaces:

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 73-75
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`robot_ip` is the robot address; `local_ip` is the computer interface used for the robot's reverse connection. The script and input/output recipes come from `elite_robots_driver/resources/`. `use_fake_hardware=true` selects `mock_components/GenericSystem`; false selects the Elite hardware plugin.

Both the scene and control tag use the `cs63_` prefix so controller joints match the exported hardware interfaces. Arguments such as `script_filename`, `input_recipe_filename`, and `output_recipe_filename` match the Xacro arguments passed by the driver launch.

## Wrap the driver launch

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
:lines: 25-42
```

```{raw} latex
\end{minipage}\par\medskip
```
````


The wrapper includes `elite_robots_driver/launch/elite_control.launch.py` and selects the custom `description_package` and `description_file`. `runtime_config_package` remains `elite_robots_driver`, so controller plugin configuration and update rates come from the driver package. The controller YAML expands `$(var tf_prefix)` to `cs63_`.

The driver reads model parameters from `description_package/config/cs63/`. The example control package's CMake installs the description package's maintained `config/` there. Visualization and MoveIt read the same source data from the description package. Rebuild both packages after changes to keep the installed copies consistent.

This launch accepts only `cs63`. Another model requires coordinated changes to geometry parameters, SRDF, joint limits, controller joint names, and target poses; changing only the model string is insufficient.

## Calibration data

The supplied `default_kinematics.yaml` contains nominal geometry. Use `elite_robots_calibration` to export calibration data for a physical robot:

```bash
ros2 launch elite_robots_calibration calibration_correction.launch.py \
  robot_ip:=192.168.1.200 target_filename:=/tmp/my_elite_robot_calibration.yaml
```

After a successful export, inspect the file and replace the description package's `config/cs63/default_kinematics.yaml`. Rebuild the description and control packages:

```bash
cp /tmp/my_elite_robot_calibration.yaml \
  "$COLCON_WS/src/my_elite_robot_cell/my_elite_robot_cell_description/config/cs63/default_kinematics.yaml"
cd "$COLCON_WS"
colcon build --symlink-install --packages-select \
  my_elite_robot_cell_description my_elite_robot_cell_control
source install/setup.bash
```

Restart the driver and MoveIt so both load the same calibration. The current driver launch does not declare a `kinematics_params_file` override; passing that name from a wrapper does not apply calibration. Model calibration does not set tool TCP, payload, or table mounting transforms.

## Start and check

Start fake hardware with the standard trajectory controller:

```bash
ros2 launch my_elite_robot_cell_control start_robot.launch.py \
  use_fake_hardware:=true launch_rviz:=false \
  initial_joint_controller:=joint_trajectory_controller
```

Check from another terminal:

```bash
ros2 control list_controllers -c /controller_manager
ros2 topic echo /joint_states --once
ros2 action info /joint_trajectory_controller/follow_joint_trajectory
```

Confirm that `joint_state_broadcaster` and `joint_trajectory_controller` are active, joint states contain all six `cs63_` names, and the trajectory action has a server. A started process or an exited spawner alone does not establish controller readiness.

For a physical robot, replace both IP addresses below and complete the robot-side external-control setup first:

```bash
ros2 launch my_elite_robot_cell_control start_robot.launch.py \
  use_fake_hardware:=false robot_ip:=192.168.1.200 local_ip:=192.168.1.100 \
  headless_mode:=false launch_rviz:=false \
  initial_joint_controller:=scaled_joint_trajectory_controller
```

With `headless_mode=false`, run the program containing the external-control node on the teach pendant. With true, the driver sends the external-control script, but the robot must still satisfy its operating prerequisites. Check that `scaled_joint_trajectory_controller` is active and that its action server is available.
