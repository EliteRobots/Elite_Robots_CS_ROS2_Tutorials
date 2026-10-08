# 准备工作空间

## 环境与前提

准备 ROS 2 Humble、MoveIt 2、已构建的 Elite 驱动和模型包。需要熟悉 ROS 包、launch、URDF/Xacro 及工作空间的 `build`/`install` 目录。基础模型知识可参考 [ROS 2 URDF 教程](https://docs.ros.org/en/humble/Tutorials/Intermediate/URDF/URDF-Main.html)。

在每个新终端先加载 ROS 和驱动工作空间；将 `/path/to/driver_ws` 换成实际路径：

```bash
source /opt/ros/humble/setup.bash
source /path/to/driver_ws/install/setup.bash
ros2 pkg prefix elite_robots_description
ros2 pkg prefix elite_robots_driver
ros2 pkg prefix elite_robots_moveit_config
```

三个查询都应返回安装前缀。仓库目录名不等于 ROS 包名，命令中使用 `package.xml` 声明的名称。

## 获取示例并构建

下载 {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>` 和 {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`。以下命令假设文件保存在 `~/Downloads/`，请按实际下载位置调整。目标工作空间的 `src` 应尚未包含同名包：

```bash
export COLCON_WS=~/workspaces/elite_tutorials
mkdir -p "$COLCON_WS/src"
unzip ~/Downloads/hello_moveit.zip -d "$COLCON_WS/src"
unzip ~/Downloads/my_elite_robot_cell.zip -d "$COLCON_WS/src"
cd "$COLCON_WS"
rosdep install --from-paths src --ignore-src -r -y --rosdistro humble
colcon build --symlink-install
source install/setup.bash
```

如果已经取得本教程文档仓库，也可在仓库根目录直接复制示例：

```bash
export COLCON_WS=~/workspaces/elite_tutorials
mkdir -p "$COLCON_WS/src"
cp -r doc/tutorials/examples/moveit/hello_moveit "$COLCON_WS/src/"
cp -r doc/tutorials/examples/moveit/my_elite_robot_cell "$COLCON_WS/src/"
```

复制后执行上面的依赖安装和构建命令。

若 rosdep 提示找不到 Elite 包，先检查驱动工作空间是否加载、所需包是否安装。教程使用驱动已有的控制器插件，不需要在示例中重复构建 SDK。

若使用安装后的文档包，可将示例根目录定位为 `$(ros2 pkg prefix elite_robots_cs_tutorials)/share/elite_robots_cs_tutorials/doc/tutorials/examples/moveit`，再复制其中的两个目录。

后续每个终端都需要加载 ROS、驱动工作空间和 `$COLCON_WS/install/setup.bash`。修改 Xacro、YAML 或 launch 后重新构建并加载；C++ 源码修改必须重新编译。

## 示例约定

所有模型、SRDF、YAML 和程序使用同一组六轴关节及 `cs63_` 前缀；`elite_arm` 从 `cs63_base_link` 延伸到 `cs63_tool0`。示例中的位姿以 `world` 为参考系，位置单位为 m，关节角为 rad，加速度为 rad/s²。

先使用 fake hardware 完成配置检查；它只回显指令，不模拟动力学。fake hardware 使用系统时钟，`use_sim_time` 保持 false。此工作单元没有 Gazebo、相机或在线环境感知。

切换实体机器人前，确认工作单元几何、安装位姿、负载和工具与实际一致，并完成机器人端的网络与外部控制配置。示例目标是教学用配置，能否规划和执行取决于实际起点、关节范围和碰撞场景。
