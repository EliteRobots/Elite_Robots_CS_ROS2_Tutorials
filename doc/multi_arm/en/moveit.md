# Optional dual-arm MoveIt

## Save the complete template

Skip this chapter if MoveIt is not required. Otherwise, save as `~/dual_arm_launch/dual_moveit.launch.py`, or download {download}`dual_moveit.launch.py <../examples/dual_moveit.launch.py>`.

````{only} html
```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
```
````

````{only} latex

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 1-32
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 33-64
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 65-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 97-128
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 129-147
```

```{raw} latex
\end{minipage}\par\medskip
```

````

## Matching each arm

The template generates three temporary configurations per arm:

1. Controller list: selects `controllers_5f.yaml` or `controllers.yaml` for the axis count and prefixes joint names. Controller names remain relative, so the MoveIt namespace resolves the corresponding actions.
2. Kinematics: replaces `cs_manipulator` with `arm1_cs_manipulator` or `arm2_cs_manipulator`, matching the prefixed SRDF planning group.
3. RViz: sets the appropriate Planning Group, Move Group Namespace, and trajectory display topic.

`prefer_scaled_controller=true` selects scaled trajectory control for both fake and physical hardware, matching the driver template. Here, the single-arm `use_fake_hardware` argument affects MoveIt execution mapping; it does not start hardware. The dual-arm driver remains responsible for hardware. `launch_servo=false` explicitly disables Servo.

The template neither combines planning scenes nor completely rewrites OMPL or joint limit YAML for multiple arms; it generates only the three files above. For a specific planner or per-joint limit overrides, verify planning group/joint names against custom configuration rather than assuming every single-arm setting receives a prefix automatically.

## Startup order and arguments

Start the driver and verify both trajectory controllers as described in the previous chapter. Then source ROS and the workspace in another terminal:

```bash
cd ~/dual_arm_launch
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  launch_rviz:=true
```

This command is for fake hardware. Physical robots use the default `use_fake_hardware=false`:

```bash
ros2 launch dual_moveit.launch.py
```

`arm1_cs_type` and `arm2_cs_type` both default to `cs63` and must match the driver. Five-axis example, with the driver's arm2 configured for the same model:

```bash
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs520h
```

`launch_rviz` defaults to true for both instances; set it to false to disable both RViz processes. This setup continues to use system time.

## Verify planning and execution targets

```bash
ros2 node info /arm1/move_group
ros2 node info /arm2/move_group
ros2 action list -t
```

Select the corresponding planning group in each RViz and check Move Group Namespace, joint feedback, and robot model. Before execution, confirm its controller target belongs to that arm rather than the other arm or the root namespace. Successful planning does not establish that the controller can execute.

If RViz does not show the expected content, inspect the generated temporary configuration for the group name, namespace, and display_planned_path. String replacements depend on the installed RViz template. End-effector poses, TF, and model base positions must still match the physical installation.
