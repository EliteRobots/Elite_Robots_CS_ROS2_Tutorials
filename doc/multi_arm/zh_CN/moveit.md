# 5. 完整双臂 MoveIt launch

使用 MoveIt 时，在任意目录创建：

{download}`dual_moveit.launch.py <../examples/dual_moveit.launch.py>`

下面是可以直接复制的完整代码。示例默认使用 `cs63`，并为两台机械臂自动生成
独立的 MoveIt controller、kinematics 和 RViz 临时配置：

````{only} not latex

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

使用虚拟的双臂：

```{code-block} bash
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  launch_rviz:=true
```

如果某台机械臂是五轴型号，可设置 `arm1_cs_type:=cs520h` 或
`arm2_cs_type:=cs520h`，模板会自动选择五轴 MoveIt 控制器列表。真机则使用
`use_fake_hardware:=false`。启动顺序是先启动第 2 节的
`dual_arm_control.launch.py`，再启动：

```{code-block} bash
ros2 launch dual_moveit.launch.py
```
