# 6. 单臂启动不受影响

```{code-block} bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

单臂默认使用 `/controller_manager`，并由单臂 launch 自己启动控制器。
