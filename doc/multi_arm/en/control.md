# 4. Check and control

Run the following command to display the controllers for arm1:

```{code-block} bash
ros2 control list_controllers -c /arm1/controller_manager
```

Run the following command to display the controllers for arm2:

```{code-block} bash
ros2 control list_controllers -c /arm2/controller_manager
```

Run the following command to display the trajectory actions:

```{code-block} bash
ros2 action list | grep follow_joint_trajectory
```

The trajectory actions are:

```{code-block} text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

When sending a trajectory action, joint names must include the corresponding
prefix, for example `arm1_wrist_1_joint`.
