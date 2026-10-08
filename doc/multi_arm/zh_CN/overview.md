# 使用前准备

## 方案范围

双臂驱动模板两次包含 `elite_robots_driver/launch/elite_control.launch.py`，为每台机械臂启动独立控制器管理器。可选 MoveIt 模板两次包含 `elite_moveit.launch.py`，各自规划并执行本机械臂的轨迹。

此方案不创建包含两台机械臂的统一机器人模型、联合规划组或同步执行器。两套独立规划场景不会自动感知另一台机械臂；namespace 和前缀也不会自动设置两台机械臂在工作区中的实际安装位置。共享工作空间内的协同运动需要另外建立一致的基座变换、完整碰撞模型及执行协调机制。

## 环境与文件

正确安装艾利特机器人的 ROS 2 驱动（如果还未安装，可以参考快速手册的相关章节进行安装）。后续操作使用的每个终端均需加载 ROS 与工作空间环境。

安装版本检查（只显示参数，不启动机器人）：

```bash
ros2 launch elite_robots_driver elite_control.launch.py --show-args
ros2 launch elite_robots_moveit_config elite_moveit.launch.py --show-args
```

驱动入口必须支持命名空间内的配置键、控制器配置绝对路径、指定管理器和关闭内部 spawner。MoveIt 入口必须支持自定义配置绝对路径，并将 prefix 同时传给 URDF 的 tf_prefix 与 SRDF。若缺少这些能力，应先更新相应源码和安装环境，不能只复制包装模板。

## 场景区别

- 实体机器人：两台控制器地址均应可达，并能回连 ROS 计算机；无头模式下按机器人配置启用远程控制。
- ELIBOTSim：使用两个独立模拟控制器的可达地址，并满足相同的回连及端口条件；不要把两台机械臂都指向同一个控制器实例。
- fake hardware：不连接机器人，用于关节与命名空间集成；它不是完整控制柜模拟器。
