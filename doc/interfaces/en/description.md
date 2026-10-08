# Robot description interfaces

## Model visualization entry point

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs66
```

This entry point starts `joint_state_publisher_gui`, `robot_state_publisher`, and RViz for model visualization. The GUI generates `/joint_states`; it neither connects to a robot nor sends physical motion commands. Do not start this GUI in a ROS graph where a physical driver already publishes the same joint states.

Accepted models: `cs63`, `cs63a`, `cs66`, `cs66a`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs630`, `cs520h`, and `ls65`.

The Driver, MoveIt, and Gazebo entry points in this version do not accept `cs63a` or `cs630`. The existence of model files does not mean every entry point supports them. There are no `es*` launch choices; do not infer a mapping from an ES model to a CS model.

## Joints and frames

The six-axis controller joint order is:

```text
shoulder_pan_joint
shoulder_lift_joint
elbow_joint
wrist_1_joint
wrist_2_joint
wrist_3_joint
```

The five-axis `cs520h` uses the first five entries and has no `wrist_3_joint`. Launch files select five-axis files when the model name ends in `h`. With non-default custom files, ensure the axis count and names remain consistent.

Common frames are `world` (model root), `base_link` (model base), `base` (controller base reference), `flange`, and `tool0` (model tool reference). A fixed transform relates `base` and `base_link`; coordinates are not interchangeable simply because both frames describe the base. The driver also provides `tool0_controller` from controller feedback, which has a different source from the model-derived `tool0`.

`tf_prefix:=robot1_` directly produces names such as `robot1_shoulder_pan_joint` and `robot1_base_link`. No underscore is added automatically.

## Xacro and configuration files

The six-axis entry point is `urdf/cs.urdf.xacro` in the package share directory; the five-axis entry point is `urdf_5f/cs.urdf.xacro`. The main arguments are listed below. Not every launch file exposes them.

```{list-table}
:header-rows: 1
:widths: 40 60

* - Xacro argument
  - Meaning
* - `name`, `cs_type`
  - Robot name and model configuration.
* - `tf_prefix`
  - Joint, link, and hardware resource prefix.
* - `joint_limit_params`
  - YAML with joint position, velocity, and other limits.
* - `kinematics_params`
  - Kinematics YAML; can integrate calibration results.
* - `physical_params`, `visual_params`
  - Physical properties such as inertia, meshes, and appearance.
* - `safety_limits`
  - Writes URDF safety controller elements; does not replace controller safety functions.
* - `safety_pos_margin`, `safety_k_position`
  - Safety position margin and position coefficient; defaults 0.15 and 20.
* - `use_fake_hardware`
  - Selects GenericSystem.
* - `fake_sensor_commands`
  - Enables sensor command interfaces for fake hardware.
* - `sim_gazebo`, `sim_ignition`
  - Select the respective Gazebo system plugin.
* - `simulation_controllers`
  - Simulation controller YAML path.
* - `initial_positions_file`
  - Simulation initial joint position YAML path.
```

When invoking the six-axis Xacro directly, `cs_type` defaults to `cs63` and `safety_limits` to `false`. Through a launch file, follow that entry point's required arguments and defaults; Xacro defaults are not necessarily launch defaults.

`config/<cs_type>/` contains `joint_limits.yaml`, `default_kinematics.yaml`, `physical_parameters.yaml`, and `visual_parameters.yaml`. Gazebo selects the ordinary, `a`-type, or `h`-type initial position file according to the model.

## ROS model interfaces

`robot_description` is a URDF string parameter passed to `robot_state_publisher`, the controller manager, or MoveIt nodes. `/joint_states` uses `sensor_msgs/msg/JointState`. `/tf` and `/tf_static` use `tf2_msgs/msg/TFMessage` for dynamic and static transforms respectively.

Standard ROS nodes provide these interfaces. Use `ros2 node info /robot_state_publisher` to inspect the publishers and subscribers in the installed version. Joint states from visualization are not hardware feedback.
