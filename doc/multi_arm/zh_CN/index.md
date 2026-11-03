# 在本项目中组装多台 Elite 机械臂

文档版本：**1.0.0** · 修订日期：**2026-11-03** · 中文

文档版本独立于 ROS 包版本，变更内容见[修订记录](changelog.md)。

这份文档可以单独使用。下面两个 launch 文件可以在任意目录创建：

```{code-block} text
dual_arm_control.launch.py
dual_moveit.launch.py
```

将本文对应章节中的完整代码复制进去，进入文件所在目录即可直接按文件名启动：

```{code-block} bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py
ros2 launch dual_moveit.launch.py
```

驱动包提供可复用的单臂入口`elite_control.launch.py`，
双臂 launch 文件负责把它 include 两次，并为每台机械臂设置独立的
namespace、TF/joint prefix、controller manager、通信端口和控制器。

```{toctree}
:maxdepth: 2

launch_files
driver
startup
control
moveit
changelog
```
