# 使用 example 驱动双臂

## 获取 example

创建 `~/dual_arm_launch` 目录，用于保存示例 launch 文件：

```bash
mkdir -p ~/dual_arm_launch
cd ~/dual_arm_launch
```

下载 {download}`dual_arm_control.launch.py <../examples/dual_arm_control.launch.py>` 到该目录；也可以将本章末尾的完整代码保存为 `~/dual_arm_launch/dual_arm_control.launch.py`。此文件可按文件名直接 launch，无需安装到 ROS 包中。

下面分别给出 fake hardware 和实体双臂的启动方式，按使用场景选择其中一种。

## fake hardware 双臂

在已加载环境的终端中进入保存目录并启动：

```bash
cd ~/dual_arm_launch
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=true \
  headless_mode:=false \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

这只创建 mock 硬件，不连接机器人。模板使用缩放轨迹控制器；后续 MoveIt 也显式选择相同控制器，不沿用旧版单臂 fake 示例的标准控制器假设。

## 实体双臂

确认两台机器人地址及回连网络后，在同一保存目录启动：

```bash
ros2 launch dual_arm_control.launch.py \
  use_fake_hardware:=false \
  headless_mode:=true \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs63
```

IP 为示例，应替换为实际地址。无头模式直接发送外部控制脚本，需满足远程模式和机器人运行状态条件。若使用 `headless_mode=false`，分别在两台示教器的 ExternalControl 任务中配置 ROS 计算机地址以及对应 script sender 端口，并运行各自任务。

## 分别确认两台机械臂

另开终端加载环境，执行只读检查：

```bash
ros2 control list_controllers -c /arm1/controller_manager
ros2 control list_controllers -c /arm2/controller_manager
ros2 control list_hardware_interfaces -c /arm1/controller_manager
ros2 control list_hardware_interfaces -c /arm2/controller_manager
ros2 action list -t
ros2 topic echo /arm1/joint_states --once
ros2 topic echo /arm2/joint_states --once
```

确认每臂关节状态与缩放轨迹控制器 active，关节名具有对应前缀。六轴应有六个关节；`cs520h` 应有五个，没有 wrist_3_joint。前向位置和 freedrive 默认 inactive 是模板的预期配置。

轨迹动作分别为：

```text
/arm1/scaled_joint_trajectory_controller/follow_joint_trajectory
/arm2/scaled_joint_trajectory_controller/follow_joint_trajectory
```

两者类型均为 `control_msgs/action/FollowJointTrajectory`。向 arm1 发送目标时，joint_names 必须使用 `arm1_shoulder_pan_joint` 等前缀名称；arm2 使用 `arm2_`。位置单位为 rad，时间为相对轨迹起点的累计时间；数组必须与关节名称一一对应。

动作存在不等于机器人可运动。真机还需检查外部控制连接、任务状态、控制器激活状态及运动范围。本手册不执行运动验证，也不提供可直接套用到任意双臂布局的目标位置。

## example 如何驱动双臂

模板根据各臂型号读取驱动包的控制器 YAML。型号以 `h` 结尾时选用 `elite_cs_controllers_5f.yaml`，其他型号使用 `elite_cs_controllers.yaml`。它将顶层节点键改为该臂的绝对名称，并把 `$(var tf_prefix)` 替换为对应前缀，写入临时文件。

`PushRosNamespace` 为单臂节点加入 namespace。`controller_manager_name` 用于正确寻址管理器，`spawn_controllers=false` 关闭单臂内部 spawner，由包装模板显式启动控制器。单臂入口同时为 update rate YAML 使用对应管理器键。

每臂内部依次运行关节状态、IO、速度缩放、力矩、TCP 位姿、缩放轨迹、直接位置和自由拖动控制器的 spawner。后两个使用 `--inactive`，其他请求激活。两臂的启动链彼此独立，可以并行进行。

```{important}
串行启动通过 `OnProcessExit` 触发下一步，不检查前一步退出码。arm2 最后一个 spawner 退出也不代表 arm1 已完成，更不保证全部控制器 active。本模板末尾日志仅提示启动链退出，必须按本章前面的检查步骤查询两套管理器确认状态。
```

fake hardware 下 GPIO command interfaces 可能不满足激活要求，`io_and_status_controller` 可能为 inactive。应检查具体日志与硬件接口，区分 mock 功能缺失和命名空间配置错误。真机不应将同样的 IO 激活失败当作预期状态。

## 每台机械臂需要隔离的内容

```{list-table}
:header-rows: 1
:widths: 30 35 35

* - 项目
  - arm1
  - arm2
* - ROS namespace
  - `arm1`
  - `arm2`
* - 关节/TF 前缀
  - `arm1_`
  - `arm2_`
* - 控制器管理器
  - `/arm1/controller_manager`
  - `/arm2/controller_manager`
* - 默认控制器 IP
  - `192.168.1.101`
  - `192.168.1.102`
* - 默认型号
  - `cs63`
  - `cs63`
* - MoveIt 规划组
  - `arm1_cs_manipulator`
  - `arm2_cs_manipulator`
```

ROS namespace 隔离节点、服务、话题和动作；前缀隔离关节、连杆及硬件资源标识。两者需要同时配置。名称前缀不等同于空间变换；默认模型中的共同 `world` 根也不代表已经标定了两臂相对位置。

同一 ROS 计算机上的机器人通信端口也必须避免冲突。四类端口依次为 reverse、script sender、trajectory、script command：arm1 默认使用 50001～50004，arm2 默认使用 50101～50104。

## 如何配置 example

以下默认值可在命令行覆盖：

- `arm1_ip`、`arm2_ip`：`192.168.1.101`、`192.168.1.102`。
- `arm1_cs_type`、`arm2_cs_type`：均为 `cs63`，分别传给单臂入口校验。
- `use_fake_hardware`：`false`，本模板两臂共用此开关。
- `headless_mode`：`true`，两臂共用。
- `controller_spawner_timeout`：`30` s，等待管理器超时，不是运动执行超时。
- `arm1_reverse_port`、`arm1_script_sender_port`、`arm1_trajectory_port`、`arm1_script_command_port`：依次为 `50001`、`50002`、`50003`、`50004`。
- arm2 的同名端口参数以 `arm2_` 开头，依次为 `50101`、`50102`、`50103`、`50104`。

namespace 和关节前缀在模板中固定为 arm1/arm1_、arm2/arm2_，并非可覆盖的 launch 参数。扩展第三台机械臂时，需要同时添加 arm group、独立前缀、IP、四个端口和对应 MoveIt 实例。

临时 YAML 由 `NamedTemporaryFile(delete=False)` 创建，不会在启动结束时自动删除；调试时可保留用于核查，确认不再使用后再清理。模板的文本替换依赖当前 YAML 结构，自定义文件结构变更后应重新检查生成结果。

端口冲突时可完整覆盖两组端口：

```bash
ros2 launch dual_arm_control.launch.py \
  arm1_ip:=192.168.1.101 \
  arm2_ip:=192.168.1.102 \
  arm1_reverse_port:=51001 \
  arm1_script_sender_port:=51002 \
  arm1_trajectory_port:=51003 \
  arm1_script_command_port:=51004 \
  arm2_reverse_port:=51101 \
  arm2_script_sender_port:=51102 \
  arm2_trajectory_port:=51103 \
  arm2_script_command_port:=51104
```

不要在默认端口的驱动仍运行时重复启动第二套相同实例。端口、namespace 和节点名都应避免冲突。

`local_ip` 未由双臂包装模板单独暴露，沿用单臂入口的自动选择行为；多网卡环境若需为每臂指定回连地址，应在自定义包装文件中添加并传递对应参数。

## example 完整代码

````{only} html
```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
```
````

````{only} latex

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 1-32
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 33-64
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 65-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 97-128
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 129-160
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 161-192
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 193-224
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_arm_control.launch.py
:language: python
:lines: 225-229
```

```{raw} latex
\end{minipage}\par\medskip
```

````
