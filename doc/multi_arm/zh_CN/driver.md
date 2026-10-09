# 2. 完整双臂驱动 launch

将下面内容完整保存在 `dual_arm_control.launch.py`：

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

这个模板已经包含：

- 两个独立的 controller manager
- 每台机械臂独立的 TF/joint prefix
- 两组独立通信端口
- 控制器 YAML 自动生成
- 每台机械臂内部按顺序启动控制器
- 最后输出一次绿色的 `All required controllers are ready.`

默认 IP、型号和端口都可以通过启动参数覆盖，不需要修改 Python 文件。

对于 `cs520h` 等五轴型号，模板会自动选择该机械臂对应的五轴控制器配置和关节列表。

注意：fake hardware 的 mock 接口不提供 GPIO command interfaces，因此
`io_and_status_controller` 在 fake 测试中可能显示为 `inactive`；这不是双臂
namespace 或轨迹控制器错误。真机运行时该控制器应按实际硬件接口正常激活。
