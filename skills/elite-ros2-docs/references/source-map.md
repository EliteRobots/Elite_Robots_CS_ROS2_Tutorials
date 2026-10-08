# ROS 2 文档源码核对入口

仅在校对操作命令与实现时查阅。下列路径默认相对于 Tutorials 所在工作空间的 `src/`；用户另行指定源码目录时以该目录为准。仓库可迁移，先定位实际 checkout，不混用同名仓库的版本。下列文件是查找入口，具体值应每次读取当前版本，不把历史默认值固化为规则。

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

## 多机械臂组合

参考入口为 Driver 的 `elite_robots_driver/doc/MultiArm_CN.md`；正式手册在 Tutorials 的 `doc/multi_arm/<language>/`，共享模板在 `doc/multi_arm/examples/`。参考中的 launch 代码也需与当前被包含入口核对，不把说明文字或最后一行日志作为运行成功证据。

- 驱动 `elite_control.launch.py`：检查 `controller_manager_name`、`spawn_controllers`、绝对控制器 YAML 路径、命名空间内的 update rate 键，以及 spawner 目标。参数是否存在和实际作用以当前版本为准。
- MoveIt `elite_moveit.launch.py`：追踪 `prefix`/`tf_prefix`、自定义控制器/运动学/RViz 文件和 `prefer_scaled_controller`；检查 fake 模式的控制器选择是否与包装模板一致。
- 控制器 YAML、`config/kinematics.yaml`、`config/ompl_planning.yaml`、关节限制 YAML、`srdf/` 和 `rviz/view_robot.rviz`：检查每臂关节名、规划组、动作目标及显示 namespace；不能假设所有配置均已自动加前缀。
- 每臂区分 ROS namespace、joint/TF prefix、管理器、控制器 IP 和回连端口。前缀不设置实际安装变换；多个 MoveIt 实例不自动形成联合碰撞场景或同步执行。
- `OnProcessExit` 只代表进程退出，若未检查退出码便不能宣称成功；某一臂启动链结束也不代表其他臂就绪。文档应给出逐臂状态查询。
- 纯配置生成函数可离线检查 YAML 键、关节数量和前缀、运动学规划组与 RViz 映射。此类检查不等同于 fake hardware、MoveIt 或实机运行验证。

## MoveIt 教程示例

正文位于 `doc/tutorials/<语言>/moveit/`，源码位于 `doc/tutorials/examples/moveit/hello_moveit/` 和 `my_elite_robot_cell/`。这些示例需要独立于底层驱动核对；上游教程中的包名或 launch 参数可能已经过期。

- 模型：Description 的 `cs_macro.xacro`、`cs.ros2_control.xacro`，以及示例的场景/控制 Xacro。检查唯一根连杆、关节与连杆前缀、控制标签数量和网格/纹理引用；保留 DAE 引用的纹理，不因正文未直接引用而删除。
- 标定：追踪驱动如何定位 `description_package/config/<型号>/`。当前示例描述包维护唯一一份参数，控制包 CMake 安装相同数据；MoveIt 的 `.setup_assistant` 指向描述包模型。不要传递底层 launch 没有声明和使用的标定覆盖参数。
- 控制：包装 `start_robot.launch.py`、两份 MoveIt 控制器 YAML 和 `move_group.launch.py` 必须使用相同关节集合及动作名称。分别检查 fake 的标准控制器和实体的 scaled 控制器；MoveIt 侧开关不负责启动硬件。
- C++：检查 SRDF 规划组、参考坐标系、末端、有效四元数、状态回调、规划与执行结果，以及客户端 launch 注入的 URDF/SRDF/运动学参数。
- 验证可离线展开 fake/实体 Xacro、用 MoveItConfigsBuilder 加载配置、编译示例；编译安装放临时工作空间，防止缓存混入源码或 ZIP。不为文档验证运行运动示例。ZIP 中保留 `.setup_assistant` 和四个包的完整资源，文件删除后重建下载以排除旧内容。

## SDK：Elite_Robots_CS_SDK

仅在解释底层通信、固件要求或 ELIBOTSim 时继续查阅：

- `script/start_elibotsim.sh`：镜像标签、型号处理、控制柜 ID、容器地址、端口和网络创建逻辑；帮助文本与实际参数解析也可能不同。
- `README.md`：SDK 声明的控制软件要求。
- `source/Elite/EliteDriver.cpp`：Local IP、无头模式及外部控制脚本发送行为。

脚本默认镜像版本不是兼容性证明。发现版本声明矛盾时记录依据和限制，不虚构已经验证的镜像标签。
