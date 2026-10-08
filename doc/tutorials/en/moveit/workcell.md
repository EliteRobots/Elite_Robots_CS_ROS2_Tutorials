# Assemble the workcell model

## Top-level description and macro

`my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro` is the model entry point. It includes the workcell macro, declares the model and four parameter files, creates the `world` link, and instantiates the scene.

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
:lines: 25-25
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`xacro:include` imports definitions; `xacro:my_elite_robot_cell` creates the links and joints. The four YAML files supply joint limits, geometric kinematics, physical properties, and visual resources. The example stores CS63 parameters in the description package's `config/cs63/` so visualization, control, and planning share the same geometry.

The `<origin xyz="0 0 1" .../>` element is an XML block passed into the macro through `*origin` and `xacro:insert_block`. It places the table reference link 1 m above `world`; this is not directly the robot base position.

## Scene and mounting relationships

The complete workcell macro is:

{download}`Download the complete file <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 73-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 97-105
```

```{raw} latex
\end{minipage}\par\medskip
```
````


The table and monitor use DAE meshes for visual and collision geometry. The wall uses a visual mesh and a box collision shape. `visual` controls appearance; `collision` controls planning collision checks. Both should describe the same physical obstacle.

`table_base_joint` fixes the table to its parent. Fixed joints connect the monitor, wall, and `robot_mount` to the table. Here, `robot_mount` is offset by `(1.0, 0.5, 0)` m relative to the table. With the default unrotated mounting, the robot mounting point is therefore `(1.0, 0.5, 1.0)` m in `world`.

`cs_robot` comes from `elite_robots_description/urdf/cs_macro.xacro`. Its `parent` must already exist. With `tf_prefix="cs63_"`, robot joints and links include names such as `cs63_shoulder_pan_joint` and `cs63_base_link`. The prefix must match the SRDF, controllers, and application.

`generate_ros2_control_tag="false"` generates geometry only. The next chapter adds the control tag once in a separate description, avoiding duplicate hardware declarations.

## Inspect the model

```bash
ros2 launch my_elite_robot_cell_description view_robot.launch.py
```

Set RViz Fixed Frame to `world`. Move the `joint_state_publisher_gui` sliders to inspect mounting height, orientation, and joint connections. These sliders publish joint states for visualization only.

```{figure} images/view_workspace.png
:name: tutorial-moveit-view-workspace
:width: 90%
:alt: Workcell containing the table, monitor, wall, and CS63.

Workcell containing the table, monitor, wall, and CS63.
```

You can also expand Xacro offline and inspect the generated XML:

```bash
xacro "$(ros2 pkg prefix my_elite_robot_cell_description)/share/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro" \
  > /tmp/my_elite_robot_cell.urdf
check_urdf /tmp/my_elite_robot_cell.urdf
```

The model should contain one root link, `world`, and six movable joints. If resources cannot be found, check that the package in each `package://` URI is installed and that CMake installs `meshes`, `config`, and `urdf`.

Close this visualization launch before starting the driver so the GUI and driver do not publish conflicting states on `/joint_states`.
