# MoveIt 2：自定义工作单元与运动规划

完成本教程后，你将得到一个包含桌子、显示器、墙体和 CS63 的工作单元，以及对应的控制配置、MoveIt 配置和 C++ 客户端。

数据流为：Xacro 生成 URDF；驱动读取 URDF 中的 `ros2_control` 配置并发布关节状态；MoveIt 结合 URDF、SRDF、运动学和碰撞场景规划轨迹，再通过 `FollowJointTrajectory` 动作交给控制器。

## 下载完整示例

- {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>`：MoveIt C++ 示例包，包含源码、构建配置和启动文件。
- {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`：完整工作单元，包含 description、control、moveit_config 三个包及模型资源。

解压后分别得到 `hello_moveit/` 和 `my_elite_robot_cell/`，将两个目录放到同一个工作空间的 `src/` 下，按[准备工作空间](preparation.md)安装依赖并构建。

```{only} latex
压缩包可从本教程 HTML 版的本节下载。
```

## 工作单元中的四个包

- `my_elite_robot_cell_description`：场景几何、机器人安装变换、模型参数和显示入口。
- `my_elite_robot_cell_control`：带 `ros2_control` 的描述文件和驱动启动入口。
- `my_elite_robot_cell_moveit_config`：规划组、碰撞矩阵、求解器、关节限制、控制器映射及 MoveIt 启动入口。
- `hello_moveit`：设置位姿和关节目标、请求规划并按需执行的 C++ 程序。

这些名称是教程示例包名；底层驱动、模型和控制器分别来自 `elite_robots_driver`、`elite_robots_description` 和 `elite_robots_controllers`。

先准备工作空间，再按建模、控制、规划配置和编程的顺序完成各章。只显示模型时无需启动驱动；执行轨迹时，驱动与 MoveIt 必须同时就绪。

```{toctree}
:maxdepth: 2

preparation
workcell
control
configuration
cpp
```
