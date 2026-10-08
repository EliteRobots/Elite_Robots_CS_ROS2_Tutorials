# 创建与使用 MoveIt 配置

## 加载工作单元

```bash
ros2 launch moveit_setup_assistant setup_assistant.launch.py
```

选择创建配置，加载描述包中的 `urdf/my_elite_robot_cell.urdf.xacro`。使用默认 CS63 参数。该 URDF 包含整个工作单元，规划时才能检查机器人与桌子、显示器及墙体之间的碰撞。

```{figure} images/load_urdf.png
:name: tutorial-moveit-load-urdf
:width: 90%
:alt: 在 Setup Assistant 中加载工作单元 Xacro。

在 Setup Assistant 中加载工作单元 Xacro。
```

配图中的路径和界面可能与本机版本不同，包名和文件以正文及配套示例为准。已复制配置包时可直接使用，或从 Setup Assistant 打开现有包继续修改；生成新包时使用独立目录，避免覆盖尚未保存的配置。

## 自碰撞矩阵

生成 Self-Collisions 矩阵，并检查被禁用的连杆对。

```{figure} images/self_collisions.png
:name: tutorial-moveit-self-collisions
:width: 90%
:alt: 生成并检查自碰撞矩阵。

生成并检查自碰撞矩阵。
```

`Adjacent` 表示相邻连杆，`Never` 是采样过程中未观察到碰撞。采样结果并非对所有姿态的证明。修改桌面高度、障碍物或机器人安装位置后，应重新生成并审查矩阵，尤其检查机器人与环境物体的排除项。不要通过禁用碰撞检查来掩盖错误的模型或起始姿态。

## 规划组和末端连杆

工作单元已经通过固定关节连接到 `world`，此例无需再增加虚拟关节。在 Planning Groups 创建 `elite_arm`，求解器选择 `kdl_kinematics_plugin/KDLKinematicsPlugin`。

```{figure} images/planning_group_kinematics.png
:name: tutorial-moveit-planning-group-kinematics
:width: 90%
:alt: 为 elite_arm 选择运动学求解器。

为 elite_arm 选择运动学求解器。
```

将运动学链的 base link 设为 `cs63_base_link`、tip link 设为 `cs63_tool0`。

```{figure} images/planning_group_chain.png
:name: tutorial-moveit-planning-group-chain
:width: 90%
:alt: 添加机械臂运动学链。

添加机械臂运动学链。
```

```{figure} images/planning_group_links.png
:name: tutorial-moveit-planning-group-links
:width: 90%
:alt: 确认运动学链的起止连杆。

确认运动学链的起止连杆。
```

可添加仅包含 `cs63_tool0` 的连杆组。该组用于语义组织，不等于配置了真实夹爪、TCP 偏置或夹爪控制器。

```{figure} images/planning_group_tool.png
:name: tutorial-moveit-planning-group-tool
:width: 90%
:alt: 添加末端连杆组。

添加末端连杆组。
```

```{figure} images/planning_groups.png
:name: tutorial-moveit-planning-groups
:width: 90%
:alt: 完成后的规划组列表。

完成后的规划组列表。
```

SRDF 中的核心定义是：

```xml
<group name="elite_arm">
  <chain base_link="cs63_base_link" tip_link="cs63_tool0"/>
</group>
```

## 控制器与生成文件

控制包已负责 `ros2_control`，在助手中跳过重复的硬件配置。实体机器人在 MoveIt Controllers 添加 `scaled_joint_trajectory_controller`，类型为 `FollowJointTrajectory`，关节列表与 URDF 一致。

```{figure} images/moveit_controllers.png
:name: tutorial-moveit-moveit-controllers
:width: 90%
:alt: 配置 MoveIt 轨迹控制器。

配置 MoveIt 轨迹控制器。
```

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml
:language: yaml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/moveit_controllers.yaml
:language: yaml
:lines: 1-19
```

```{raw} latex
\end{minipage}\par\medskip
```
````


该 YAML 告诉 MoveIt 动作服务器在哪里；它不会加载或激活 ros2_control 控制器。动作名称由控制器名和 `action_ns` 拼接，实体机器人对应 `/scaled_joint_trajectory_controller/follow_joint_trajectory`。fake hardware 使用另一个 `moveit_controllers_fake.yaml`，控制器名为 `joint_trajectory_controller`。

跳过 Perception。Launch Files 选择 RViz Launch and Config、MoveGroup Launch 和 Setup Assistant Launch；控制包已负责状态发布和硬件启动，无需生成重复的 demo 启动链。本例不使用 Warehouse。

```{figure} images/launch_files.png
:name: tutorial-moveit-launch-files
:width: 90%
:alt: 选择需要生成的启动文件。

选择需要生成的启动文件。
```

填写作者信息，生成配置包 `my_elite_robot_cell_moveit_config`，保留 SRDF、运动学、关节限制和控制器文件。

```{figure} images/config_files.png
:name: tutorial-moveit-config-files
:width: 90%
:alt: 生成工作单元 MoveIt 配置包。

生成工作单元 MoveIt 配置包。
```

## 关节限制与时间参数化

URDF 的位置和速度限制不能代替 MoveIt 的加速度配置。示例在 `config/joint_limits.yaml` 中为六轴指定加速度上限，并将默认速度、加速度缩放设为 0.1：

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/config/joint_limits.yaml
:language: yaml
:lines: 25-36
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`max_velocity` 单位为 rad/s，`max_acceleration` 为 rad/s²。这里的 `4.0` 是教学示例的规划值，不是制造商认证的硬件上限；应按实际负载、姿态和工艺确定。较低缩放会增加加减速时间，较高值不保证实际执行更快。

这些参数用于 MoveIt 的轨迹时间参数化，不替代控制器或机器人自身限制，也不会自动约束绕过 MoveIt 发送的轨迹。

## 启动规划与 RViz

`move_group.launch.py` 根据 `use_fake_hardware` 选择对应的控制器文件，并明确使用 OMPL：

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_moveit_config/launch/move_group.launch.py
:language: python
:lines: 25-31
```

```{raw} latex
\end{minipage}\par\medskip
```
````


这个参数在此处只选择 MoveIt 控制器映射；硬件必须由上一章的控制 launch 启动。

在已经启动 fake hardware 的基础上，分别在两个已加载工作空间的终端执行：

```bash
ros2 launch my_elite_robot_cell_moveit_config move_group.launch.py \
  use_fake_hardware:=true
```

```bash
ros2 launch my_elite_robot_cell_moveit_config moveit_rviz.launch.py
```

实体机器人对应 `use_fake_hardware:=false`，与驱动选择的 scaled 控制器配对。`You can start planning now!` 表示规划节点启动，执行前仍需检查关节状态及动作服务器。

在 RViz 的 MotionPlanning 面板选择 `elite_arm`，设置起点为当前状态，拖动目标标记后点击 Plan，检查轨迹与环境的关系，再按需执行。规划成功与执行成功是两个独立结果。

## 排查方法

- 模型或 SRDF 加载失败：检查工作空间顺序、包安装和 `.setup_assistant` 中的路径。
- 不能获取当前状态：检查 `/joint_states` 是否持续更新、六个关节名是否一致，以及是否误用了仿真时钟。
- 起点碰撞或目标不可达：核对 `world` 安装变换、起始姿态、目标坐标系和碰撞几何。
- 规划成功但无法执行：核对控制器 active 状态、动作名称及 fake/实体两端配置是否匹配。
- 校准后显示与实际不一致：确认两个示例包已重新构建，驱动、MoveIt 和客户端已重新启动。
