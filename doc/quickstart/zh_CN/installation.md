# 本地环境安装

ROS 2 拥有许多发行版本，此处的安装教程以**Ubuntu 22.04**系统中在线安装**ROS 2 Humble**为例，其他发行版或安装方式请查阅 [ROS 2 官方安装文档](https://docs.ros.org/en/humble/Installation.html)。

## 安装 ROS 2 Humble

### 区域设置

请确保系统使用支持 UTF-8 的区域设置。如果你处在精简环境中（例如 Docker 容器），区域设置可能是 POSIX 之类的最小配置。官方使用以下设置进行测试；使用其他支持 UTF-8 的区域设置通常也没有问题。

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### 设置软件源

你需要将 ROS 2 apt 软件仓库添加到系统中。

首先，确保已启用 [Ubuntu Universe 软件仓库](https://help.ubuntu.com/community/Repositories/Ubuntu)。

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

[ros-apt-source](https://github.com/ros-infrastructure/ros-apt-source/) 软件包为各个 ROS 软件仓库提供密钥和 apt 软件源配置。安装 ros2-apt-source 软件包后，系统会完成 ROS 2 软件仓库的配置。ROS 软件仓库发布该软件包的新版本时，仓库配置也会自动更新。

```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

### 安装 ROS 2 软件包

设置软件仓库后，更新 apt 软件仓库缓存。
```bash
sudo apt update
```


桌面版安装：包含 ROS、RViz、演示程序和教程。
```bash
sudo apt install ros-humble-desktop
```

安装开发工具：用于构建 ROS 软件包的编译器及其他工具。
```bash
sudo apt install ros-dev-tools
```

### 配置环境

#### 加载配置脚本

加载以下文件来配置环境：

```bash
source /opt/ros/humble/setup.bash
```

```{note}
如果你使用的不是 bash，请将 .bash 替换为相应 shell 的后缀。可用文件包括 setup.bash、setup.sh 和 setup.zsh。
```

为了日后方便，可以把配置脚本写入环境中，这样每次启动终端都会自动加载`/opt/ros/humble/setup.bash`脚本：
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### 试运行示例

在一个终端中运行 C++ talker：
```bash
ros2 run demo_nodes_cpp talker
```

在另一个终端加载环境后运行 Python listener：
```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

你应该会看到 talker 显示它正在 Publishing（发布）消息，而 listener 显示 I heard（我收到了）这些消息。这说明 C++ 和 Python API 均能正常工作。成功了！

## 安装 Elite Robots ROS 2 驱动

### 在线安装

先加载所用 ROS 发行版的环境，确认 `ROS_DISTRO` 已设置。以下安装方式要求该发行版的软件源中已有对应二进制包；可先用 `apt-cache policy ros-${ROS_DISTRO}-elite-robots` 查看候选版本。若无候选版本，改用下方源码构建流程。二进制发布版与工作空间中的最新源码可能存在接口差异，本手册以当前源码为核对依据。

```bash
sudo apt install ros-${ROS_DISTRO}-elite-robots

# （可选）如果需要使用 Gazebo（仅humble可用）
sudo apt install ros-humble-elite-robots-simulation-gz
```

### 编译安装

1. 创建工作空间并下载源码
```bash
mkdir -p ~/elite_ros_ws/src

cd ~/elite_ros_ws/src

# ROS2 驱动
git clone --branch ${ROS_DISTRO} --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver.git

# 机器人描述文件和模型
git clone --branch ${ROS_DISTRO} --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Description.git

# 机器人SDK
git clone https://github.com/EliteRobots/Elite_Robots_CS_SDK.git

# （可选）如果需要使用 Gazebo（仅humble可用）
git clone --branch humble --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_GZ_Simulation.git
```

2. 安装依赖
```bash
cd ~/elite_ros_ws

sudo rosdep init # 首次执行需要

rosdep update

rosdep install --ignore-src --rosdistro "$ROS_DISTRO" --from-paths src -y
```

3. 编译与加载配置

```bash
colcon build
```

编译成功会有类似如下的输出：
```
Starting >>> elite_robots_description
Starting >>> elite_cs_series_sdk
Starting >>> elite_robots_msgs
Starting >>> elite_robots_dashboard_msgs
Finished <<< elite_robots_description [15.6s]
Starting >>> elite_robots_moveit_config
[Processing: elite_cs_series_sdk, elite_robots_dashboard_msgs, elite_robots_moveit_config, elite_robots_msgs]
Finished <<< elite_robots_moveit_config [39.3s]
Starting >>> elite_robots_simulation_gz
Finished <<< elite_robots_simulation_gz [10.7s]
[Processing: elite_cs_series_sdk, elite_robots_dashboard_msgs, elite_robots_msgs]
Finished <<< elite_robots_dashboard_msgs [1min 49s]
Finished <<< elite_cs_series_sdk [2min 10s]
Starting >>> elite_robots_calibration
Finished <<< elite_robots_msgs [2min 19s]
Starting >>> elite_robots_controllers
Starting >>> elite_robots_driver
[Processing: elite_robots_calibration, elite_robots_controllers, elite_robots_driver]
[Processing: elite_robots_calibration, elite_robots_controllers, elite_robots_driver]
Finished <<< elite_robots_calibration [1min 36s]
Finished <<< elite_robots_controllers [1min 32s]
[Processing: elite_robots_driver]
[Processing: elite_robots_driver]
Finished <<< elite_robots_driver [2min 38s]
Starting >>> elite_robots
Finished <<< elite_robots [4.79s]

Summary: 10 packages finished [5min 3s]
```
> 只要最后的`Summary`没有提示failed、aborted就认为是编译成功

使用下面的命令加载配置：

```bash
source ~/elite_ros_ws/install/setup.bash
```

如需每次新开终端自动加载，可以运行：

```bash
echo 'source ~/elite_ros_ws/install/setup.bash' >> ~/.bashrc
```

## 验证

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs66
```

运行后会出现一个显示了 CS66 的 rviz 界面，以及一个操控面板。

完成后继续阅读[驱动入门](driver.md)，验证状态反馈与基本控制。

## 虚拟机中的渲染问题

如果在 Ubuntu 虚拟机中出现网格闪烁或空白渲染窗口，建议尝试软件渲染：

```bash
echo 'export LIBGL_ALWAYS_SOFTWARE=true' >> ~/.bashrc
source ~/.bashrc
```

该设置用于处理虚拟机图形加速受限的情况。
