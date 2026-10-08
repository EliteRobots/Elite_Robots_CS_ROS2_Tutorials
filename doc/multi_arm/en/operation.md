# Troubleshooting and returning to single-arm operation

- Manager wait timeout: inspect namespaces, manager full names, generated YAML node keys, and the sourced installation.
- Action exists but rejects a goal: inspect active state, prefixes, five/six-axis counts, and timing fields.
- Fake IO is inactive: check missing mock resources and logs; independently verify trajectory controller state. Do not substitute the final log line for a state query.
- Physical robot does not enter external control: check each IP, reverse connection address, port set, remote mode, and task.

The template does not modify the single-arm entry point. After stopping dual-arm instances, single-arm operation remains available:

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

The single-arm default is `/controller_manager`, with controllers spawned by its own launch file.
