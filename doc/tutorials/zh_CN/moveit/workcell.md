# 组装工作单元模型

## 顶层描述与宏

`my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro` 是模型入口。它包含工作单元宏，声明型号和四份参数文件，创建 `world` 连杆，再实例化场景。

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro
:language: xml
:lines: 25-25
```

```{raw} latex
\end{minipage}\par\medskip
```
````


`xacro:include` 只引入定义；`xacro:my_elite_robot_cell` 才生成实际的连杆与关节。四份 YAML 分别提供关节限制、几何运动学、物理属性和可视化资源。示例将 CS63 参数放在描述包的 `config/cs63/` 中，使显示、控制与规划共用同一套几何数据。

调用中的 `<origin xyz="0 0 1" .../>` 是传给宏的 XML 块，对应 `*origin` 和 `xacro:insert_block`。它将桌子的参考连杆放到 `world` 上方 1 m，并不直接等于机械臂底座的位置。

## 建立场景和安装关系

完整的工作单元宏如下：

{download}`下载完整文件 <../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro>`

````{only} html
```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
```
````

````{only} latex
```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 1-24
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 25-48
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 49-72
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 73-96
```

```{raw} latex
\end{minipage}\par\medskip
```

```{raw} latex
\par\noindent\begin{minipage}{\linewidth}
```

```{literalinclude} ../../examples/moveit/my_elite_robot_cell/my_elite_robot_cell_description/urdf/my_elite_robot_cell_macro.xacro
:language: xml
:lines: 97-105
```

```{raw} latex
\end{minipage}\par\medskip
```
````


桌子和显示器使用 DAE 网格作为可视和碰撞几何；墙体使用网格显示、长方体碰撞几何。`visual` 决定外观，`collision` 决定规划中的碰撞检查，两者应表达同一个实际障碍物。

桌子通过 `table_base_joint` 固定在父连杆上。显示器、墙体和 `robot_mount` 通过固定关节连接到桌子；本例 `robot_mount` 相对桌子偏移为 `(1.0, 0.5, 0)` m。因此在默认无旋转安装下，机械臂安装点相对 `world` 为 `(1.0, 0.5, 1.0)` m。

`cs_robot` 来自 `elite_robots_description/urdf/cs_macro.xacro`，其 `parent` 必须是已经存在的连杆。传入 `tf_prefix="cs63_"` 后，机器人关节与连杆分别形如 `cs63_shoulder_pan_joint` 和 `cs63_base_link`。前缀必须与 SRDF、控制器和应用程序一致。

这里设置 `generate_ros2_control_tag="false"`，只生成机器人几何；下一章会在控制描述中添加一次控制标签，避免重复声明硬件。

## 检查模型

```bash
ros2 launch my_elite_robot_cell_description view_robot.launch.py
```

RViz 的 Fixed Frame 为 `world`。用 `joint_state_publisher_gui` 的滑块改变显示姿态，检查安装高度、朝向和各关节连接。这些滑块只发布显示用关节状态。

```{figure} images/view_workspace.png
:name: tutorial-moveit-view-workspace
:width: 90%
:alt: 包含桌子、显示器、墙体和 CS63 的工作单元。

包含桌子、显示器、墙体和 CS63 的工作单元。
```

也可离线展开 Xacro，检查生成的 XML：

```bash
xacro "$(ros2 pkg prefix my_elite_robot_cell_description)/share/my_elite_robot_cell_description/urdf/my_elite_robot_cell.urdf.xacro" \
  > /tmp/my_elite_robot_cell.urdf
check_urdf /tmp/my_elite_robot_cell.urdf
```

模型应只有一个根连杆 `world` 和六个可动关节。若资源找不到，检查 `package://` 路径对应的包是否安装，以及 `meshes`、`config`、`urdf` 是否由 CMake 安装。

结束显示检查后关闭该 launch，再启动驱动，避免 GUI 与驱动同时向 `/joint_states` 发布不同状态。
