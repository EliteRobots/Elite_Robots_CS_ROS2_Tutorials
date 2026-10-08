# 接入 ros2_control 与机器人驱动

## 给工作单元添加控制信息

`my_elite_robot_cell_controlled.urdf.xacro` 先生成同一场景，再调用 `cs_ros2_control` 添加硬件插件和状态、指令接口：

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/urdf/my_elite_robot_cell_controlled.urdf.xacro
:language: xml
:lines: 73-75
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`robot_ip` 是机器人地址，`local_ip` 是计算机用于机器人回连的网卡地址。脚本和输入/输出配方来自 `elite_robots_driver/resources/`。`use_fake_hardware=true` 使用 `mock_components/GenericSystem`；false 使用 Elite 硬件插件。

场景与控制标签均使用 `cs63_` 前缀，否则控制器声明的关节与硬件导出的接口不匹配。`script_filename`、`input_recipe_filename`、`output_recipe_filename` 等参数名与驱动 launch 传入的 Xacro 参数一致。

## 包装驱动 launch

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_control/launch/start_robot.launch.py
:language: python
:lines: 25-42
```

```{raw} latex
\end{minipage}\par\medskip
```
````


包装入口包含 `elite_robots_driver/launch/elite_control.launch.py`，并设置自定义 `description_package` 和 `description_file`。`runtime_config_package` 保持为 `elite_robots_driver`，因此控制器插件配置和更新频率来自驱动包；控制器 YAML 中的 `$(var tf_prefix)` 会展开为 `cs63_`。

驱动从 `description_package/config/cs63/` 读取模型参数。示例的控制包 CMake 将描述包维护的 `config/` 安装到这个位置；显示和 MoveIt 从描述包读取同一源数据。修改后重新构建两个包，避免安装目录中出现不一致的副本。

本例启动入口只接受 `cs63`。使用其他机型需同时更新几何参数、SRDF、关节限制、控制器关节名和目标位姿，不能只改型号字符串。

## 标定数据

默认 `default_kinematics.yaml` 是名义模型参数。实体机器人可用 `elite_robots_calibration` 导出自己的标定数据：

```bash
ros2 launch elite_robots_calibration calibration_correction.launch.py \
  robot_ip:=192.168.1.200 target_filename:=/tmp/my_elite_robot_calibration.yaml
```

成功后核对输出文件，将其替换到描述包的 `config/cs63/default_kinematics.yaml`，再重新构建描述包和控制包：

```bash
cp /tmp/my_elite_robot_calibration.yaml \
  "$COLCON_WS/src/my_elite_robot_cell/my_elite_robot_cell_description/config/cs63/default_kinematics.yaml"
cd "$COLCON_WS"
colcon build --symlink-install --packages-select \
  my_elite_robot_cell_description my_elite_robot_cell_control
source install/setup.bash
```

重新启动驱动和 MoveIt，使两者读取同一组标定参数。当前驱动 launch 不声明 `kinematics_params_file` 覆盖参数；仅在包装 launch 中传入该名字不会应用标定。模型标定也不负责工具 TCP、负载或工作台安装位姿。

## 启动与检查

先启动 fake hardware，使用标准轨迹控制器：

```bash
ros2 launch my_elite_robot_cell_control start_robot.launch.py \
  use_fake_hardware:=true launch_rviz:=false \
  initial_joint_controller:=joint_trajectory_controller
```

在另一终端检查：

```bash
ros2 control list_controllers -c /controller_manager
ros2 topic echo /joint_states --once
ros2 action info /joint_trajectory_controller/follow_joint_trajectory
```

确认 `joint_state_broadcaster` 和 `joint_trajectory_controller` 为 active，关节状态包含六个 `cs63_` 名称，轨迹动作存在服务器。进程启动或 spawner 退出本身不代表控制器已就绪。

实体机器人使用下面的启动方式；替换两处 IP，并先完成机器人端外部控制准备：

```bash
ros2 launch my_elite_robot_cell_control start_robot.launch.py \
  use_fake_hardware:=false robot_ip:=192.168.1.200 local_ip:=192.168.1.100 \
  headless_mode:=false launch_rviz:=false \
  initial_joint_controller:=scaled_joint_trajectory_controller
```

`headless_mode=false` 时，在示教器运行含外部控制节点的程序；设为 true 时由驱动发送外部控制脚本，但仍需满足机器人运行条件。实体机器人应检查 `scaled_joint_trajectory_controller` 的 active 状态和对应动作服务器。
