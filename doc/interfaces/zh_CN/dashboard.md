# 机器人管理与脚本接口

## Dashboard 节点

默认节点名为 `dashboard_client`，服务均为 `~/...` 私有名称。独立入口：

```bash
ros2 run elite_robots_driver dashboard_client \
  --ros-args -p robot_ip:=<robot_ip>
```

通常由驱动 launch 的组件进程启动，不需要重复运行独立节点。独立节点的 `robot_ip` 默认 `192.168.51.244`，该值只是代码默认值，使用时应显式填写实际控制器地址。改变参数本身不会自动建立新连接；`connect` 回调读取当前参数后连接。

服务响应只反映命令或查询的返回。上电、释放抱闸、播放任务等请求应结合机器人模式、安全状态和任务状态继续确认。

## Dashboard 服务目录

### Trigger 服务

以下类型均为 `std_srvs/srv/Trigger`，完整名称是 `/dashboard_client/<后缀>`。请求为空，响应为 `success`、`message`。

```{list-table}
:header-rows: 1
:widths: 40 60

* - 后缀
  - 功能
* - `power_on`
  - 机器人上电
* - `power_off`
  - 机器人断电
* - `brake_release`
  - 释放抱闸
* - `play`
  - 运行当前任务
* - `pause`
  - 暂停当前任务
* - `stop`
  - 停止当前任务
* - `shutdown`
  - 关闭控制器系统
* - `reboot`
  - 重启控制器系统
* - `unlock_protective_stop`
  - 请求解除保护停止
* - `close_safety_dialog`
  - 关闭安全提示对话框
* - `quit`
  - 退出 Dashboard 连接
* - `restart_safety`
  - 重启安全系统
* - `connect`
  - 按当前 `robot_ip` 连接 Dashboard
* - `get_task_path`
  - 查询当前任务路径；路径放在响应 `message` 中
```

`shutdown`、`reboot`、`quit` 的回调在 SDK 调用未抛异常时直接返回 true，不等待机器人完成关机、重启或状态转换。`get_task_path` 的 `message` 是查询数据，不应一律作为错误文本处理。

### 查询服务

- `/dashboard_client/get_task_status`：类型：`elite_robots_msgs/srv/GetTaskStatus`；成功响应数据：`status.status`。

- `/dashboard_client/robot_mode`：类型：`elite_robots_msgs/srv/GetRobotMode`；成功响应数据：`mode.mode`。

- `/dashboard_client/get_safety_mode`：类型：`elite_robots_msgs/srv/GetSafetyMode`；成功响应数据：`mode.mode`。

- `/dashboard_client/is_task_saved`：类型：`elite_robots_dashboard_msgs/srv/IsSaved`；成功响应数据：`is_saved`。

- `/dashboard_client/is_configuration_saved`：类型：`elite_robots_dashboard_msgs/srv/IsSaved`；成功响应数据：`is_saved`。


均为空请求，响应另有 `success`、`message`。先检查 `success`，再解析数据。任务状态是 ROS 常量：-1 未知、0 停止、1 暂停、2 运行；该节点已将 SDK 枚举映射为 ROS 定义，不能直接拿 SDK 数值与响应比较。

### 文件与交互服务

服务前缀 `/dashboard_client/`，类型包为 `elite_robots_dashboard_msgs`。

- `load_task`：类型：`srv/Load`；请求：`filename`；响应：`answer`、`success`。

- `load_configure`：类型：`srv/Load`；请求：`filename`；响应：`answer`、`success`。

- `popup`：类型：`srv/Popup`；请求：`arg`、`message`；响应：`success`、`message`。

- `log`：类型：`srv/Log`；请求：`message`；响应：`message`、`success`。

- `custom_request`：类型：`srv/CustomRequest`；请求：`request`；响应：`response`。


`filename` 指机器人控制器端的任务或配置文件路径，不是 ROS 计算机文件路径；服务不上传文件。`popup.arg` 原样传给 SDK，具体弹窗操作字符串由控制器协议决定，ROS 类型未定义合法字符串枚举。

`custom_request` 发送原始 Dashboard 命令并返回文本，没有 `success` 字段。SDK 异常文本也会写入 `response`，应用必须解析协议响应并区分错误，不应仅判断文本非空。

## Primary 节点

独立可执行名和默认节点名均为 `primary_client`，参数 `robot_ip` 默认 `192.168.51.244`，应显式指定。它通过 Primary 通道提供以下 `std_srvs/srv/Trigger` 服务：

```text
/primary_client/power_on
/primary_client/power_off
/primary_client/brake_release
/primary_client/pause
/primary_client/stop
/primary_client/unlock_protective_stop
/primary_client/restart_safety
/primary_client/connect
```

对应功能与名称一致，响应 `success` 来自 SDK 返回，异常时设为 false 并填写 `message`。没有 Primary `play`、`robot_mode` 或 `get_task_status` ROS 服务，不能把 Dashboard 目录整体替换前缀后使用。

与组件进程中的 Dashboard 不同，Primary 初始连接失败后节点仍加入执行器，`connect` 服务可用于再次连接。两种通道的控制器权限与状态要求仍由机器人端决定。

## 脚本发送节点

可执行名 `script_node`，默认节点名 `script_sender`，必需参数 `robot_ip`：

```bash
ros2 run elite_robots_driver script_node \
  --ros-args -p robot_ip:=<robot_ip>
```

订阅 `/script_sender/script_command`，类型 `std_msgs/msg/String`，队列深度 1。`data` 是完整脚本文本，保留换行与缩进，通过 Primary 通道发送。

本接口没有结果话题、服务响应或动作反馈；发送是否成功只能从本节点日志得知，执行效果需要独立观测。启动节点本身还会发送包含 `textmsg` 的连接提示脚本，因此它不是纯只读监视节点。

任意脚本可能改变或替换当前机器人任务；不要在轨迹控制执行中并行发送未经协调的运动脚本。本手册只提供接口定义，不提供会与外部控制脚本争用的运动脚本示例。
