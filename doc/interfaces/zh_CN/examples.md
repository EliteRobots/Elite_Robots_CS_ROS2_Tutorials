# 客户端示例与接口自检

## 启动后的只读检查

下列命令假定已经加载 ROS 和工作空间环境，并启动对应驱动。本手册编写时没有实际连接机器人执行这些命令。

```bash
ros2 node list
ros2 control list_controllers
ros2 control list_hardware_interfaces
ros2 topic list -t
ros2 service list -t
ros2 action list -t
ros2 topic echo /joint_states --once
ros2 topic info /io_and_status_controller/io_states -v
```

检查关节名称和数量、控制器 active 状态、接口类型，以及反馈时间戳是否持续更新。`ros2 topic hz` 只反映观察到的频率，不能据此推导底层实时性保证。模式话题按变化发布，没有持续输出不一定表示断线。

## 查询机器人状态

```bash
ros2 service call /dashboard_client/robot_mode \
  elite_robots_msgs/srv/GetRobotMode '{}'

ros2 service call /dashboard_client/get_safety_mode \
  elite_robots_msgs/srv/GetSafetyMode '{}'

ros2 service call /dashboard_client/get_task_status \
  elite_robots_msgs/srv/GetTaskStatus '{}'
```

每个响应先检查 success，再读取 mode.mode 或 status.status。要观察外部控制程序运行状态，可订阅：

```bash
ros2 topic echo /io_and_status_controller/robot_task_running \
  --qos-durability transient_local
```

该话题需要已经产生样本；Dashboard 查询与此 Bool 的语义不同，前者是机器人任务状态，后者还要求外部控制连接有效。

## IO 与速度滑块请求格式

以下命令会改变机器人或外设状态。只在对应通道用途、工具电压和运行条件已经确认后调用；这里展示服务格式，不作为启动时自动执行步骤。

标准数字输出 0 置为高：

```bash
ros2 service call /io_and_status_controller/set_io \
  elite_robots_msgs/srv/SetIO \
  '{fun: 1, pin: 0, analog_type: 0, state: 1.0}'
```

将速度滑块设为 25%：

```bash
ros2 service call /io_and_status_controller/set_speed_slider \
  elite_robots_msgs/srv/SetSpeedSliderFraction \
  '{speed_slider_fraction: 0.25}'
```

随后读回 IO/速度状态。服务存在、请求已发送、响应 success 为 true、实际状态已变化，应分别判断。

## 六轴运动示例程序

Driver 的 C++ 与 Python 示例读取 `/joint_states`，按关节名重排当前值，然后向指定控制器的 `follow_joint_trajectory` 发送一个起点和一个目标点。两个程序都固定为六轴无前缀名称，不适用于 `cs520h`。

- `controller`：类型：string；直接运行的默认值：`scaled_joint_trajectory_controller`。

- `target`：类型：double[]；直接运行的默认值：Python 必填；C++ 为 `[0.0, -1.2, 0.0, -1.57, 0.0, 0.0]`。

- `max_vel`：类型：double；直接运行的默认值：0.5 rad/s。

- `min_time`：类型：double；直接运行的默认值：2.0 s。


时长按 `max(max_i(abs(target_i-current_i))/max_vel, min_time)` 估算。`max_vel` 只是时长估算输入，不是控制器硬速度限幅，示例也不执行碰撞规划。应传入正速度和已检查的目标。

`example_safe_joint_move.launch.py` 的默认 `min_time` 是 **20.0 s**，与直接 ros2 run 的 2.0 s 不同；launch 的 `target` 必填。

下面示例只用于已启动的六轴 Gazebo、标准轨迹控制器和已确认目标的场景，会产生运动：

```bash
ros2 run elite_robots_driver example_safe_joint_move_py --ros-args \
  -p controller:=joint_trajectory_controller \
  -p target:='[0.0, -1.57, 0.0, -1.57, 0.0, 0.0]' \
  -p max_vel:=0.2 -p min_time:=20.0 -p use_sim_time:=true
```

实体机器人使用缩放轨迹控制器时，还需确保外部控制任务运行、机器人模式正常且控制器 active，并根据实际环境重新确认目标。

## 应用动作客户端流程

1. 获取新鲜的关节状态，按名称建立映射；检查轴数、前缀、目标范围及使用的时钟。
2. 等待预期的动作服务器，设置连接超时；不要把同名话题存在作为服务器可执行的证明。
3. 构造完整 joint_names 和时间递增的 points，选择路径与目标容差。
4. 发送目标后检查是否被接受；被拒绝时不要继续等待运动完成。
5. 接收反馈，跟踪最终动作状态、error_code 和 error_string。
6. 在应用取消、断连或异常时走明确的停止流程，并独立确认机器人状态。

客户端应给等待响应、执行和取消设置超时，避免无限等待。管理服务中的停止操作与动作取消不是同一层接口，应按应用控制权设计协调。

## 常见接口问题

```{list-table}
:header-rows: 1
:widths: 40 60

* - 现象
  - 检查方向
* - 找不到 Dashboard 服务
  - fake hardware 不加载组件；组件进程可能因首次连接失败移除了 Dashboard 节点
* - 轨迹目标被拒绝
  - 控制器 inactive、关节数/名称错误、前缀不一致或轨迹时间无效
* - MoveIt 规划成功但执行失败
  - 实际控制器与 MoveIt 默认映射不一致；管理器不由 MoveIt 自动启动
* - Gazebo 规划或 TF 卡住
  - `/clock` 无发布者/无数据，或节点使用了不同时间源
* - 速度设置失败
  - 使用了 25 而不是 0.25，或请求小于 0.01
* - 模式话题没有持续消息
  - 本版只在变化时发布；用查询服务获取当前状态
* - IO success 为 true 但输出未变化
  - 校验通道范围，检查异步超时日志，并读回实际 IO
* - TCP 位姿与 TF 不一致
  - 比较的 frame 不同，或混用了模型 tool0 与控制器 TCP
* - 五轴示例报参数错误
  - 示例固定六轴；使用五轴配置及自定义轨迹客户端
* - 已修改源码但接口未变化
  - 核对安装路径、是否重建及终端 overlay 加载顺序
```
