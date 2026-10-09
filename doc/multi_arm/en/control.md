# 4. Check and control

```{code-block} bash
ros2 control list_controllers -c /arm1/controller_manager
ros2 control list_controllers -c /arm2/controller_manager
ros2 action list | grep follow_joint_trajectory
```

The trajectory actions are:

```{code-block} text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

When sending a trajectory action, joint names must include the corresponding
prefix, for example `arm1_wrist_1_joint`.
