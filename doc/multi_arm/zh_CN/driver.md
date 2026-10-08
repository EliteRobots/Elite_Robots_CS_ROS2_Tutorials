# 双臂驱动模板

## 保存完整 launch 文件

保存为 `~/dual_arm_launch/dual_arm_control.launch.py`，或下载 {download}`dual_arm_control.launch.py <../examples/dual_arm_control.launch.py>`。此文件不需要安装到 ROS 包中，可按文件名直接 launch。

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

## 配置生成与控制器启动

模板根据各臂型号读取驱动包的控制器 YAML。型号以 `h` 结尾时选用 `elite_cs_controllers_5f.yaml`，其他型号使用 `elite_cs_controllers.yaml`。它将顶层节点键改为该臂的绝对名称，并把 `$(var tf_prefix)` 替换为对应前缀，写入临时文件。

`PushRosNamespace` 为单臂节点加入 namespace。`controller_manager_name` 用于正确寻址管理器，`spawn_controllers=false` 关闭单臂内部 spawner，由包装模板显式启动控制器。单臂入口同时为 update rate YAML 使用对应管理器键。

每臂内部依次运行关节状态、IO、速度缩放、力矩、TCP 位姿、缩放轨迹、直接位置和自由拖动控制器的 spawner。后两个使用 `--inactive`，其他请求激活。两臂的启动链彼此独立，可以并行进行。

```{important}
串行启动通过 `OnProcessExit` 触发下一步，不检查前一步退出码。arm2 最后一个 spawner 退出也不代表 arm1 已完成，更不保证全部控制器 active。本模板末尾日志仅提示启动链退出，必须按下一章查询两套管理器确认状态。
```

fake hardware 下 GPIO command interfaces 可能不满足激活要求，`io_and_status_controller` 可能为 inactive。应检查具体日志与硬件接口，区分 mock 功能缺失和命名空间配置错误。真机不应将同样的 IO 激活失败当作预期状态。

## 启动参数

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
