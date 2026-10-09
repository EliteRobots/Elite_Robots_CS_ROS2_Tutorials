# 5. Complete dual-arm MoveIt launch (optional)

If MoveIt is not needed, stop after Section 4. To use MoveIt, create the
following file in any directory:

{download}`dual_moveit.launch.py <../examples/dual_moveit.launch.py>`

The following complete code can be copied directly. It defaults to `cs63` and
automatically generates independent MoveIt controller, kinematics, and RViz
temporary configuration files for both arms:

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

Fake dual-arm MoveIt startup:

```{code-block} bash
ros2 launch dual_moveit.launch.py \
  use_fake_hardware:=true \
  launch_rviz:=true
```

Use `arm1_cs_type:=cs520h` or `arm2_cs_type:=cs520h` for a five-axis arm; its
five-axis MoveIt controller list is selected automatically. For real hardware,
use `use_fake_hardware:=false`. Start the Section 2
`dual_arm_control.launch.py` first, then run:

```{code-block} bash
ros2 launch dual_moveit.launch.py
```
