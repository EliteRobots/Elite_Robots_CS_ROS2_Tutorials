# Write a MoveIt 2 C++ application

## Create a package and declare dependencies

`hello_moveit` demonstrates setting targets and requesting plans from an application. The copied examples already include this package. To create it from scratch, run the following in a workspace `src` directory that does not already contain it:

```bash
ros2 pkg create --build-type ament_cmake \
  --dependencies moveit_ros_planning_interface rclcpp geometry_msgs \
  --node-name hello_moveit hello_moveit
```

`moveit_ros_planning_interface` provides the client API, `rclcpp` supplies ROS nodes and executors, and `geometry_msgs` defines poses. Save the program below as `src/hello_moveit.cpp` and configure CMake to install the executable and launch files:

{download}`Download the complete file <../../examples/moveit/hello_moveit/CMakeLists.txt>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
:lines: 25-43
```

```{raw} latex
\end{minipage}\par\medskip
```
````


The supplied `package.xml` also declares `moveit_configs_utils`, `launch_ros`, and the workcell MoveIt configuration package used by the launch file. When creating the package from scratch, add these dependencies and the accompanying launch file too.

## Complete program

{download}`Download the complete file <../../examples/moveit/hello_moveit/src/hello_moveit.cpp>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 73-79
```

```{raw} latex
\end{minipage}\par\medskip
```
````


## Node, executor, and model parameters

`rclcpp::init` initializes ROS. The node enables automatic parameter declaration to accept robot model parameters injected by launch. An executor thread processes state and action callbacks while the main thread calls planning interfaces. Shutdown cancels the executor and joins the thread.

The group in `MoveGroupInterface(node, "elite_arm")` must match the SRDF. The program explicitly selects `world` as its reference frame and `cs63_tool0` as its tip, then waits for current joint states. Model files alone cannot establish a valid start state without `/joint_states`.

## Pose and joint targets

The pose target is `(1.3, 0.3, 1.5)` m in `world`. Quaternion `(x,y,z,w)=(0,0,0,1)` represents the identity rotation; four zero components are invalid. Reachability depends on the current model and collision scene.

`setPoseTarget` sets the target, `plan` computes a trajectory, and `execute` sends the result to a controller. The program checks planning and execution results separately. If the first segment fails, it stops before the next target and returns a nonzero exit code.

The second target specifies joint names and values in rad explicitly, avoiding an implicit ordering assumption. `clearPoseTargets` removes the previous target, and `setStartStateToCurrentState` updates the start before each plan. With the default `execute=false`, both plans start from the actual current state; the unexecuted first plan's endpoint is not used as the second plan's start.

## Inject the model and run

The launch file passes the workcell URDF, SRDF, and kinematics parameters directly to the client:

{download}`Download the complete file <../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
:lines: 25-29
```

```{raw} latex
\end{minipage}\par\medskip
```
````


This keeps the client model consistent with `move_group` without relying on model topic publication.

```bash
cd "$COLCON_WS"
colcon build --symlink-install --packages-select hello_moveit
source install/setup.bash
ros2 launch hello_moveit hello_moveit.launch.py execute:=false
```

Keep the driver, `move_group`, and RViz running as described in the previous chapter. Inspect the plans and logs first. To execute the reviewed teaching targets, use:

```bash
ros2 launch hello_moveit hello_moveit.launch.py execute:=true
```

```{figure} images/run_pose.png
:name: tutorial-moveit-run-pose
:width: 90%
:alt: Example RViz display of a pose-target plan.

Example RViz display of a pose-target plan.
```

```{figure} images/run_joint.png
:name: tutorial-moveit-run-joint
:width: 90%
:alt: Example RViz display of a joint-target plan.

Example RViz display of a joint-target plan.
```

These screenshots illustrate how to inspect planning results. Changes in current pose, calibration, or scene may produce different trajectories. `execute=true` sends motion requests to the currently connected controller.

For further API study, see the [MoveIt 2 Humble tutorials](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html).

## Download the complete examples

- {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>`: the MoveIt C++ example package, including source, build configuration, and launch files.
- {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`: the complete workcell, including the description, control, and moveit_config packages and model resources.

Extract the archives to obtain `hello_moveit/` and `my_elite_robot_cell/`. Place both directories under the same workspace's `src/`, then follow [Prepare the workspace](preparation.md) to install dependencies and build.

```{only} latex
Download the archives from this section in the HTML edition of the tutorial.
```
