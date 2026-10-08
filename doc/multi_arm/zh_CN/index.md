# Elite Robots ROS 2 多机械臂使用手册

**艾利特智能机器人股份有限公司**

文档版本：**1.0.0** · 修订日期：**2026-10-08**

本手册通过两个独立的单臂实例组装双臂系统，介绍驱动隔离、控制器配置、启动检查以及可选的双实例 MoveIt。

```{rubric} 适用版本与验证范围
```

版本要求以以下 ROS 包的版本号为准：

```{list-table}
:header-rows: 1
:widths: 56 22 22

* - 版本依据包
  - Humble
  - Jazzy
* - `elite_robots`
  - `≥ 1.2.0`
  - `≥ 1.2.0`
* - `elite_robots_description`
  - `≥ 1.0.0`
  - `≥ 1.0.0`
```

本文完成源码与文档检查，未运行实体机器人、fake hardware 或 MoveIt 集成测试。Jazzy 对应版本尚未核对。本手册不采用旧版接口手册的 Driver 1.0.3 基线。

```{rubric} 阅读顺序
```

完成[使用前准备](overview.md)后，按[使用 example 驱动双臂](driver.md)获取示例、启动并检查，再阅读示例讲解和配置方法。需要规划时，按相同顺序阅读 [MoveIt example](moveit.md)。遇到问题时查看[常见问题与单臂回退](operation.md)。

```{toctree}
:maxdepth: 2
:numbered:
:caption: 目录

overview
driver
moveit
operation
changelog
```
