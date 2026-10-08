# Elite Robots ROS 2 多机械臂使用手册

**艾利特智能机器人股份有限公司**

文档版本：**1.0.0** · 修订日期：**2026-10-08**

本手册通过两个独立的单臂实例组装双臂系统，介绍驱动隔离、控制器配置、启动检查以及可选的双实例 MoveIt。附带完整 launch 文件，可在工作空间编译并加载环境后，从任意目录启动。

```{rubric} 适用版本与验证范围
```

本版依据 ROS 2 Humble 对应源码核对：Driver 仓库软件包 **1.2.0**，Description **1.0.0**。需要单臂入口提供 `controller_manager_name`、`spawn_controllers`，以及 MoveIt 的 `kinematics_file`、`rviz_config_file`、`prefer_scaled_controller` 等参数。仅有包名相同或较旧的接口手册，不能证明安装版本具备这些能力。

本文完成源码与文档检查，未运行实体机器人、fake hardware 或 MoveIt 集成测试。Jazzy 对应版本尚未核对。本手册不采用旧版接口手册的 Driver 1.0.3 基线。

```{rubric} 阅读顺序
```

先阅读[准备与隔离原则](overview.md)，保存[双臂驱动模板](driver.md)，按[启动与检查](operation.md)启动；需要规划时再添加 [MoveIt 模板](moveit.md)。

```{toctree}
:maxdepth: 2
:numbered:
:caption: 目录

overview
driver
operation
moveit
changelog
```
