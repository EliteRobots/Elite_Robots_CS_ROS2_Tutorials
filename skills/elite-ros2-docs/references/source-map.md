# ROS 2 文档源码核对入口

仅在校对操作命令与实现时查阅。路径相对于 Tutorials 所在的工作空间 `src/`；仓库可迁移，先定位实际目录。下列文件是查找入口，具体值应每次读取当前版本，不把历史默认值固化为规则。

## Driver：Elite_Robots_CS_ROS2_Driver

| 要核对的内容 | 入口 |
| --- | --- |
| ROS 包名、依赖、发行版本 | 各包 `package.xml` |
| 驱动 launch 参数、默认控制器、型号选项 | `elite_robots_driver/launch/elite_control.launch.py` |
| Python/C++ 安装后的可执行名 | `elite_robots_driver/CMakeLists.txt` |
| 示例参数类型、关节数量、速度单位和时间估算 | `elite_robots_driver/example/python/example_safe_joint_move.py`、`example/cpp/example_safe_joint_move.cpp` |
| 默认控制器、激活状态及五轴差异 | `elite_robots_driver/config/`、驱动 launch 的 spawner 配置 |
| 硬件参数和 Local IP 处理 | `elite_robots_driver/src/hardware_interface.cpp` |
| IO 服务、速度缩放消息及单位 | `elite_robots_controllers/src/`，尤其 `gpio_controller.cpp`、`speed_scaling_state_broadcaster.cpp` |
| Dashboard 服务类型、私有名称及节点加载条件 | `elite_robots_driver/src/`；搜索 `create_service`、`dashboard_client`、`load_components` |
| 状态常量和服务字段 | `elite_robots_msgs/msg/`、`srv/` 及 `elite_robots_dashboard_msgs/` |
| MoveIt 启动名称、控制器选择、仿真时钟 | `elite_robots_moveit_config/launch/elite_moveit.launch.py`、`config/` |

注意检查参数在 launch 内实际影响的对象，而非只按参数名称推断。例如 `use_fake_hardware` 在 MoveIt 配置中的作用，需要追踪控制器选择及是否真的启动硬件节点。

## Description：Elite_Robots_CS_ROS2_Description

从 `launch/view_cs.launch.py` 核对模型展示命令及允许型号；从 `config/`、`urdf/` 和 `urdf_5f/` 核对模型、关节数、前缀和硬件参数默认值。产品型号列表不等于 launch 接受的字符串列表，不自行猜测 ES/CS 型号映射。

## Gazebo：Elite_Robots_CS_ROS2_GZ_Simulation

检查 `launch/elite_sim_control.launch.py`、`launch/elite_sim_moveit.launch.py`、`config/`、`scripts/gz_control.py`、`CMakeLists.txt` 和 `package.xml`。

追踪组合 launch 引用的文件是否确实存在、默认轨迹控制器是否与 MoveIt 一致，以及使用仿真时间的节点是否能收到 `/clock`。不要因为顶层 launch 文件存在就认为组合启动有效。程序脚本的 CLI 可能使用 argparse，与驱动示例的 ROS 参数格式不同。

## SDK：Elite_Robots_CS_SDK

仅在解释底层通信、固件要求或 ELIBOTSim 时继续查阅：

- `script/start_elibotsim.sh`：镜像标签、型号处理、控制柜 ID、容器地址、端口和网络创建逻辑；帮助文本与实际参数解析也可能不同。
- `README.md`：SDK 声明的控制软件要求。
- `source/Elite/EliteDriver.cpp`：Local IP、无头模式及外部控制脚本发送行为。

脚本默认镜像版本不是兼容性证明。发现版本声明矛盾时记录依据和限制，不虚构已经验证的镜像标签。
