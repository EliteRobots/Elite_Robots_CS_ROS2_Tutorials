# Create and use the MoveIt configuration

## Load the workcell

```bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```

Create a configuration and load `urdf/my_elite_robot_cell.urdf.xacro` from the description package with the default CS63 parameters. This URDF includes the complete workcell so planning can check the robot against the table, monitor, and wall.

```{figure} images/load_urdf.png
:name: tutorial-moveit-load-urdf
:width: 90%
:alt: Load the workcell Xacro in Setup Assistant.

Load the workcell Xacro in Setup Assistant.
```

Screenshot paths and UI details may differ from your installation. Use the package and file names in the text and supplied examples. You can use the copied configuration directly or open it in Setup Assistant. Generate a new package in a separate directory to avoid overwriting unsaved configuration.

## Self-collision matrix

Generate the Self-Collisions matrix and inspect disabled link pairs.

```{figure} images/self_collisions.png
:name: tutorial-moveit-self-collisions
:width: 90%
:alt: Generate and review the self-collision matrix.

Generate and review the self-collision matrix.
```

`Adjacent` identifies neighboring links. `Never` means sampling did not observe a collision; it is not proof for every possible pose. Regenerate and review the matrix after changing table height, obstacles, or robot mounting. Pay particular attention to exclusions between the robot and environment objects. Do not disable collision checking to hide an incorrect model or start state.

## Planning group and tip link

Fixed joints already connect the workcell to `world`, so this example needs no additional virtual joint. Create `elite_arm` in Planning Groups and select `kdl_kinematics_plugin/KDLKinematicsPlugin`.

```{figure} images/planning_group_kinematics.png
:name: tutorial-moveit-planning-group-kinematics
:width: 90%
:alt: Select the kinematics solver for elite_arm.

Select the kinematics solver for elite_arm.
```

Set the chain base link to `cs63_base_link` and the tip link to `cs63_tool0`.

```{figure} images/planning_group_chain.png
:name: tutorial-moveit-planning-group-chain
:width: 90%
:alt: Add the arm's kinematic chain.

Add the arm's kinematic chain.
```

```{figure} images/planning_group_links.png
:name: tutorial-moveit-planning-group-links
:width: 90%
:alt: Confirm the chain's base and tip links.

Confirm the chain's base and tip links.
```

You can add a link group containing only `cs63_tool0`. This provides semantic organization; it does not configure a physical gripper, TCP offset, or gripper controller.

```{figure} images/planning_group_tool.png
:name: tutorial-moveit-planning-group-tool
:width: 90%
:alt: Add a tip-link group.

Add a tip-link group.
```

```{figure} images/planning_groups.png
:name: tutorial-moveit-planning-groups
:width: 90%
:alt: Completed planning groups.

Completed planning groups.
```

The core SRDF definition is:

```xml
<group name="elite_arm">
  <chain base_link="cs63_base_link" tip_link="cs63_tool0"/>
</group>
```

## Controllers and generated files

The control package already handles `ros2_control`, so skip duplicate hardware configuration in the assistant. For physical hardware, add `scaled_joint_trajectory_controller` in MoveIt Controllers, with type `FollowJointTrajectory` and the same joint names as the URDF.

```{figure} images/moveit_controllers.png
:name: tutorial-moveit-moveit-controllers
:width: 90%
:alt: Configure the MoveIt trajectory controller.

Configure the MoveIt trajectory controller.
```

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml
:language: yaml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml
:language: yaml
:lines: 1-19
```

```{raw} latex
\end{minipage}\par\medskip
```
````


This YAML tells MoveIt where to find an action server; it does not load or activate ros2_control controllers. The controller name and `action_ns` form `/scaled_joint_trajectory_controller/follow_joint_trajectory` for physical hardware. Fake hardware uses `moveit_controllers_fake.yaml` with `joint_trajectory_controller`.

Skip Perception. Select RViz Launch and Config, MoveGroup Launch, and Setup Assistant Launch under Launch Files. The control package already starts hardware and state publication, so no duplicate demo launch chain is needed. This example does not use Warehouse.

```{figure} images/launch_files.png
:name: tutorial-moveit-launch-files
:width: 90%
:alt: Select the required launch files.

Select the required launch files.
```

Enter the author information and generate `my_elite_robot_cell_moveit_config`, retaining the SRDF, kinematics, joint limits, and controller files.

```{figure} images/config_files.png
:name: tutorial-moveit-config-files
:width: 90%
:alt: Generate the workcell MoveIt configuration package.

Generate the workcell MoveIt configuration package.
```

## Joint limits and time parameterization

URDF position and velocity limits do not replace MoveIt acceleration settings. The example sets acceleration limits for all six joints in `config/joint_limits.yaml` and defaults both velocity and acceleration scaling to 0.1:

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
:lines: 25-36
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`max_velocity` is in rad/s and `max_acceleration` in rad/s². Here, `4.0` is a teaching example's planning value, not a manufacturer-certified hardware limit. Select values for the actual payload, posture, and process. Lower scaling lengthens acceleration and deceleration; higher values do not guarantee faster execution.

These parameters govern MoveIt trajectory time parameterization. They do not replace controller or robot limits and do not automatically constrain trajectories sent outside MoveIt.

## Start planning and RViz

`move_group.launch.py` selects a controller file through `use_fake_hardware` and explicitly selects OMPL:

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
:lines: 25-31
```

```{raw} latex
\end{minipage}\par\medskip
```
````


Here, the argument selects only the MoveIt controller mapping. Start hardware separately through the control launch from the previous chapter.

With fake hardware already running, use two terminals with the workspace sourced:

```bash
ros2 launch my_elite_robot_cell_moveit_config move_group.launch.py \
  use_fake_hardware:=true
```

```bash
ros2 launch my_elite_robot_cell_moveit_config moveit_rviz.launch.py
```

For physical hardware, use `use_fake_hardware:=false` to match the driver's scaled controller. `You can start planning now!` indicates that the planning node started; still check joint states and the action server before execution.

Select `elite_arm` in RViz's MotionPlanning panel, set the start state to the current state, move the target marker, and click Plan. Inspect the trajectory against the environment before executing. Planning success and execution success are separate results.

## Troubleshooting

- Model or SRDF loading fails: check workspace order, package installation, and paths in `.setup_assistant`.
- Current state unavailable: check continuous `/joint_states` publication, all six joint names, and unintended use of simulation time.
- Start-state collision or unreachable target: inspect mounting transforms in `world`, the start pose, target frame, and collision geometry.
- Planning succeeds but execution fails: check active controllers, action names, and matching fake/physical settings on both sides.
- Model and robot differ after calibration: rebuild both example packages and restart the driver, MoveIt, and client.
