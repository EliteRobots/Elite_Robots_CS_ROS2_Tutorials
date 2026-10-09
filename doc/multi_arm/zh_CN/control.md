# 4. 检查和控制

```{code-block} bash
ros2 control list_controllers -c /arm1/controller_manager
ros2 control list_controllers -c /arm2/controller_manager
ros2 action list | grep follow_joint_trajectory
```

轨迹 action 分别是：

```{code-block} text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

发送 action 时，joint 名称必须带对应 prefix，例如 `arm1_wrist_1_joint`。
