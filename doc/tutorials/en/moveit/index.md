# MoveIt 2: custom workcell and motion planning

This tutorial produces a workcell containing a table, monitor, wall, and CS63, together with control configuration, MoveIt configuration, and a C++ client.

Xacro generates the URDF. The driver reads its `ros2_control` configuration and publishes joint states. MoveIt combines the URDF, SRDF, kinematics, and collision scene to plan trajectories, then sends them to a controller through a `FollowJointTrajectory` action.

## Download the complete examples

- {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>`: the MoveIt C++ example package, including source, build configuration, and launch files.
- {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`: the complete workcell, including the description, control, and moveit_config packages and model resources.

Extract the archives to obtain `hello_moveit/` and `my_elite_robot_cell/`. Place both directories under the same workspace's `src/`, then follow [Prepare the workspace](preparation.md) to install dependencies and build.

```{only} latex
Download the archives from this section in the HTML edition of the tutorial.
```

## Four packages in the workcell

- `my_elite_robot_cell_description`: scene geometry, mounting transforms, model parameters, and a visualization launch file.
- `my_elite_robot_cell_control`: the description with `ros2_control` and the driver launch file.
- `my_elite_robot_cell_moveit_config`: planning groups, collision matrix, solvers, joint limits, controller mappings, and MoveIt launch files.
- `hello_moveit`: a C++ program that sets pose and joint targets, plans, and optionally executes.

These are tutorial package names. The underlying driver, model, and controllers come from `elite_robots_driver`, `elite_robots_description`, and `elite_robots_controllers`.

Prepare the workspace, then follow modeling, control, planning configuration, and programming in order. Displaying the model does not require the driver; executing a trajectory requires both the driver and MoveIt to be ready.

```{toctree}
:maxdepth: 2

preparation
workcell
control
configuration
cpp
```
