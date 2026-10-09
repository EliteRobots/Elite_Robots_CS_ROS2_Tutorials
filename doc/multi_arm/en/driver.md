# 2. Complete dual-arm driver launch

Save the following complete content as `dual_arm_control.launch.py` in any
directory:

{download}`dual_arm_control.launch.py <../examples/dual_arm_control.launch.py>`

````{only} not latex

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

This template provides:

- Two independent controller managers.
- An independent TF/joint prefix for each arm.
- Two independent communication-port groups.
- Automatic generation of controller YAML files.
- Sequential controller startup for each arm.
- One final green `All required controllers are ready.` message.

The default IP addresses, robot models, and ports can all be overridden with
launch arguments; no Python-file edits are required.

For five-axis models such as `cs520h`, the template automatically selects the
five-axis controller configuration and joint list for that arm.

Note: fake hardware mock interfaces do not provide GPIO command interfaces, so
`io_and_status_controller` may be shown as `inactive` during fake tests. This
is a known fake-hardware limitation, not a dual-arm namespace or trajectory
controller failure. On real hardware, this controller should activate when the
corresponding interfaces are available.
