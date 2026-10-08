# Dual-arm driver template

## Save the complete launch file

Save as `~/dual_arm_launch/dual_arm_control.launch.py`, or download {download}`dual_arm_control.launch.py <../examples/dual_arm_control.launch.py>`. The file need not be installed into a ROS package; launch it directly by filename.

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

## Configuration generation and controller startup

The template reads the driver controller YAML for each arm's model. Models ending in `h` use `elite_cs_controllers_5f.yaml`; others use `elite_cs_controllers.yaml`. It qualifies top-level node keys with the arm's absolute names, replaces `$(var tf_prefix)` with its prefix, and writes a temporary file.

`PushRosNamespace` places single-arm nodes in their namespace. `controller_manager_name` addresses the correct manager. `spawn_controllers=false` disables the single-arm internal spawners so the wrapper can start controllers explicitly. The single-arm entry point also uses the corresponding manager key in the update rate YAML.

Within each arm, spawners run sequentially for joint states, IO, speed scaling, force/torque, TCP pose, scaled trajectories, direct position, and freedrive. The last two use `--inactive`; the others request activation. The two arms' startup chains are independent and may run concurrently.

```{important}
Sequencing uses `OnProcessExit` without checking the preceding exit code. Completion of arm2's last spawner does not mean arm1 has finished or that all controllers are active. The final log in this template only reports that the startup chain exited. Query both managers as described in the next chapter.
```

With fake hardware, GPIO command interfaces may not satisfy activation requirements and `io_and_status_controller` may remain inactive. Inspect logs and hardware interfaces to distinguish mock limitations from namespace errors. The same IO activation failure on physical hardware should not be treated as expected.

## Launch arguments

Override these defaults on the command line:

- `arm1_ip`, `arm2_ip`: `192.168.1.101`, `192.168.1.102`.
- `arm1_cs_type`, `arm2_cs_type`: both `cs63`, validated by each single-arm entry point.
- `use_fake_hardware`: `false`; shared by both arms in this template.
- `headless_mode`: `true`; shared by both arms.
- `controller_spawner_timeout`: `30` s; manager wait timeout, not a motion execution timeout.
- `arm1_reverse_port`, `arm1_script_sender_port`, `arm1_trajectory_port`, `arm1_script_command_port`: `50001`, `50002`, `50003`, `50004` respectively.
- Corresponding arm2 arguments start with `arm2_` and default to `50101`, `50102`, `50103`, `50104`.

Namespaces and joint prefixes are fixed in the template as arm1/arm1_ and arm2/arm2_; they are not overridable launch arguments. A third arm requires another arm group, unique prefix, IP, four ports, and a corresponding MoveIt instance.

Temporary YAML files use `NamedTemporaryFile(delete=False)` and are not removed automatically at shutdown. Retain them for debugging and clean them up once no longer used. Text substitutions depend on the current YAML structure; recheck generated output after changing custom file structures.
