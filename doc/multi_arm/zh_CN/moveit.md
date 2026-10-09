# 双臂 MoveIt 使用指南

## 准备示例文件

需要 MoveIt 规划与执行时，下载 {download}`dual_moveit.launch.py <../examples/dual_moveit.launch.py>` 到前面创建的 `~/dual_arm_launch` 目录；也可以将本章末尾的完整代码保存为 `~/dual_arm_launch/dual_moveit.launch.py`。该示例启动两个独立的 MoveIt 实例，分别控制各自机械臂。

## 启动 MoveIt

先按[驱动章节](driver.md)启动双臂驱动并确认两套轨迹控制器，再开终端加载 ROS 与工作空间环境：

```bash
cd ~/dual_arm_launch
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  launch_rviz:=true
```

上面用于 fake 场景。真机场景使用默认 `use_fake_hardware=false`：

```bash
ros2 launch dual_moveit.launch.py
```

## 确认规划与执行目标

```bash
ros2 node info /arm1/move_group
ros2 node info /arm2/move_group
ros2 action list -t
```

在每个 RViz 中选择对应的规划组，检查 Move Group Namespace、关节反馈及机器人型号。执行前再次确认其控制器目标指向本臂，而不是另一臂或根 namespace。规划成功不等于控制器可执行。

若 RViz 未显示预期内容，检查生成的临时配置是否包含正确的组名、namespace 和 display_planned_path 路径；字符串替换依赖当前包内 RViz 模板内容。末端位姿、TF 和模型基座位置仍需与实际安装关系一致。

## MoveIt 配置的适配原理

模板为每臂生成三个临时配置：

1. 控制器列表：按五轴/六轴选择 `controllers_5f.yaml` 或 `controllers.yaml`，给关节名添加前缀。控制器名称保持相对名称，由 MoveIt 所在 namespace 定位到对应动作。
2. 运动学配置：将 `cs_manipulator` 改为 `arm1_cs_manipulator` 或 `arm2_cs_manipulator`，匹配带前缀的 SRDF 规划组。
3. RViz 配置：设置各自 Planning Group、Move Group Namespace 和轨迹显示话题。

`prefer_scaled_controller=true` 让 fake 与真机都优先使用缩放轨迹控制器，匹配驱动模板。单臂入口中的 `use_fake_hardware` 在这里用于 MoveIt 执行映射，不会启动硬件；硬件仍由双臂驱动负责。`launch_servo=false` 明确关闭 Servo。

模板没有合并两臂规划场景，也没有为 OMPL 或关节限制 YAML 做完整的多臂改写；它仅生成上述三个文件。需要特定规划器或每关节覆盖限制时，应检查规划组/关节名与自定义配置的匹配，不应假定所有单臂配置都自动添加了前缀。

## 参数与配置说明

参数 `arm1_cs_type`、`arm2_cs_type` 默认均为 `cs63`；必须与驱动保持一致。五轴示例（驱动中的 arm2 也需选择同一型号）：

```bash
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  arm1_cs_type:=cs63 \
  arm2_cs_type:=cs520h
```

`launch_rviz` 默认 true，对两个实例同时生效，可设为 false 关闭两个 RViz。此方案仍使用系统时间。

## 完整示例代码

````{only} html
```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
```
````

````{only} latex

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 1-32
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 33-64
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 65-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 97-128
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../examples/dual_moveit.launch.py
:language: python
:lines: 129-147
```

```{raw} latex
\end{minipage}\par\medskip
```

````
