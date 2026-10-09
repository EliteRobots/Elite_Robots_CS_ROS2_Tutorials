# 6. Single-arm startup remains unchanged

```{code-block} bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

Single-arm startup still uses `/controller_manager`, and the single-arm launch
file starts its controllers itself.
