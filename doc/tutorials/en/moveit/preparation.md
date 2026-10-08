# Prepare the workspace

## Environment and prerequisites

Prepare ROS 2 Humble, MoveIt 2, and a built Elite driver and description workspace. You should be familiar with ROS packages, launch files, URDF/Xacro, and the workspace `build` and `install` directories. For model basics, see the [ROS 2 URDF tutorials](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html).

In each new terminal, source ROS and the driver workspace. Replace `/path/to/driver_ws` with its actual path:

```bash
source /opt/ros/humble/setup.bash
source /path/to/driver_ws/install/setup.bash
ros2 pkg prefix elite_robots_description
ros2 pkg prefix elite_robots_driver
ros2 pkg prefix elite_robots_moveit_config
```

All three queries should return installation prefixes. Repository directory names differ from ROS package names; commands use the names declared in `package.xml`.

## Download and build the examples

Download {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>` and {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`. The commands below assume the files are in `~/Downloads/`; adjust this to your download location. The workspace's `src` directory should not already contain packages with these names:

```bash
export COLCON_WS=~/workspaces/elite_tutorials
mkdir -p "$COLCON_WS/src"
unzip ~/Downloads/hello_moveit.zip -d "$COLCON_WS/src"
unzip ~/Downloads/my_elite_robot_cell.zip -d "$COLCON_WS/src"
cd "$COLCON_WS"
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --symlink-install
source install/setup.bash
```

If you already have this documentation repository, you can instead copy the examples from its root:

```bash
export COLCON_WS=~/workspaces/elite_tutorials
mkdir -p "$COLCON_WS/src"
cp -r doc/tutorials/examples/moveit/hello_moveit "$COLCON_WS/src/"
cp -r doc/tutorials/examples/moveit/my_elite_robot_cell "$COLCON_WS/src/"
```

Then run the dependency installation and build commands above.

If rosdep cannot find an Elite package, check that the driver workspace is sourced and the required packages are installed. The tutorial uses the driver's controller plugins; the examples do not need to build another SDK.

For an installed documentation package, locate the examples at `$(ros2 pkg prefix elite_robots_cs_tutorials)/share/elite_robots_cs_tutorials/doc/tutorials/examples/moveit` and copy its two directories instead.

Source ROS, the driver workspace, and `$COLCON_WS/install/setup.bash` in every subsequent terminal. Rebuild and source after changing Xacro, YAML, or launch files. C++ source changes require recompilation.

## Example conventions

The model, SRDF, YAML files, and program share six joint names with the `cs63_` prefix. The `elite_arm` group runs from `cs63_base_link` to `cs63_tool0`. Poses use the `world` frame; positions are in m, joint angles in rad, and accelerations in rad/s².

Start with fake hardware to check the configuration. It mirrors commands without simulating dynamics. Fake hardware uses the system clock; leave `use_sim_time` false. This workcell has no Gazebo, camera, or online environment perception.

Before using a physical robot, match the geometry, mounting pose, payload, and tool to the actual installation and complete the robot's network and external-control setup. The example targets are teaching configurations; planning and execution depend on the actual start state, joint bounds, and collision scene.
