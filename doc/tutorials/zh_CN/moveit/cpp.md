# 编写 MoveIt 2 C++ 程序

## 创建包与声明依赖

`hello_moveit` 演示从应用程序设置目标并请求规划。前面复制的示例已包含这个包；从零创建时，可在尚无同名包的工作空间 `src` 下执行：

```bash
ros2 pkg create --build-type ament_cmake \
  --dependencies moveit_ros_planning_interface rclcpp geometry_msgs \
  --node-name hello_moveit hello_moveit
```

`moveit_ros_planning_interface` 提供客户端 API，`rclcpp` 提供 ROS 节点与执行器，`geometry_msgs` 定义位姿。将下面程序保存为 `src/hello_moveit.cpp`，并让 CMake 安装可执行文件及 launch：

{download}`下载完整文件 <../../examples/moveit/hello_moveit/CMakeLists.txt>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/CMakeLists.txt
:language: cmake
:lines: 25-43
```

```{raw} latex
\end{minipage}\par\medskip
```
````


配套 `package.xml` 还声明启动文件使用的 `moveit_configs_utils`、`launch_ros` 和工作单元 MoveIt 配置包依赖。从零创建时也需补齐这些依赖及配套 launch 文件。

## 完整程序

{download}`下载完整文件 <../../examples/moveit/hello_moveit/src/hello_moveit.cpp>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/src/hello_moveit.cpp
:language: cpp
:lines: 73-79
```

```{raw} latex
\end{minipage}\par\medskip
```
````


## 节点、执行器与模型参数

`rclcpp::init` 初始化 ROS，节点启用自动声明参数选项，接收 launch 注入的机器人模型参数。执行器在独立线程处理状态与动作回调，主线程调用规划接口；退出时取消执行器并回收线程。

`MoveGroupInterface(node, "elite_arm")` 的组名必须与 SRDF 相同。程序明确指定 `world` 参考系和 `cs63_tool0` 末端，并等待当前关节状态。仅有模型文件、没有有效 `/joint_states` 时不能正确建立规划起点。

## 位姿目标与关节目标

位姿目标位置为 `(1.3, 0.3, 1.5)` m，参考系为 `world`。四元数 `(x,y,z,w)=(0,0,0,1)` 表示单位旋转，四个分量全零不是合法姿态。目标是否可达由当前模型和碰撞场景决定。

`setPoseTarget` 设置目标，`plan` 计算轨迹，`execute` 将规划结果发给控制器。程序分别检查规划和执行返回值。第一段失败时停止后续目标，进程返回非零值。

第二段使用明确的关节名称和 rad 值设置目标，避免依赖隐含的关节顺序。`clearPoseTargets` 清除上一目标，每次规划前 `setStartStateToCurrentState` 获取实际起点。默认 `execute=false` 时，两次规划都从实际当前状态开始，不会把未执行的第一段终点当成第二段起点。

## 注入模型与运行

配套 launch 将工作单元 URDF、SRDF 和运动学参数直接传给客户端：

{download}`下载完整文件 <../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/hello_moveit/launch/hello_moveit.launch.py
:language: python
:lines: 25-29
```

```{raw} latex
\end{minipage}\par\medskip
```
````


这样客户端使用的模型与 `move_group` 一致。无需依赖是否开启了模型话题发布。

```bash
cd "$COLCON_WS"
colcon build --symlink-install --packages-select hello_moveit
source install/setup.bash
ros2 launch hello_moveit hello_moveit.launch.py execute:=false
```

运行前保持驱动、`move_group` 和 RViz 已按上一章启动。先观察计划和日志；需要执行已检查的教学目标时使用：

```bash
ros2 launch hello_moveit hello_moveit.launch.py execute:=true
```

```{figure} images/run_pose.png
:name: tutorial-moveit-run-pose
:width: 90%
:alt: 位姿目标规划的 RViz 显示示例。

位姿目标规划的 RViz 显示示例。
```

```{figure} images/run_joint.png
:name: tutorial-moveit-run-joint
:width: 90%
:alt: 关节目标规划的 RViz 显示示例。

关节目标规划的 RViz 显示示例。
```

截图用于展示规划结果的观察方式；当前姿态、标定及场景变化可能产生不同轨迹。`execute=true` 会向当前连接的控制器发送运动请求。

更完整的 API 学习可继续阅读 [MoveIt 2 Humble 教程](https://moveit.picknik.ai/humble/doc/tutorials/getting_started/getting_started.html)。

## 下载完整示例

- {download}`hello_moveit.zip <../../downloads/hello_moveit.zip>`：MoveIt C++ 示例包，包含源码、构建配置和启动文件。
- {download}`my_elite_robot_cell.zip <../../downloads/my_elite_robot_cell.zip>`：完整工作单元，包含 description、control、moveit_config 三个包及模型资源。

解压后分别得到 `hello_moveit/` 和 `my_elite_robot_cell/`，将两个目录放到同一个工作空间的 `src/` 下，按[准备工作空间](preparation.md)安装依赖并构建。

```{only} latex
压缩包可从本教程 HTML 版的本节下载。
```
