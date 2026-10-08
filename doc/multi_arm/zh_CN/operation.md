# 常见问题与单臂回退

- 管理器等待超时：检查 namespace、管理器全名、生成 YAML 的节点键，以及是否加载了正确的安装环境。
- 找到动作但拒绝目标：检查 active 状态、前缀、五轴/六轴数量及时间字段。
- fake IO 未激活：核对 mock 资源缺失及日志；分别确认轨迹控制器是否正常，勿用最后一行日志代替状态查询。
- 真机未进入外部控制：分别核对 IP、回连地址、端口、远程模式和各自任务。

模板不会修改单臂入口。停止双臂实例后仍可按单臂方式启动：

```bash
ros2 launch elite_robots_driver elite_control.launch.py \
  robot_ip:=192.168.1.101 \
  cs_type:=cs63
```

单臂默认使用 `/controller_manager`，由其 launch 自己启动控制器。
