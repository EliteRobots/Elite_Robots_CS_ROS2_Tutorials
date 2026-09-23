# 本地环境安装

本章沿用原手册的 **Ubuntu 22.04 + ROS 2 Humble + MoveIt 2 + Gazebo Fortress** 环境及安装路线。安装命令用于复现原手册环境，尚未针对当前项目依赖做调整。

## 安装 ROS 2 Humble

### 官方软件包安装方式

先配置软件包源：

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update
sudo apt install curl -y

sudo curl -sSL \
  https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
  -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" \
  | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null
```

安装桌面版本，其中包含 RViz 等可视化工具；`ros-dev-tools` 提供常用开发工具：

```bash
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop
sudo apt install ros-dev-tools
```

配置 Bash 终端环境：

```bash
echo 'source /opt/ros/humble/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

若 `.bashrc` 已有相同配置，无需重复追加。仅希望在当前终端生效时，可以直接执行 `source /opt/ros/humble/setup.bash`。

### 原手册提供的替代安装方式

原手册也提供了以下安装入口，和上述方式任选其一：

```bash
wget http://fishros.com/install -O fishros && . fishros
```

按脚本提示操作完成安装。

### 验证安装

```bash
ros2 --help
```

终端应显示 ROS 2 命令帮助。

```{admonition} 图片占位 · 原图 3-1：ROS 2 安装成功
:class: figure-placeholder
待补充 `ros2 --help` 输出截图。建议文件名：`images/fig-3-1-ros2-help.png`。
```

## 安装 MoveIt 2

MoveIt 2 提供运动规划、正逆运动学、碰撞检测、轨迹生成与优化、机器人控制集成、抓取操作及 RViz 调试能力。

按原手册安装 MoveIt 2 和 MoveIt Servo：

```bash
sudo apt update
sudo apt install ros-humble-moveit
sudo apt install ros-humble-moveit-servo
source /opt/ros/humble/setup.bash
```

原手册参考链接：[MoveIt 2 二进制安装指南](https://moveit.ai/install-moveit2/binary/)。

## 安装 Gazebo Fortress

Gazebo Fortress 属于原 Ignition Gazebo 系列，用于机器人物理仿真。它提供渲染、物理模拟、场景编辑及通信能力，可通过 ROS 集成组件与 ROS 2 配合使用。

### 准备基础工具并安装 Fortress

```bash
sudo apt-get update
sudo apt-get install lsb-release gnupg

sudo curl https://packages.osrfoundation.org/gazebo.gpg \
  --output /usr/share/keyrings/pkgs-osrf-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/pkgs-osrf-archive-keyring.gpg] http://packages.osrfoundation.org/gazebo/ubuntu-stable $(lsb_release -cs) main" \
  | sudo tee /etc/apt/sources.list.d/gazebo-stable.list > /dev/null

sudo apt-get update
sudo apt-get install ignition-fortress
```

### 安装 ROS 2 集成并配置环境

```bash
sudo apt install -y ros-humble-ros-gz
```

原手册给出的环境加载路径为 `/usr/share/gz/setup.bash`。该路径需要结合实际安装结果确认；若该文件存在，可按原手册追加：

```bash
echo 'source /usr/share/gz/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

原手册参考链接：[Gazebo Fortress 安装指南](https://gazebosim.org/docs/fortress/install_ubuntu/)。

### 虚拟机中的渲染问题

如果在 Ubuntu 虚拟机中出现网格闪烁或空白渲染窗口，原手册建议尝试软件渲染：

```bash
echo 'export LIBGL_ALWAYS_SOFTWARE=true' >> ~/.bashrc
source ~/.bashrc
```

该设置用于处理虚拟机图形加速受限的情况。

## 安装 ELITE SDK

ELITE SDK 是用于 CS、ES 系列机器人的 C++ 库。按原手册要求，应在安装 ROS 2 驱动前先安装 SDK，推荐使用源码编译安装。

SDK 的完整安装和使用步骤请参阅《C++ SDK 快速使用手册》。原手册未在本章提供 SDK 构建命令，因此本版也不补写与当前 SDK 版本绑定的安装步骤。

## 获取并编译 ROS 2 驱动

### 创建工作空间并下载源码

```bash
mkdir -p ~/elite_ros_ws/src
cd ~/elite_ros_ws/src
git clone https://github.com/Elite-Robots/Elite_Robots_CS_ROS2_Driver.git
```

### 安装依赖

```bash
cd ~/elite_ros_ws
sudo rosdep init
rosdep update
rosdep install --ignore-src --rosdistro "$ROS_DISTRO" --from-paths src -y
```

`rosdep init` 仅需在系统首次初始化时执行。执行依赖安装前，应已加载 ROS 2 Humble 环境，使 `ROS_DISTRO` 为 `humble`。

### 编译并加载工作空间

```bash
cd ~/elite_ros_ws
colcon build
source ~/elite_ros_ws/install/setup.bash
```

如需每次新开终端自动加载，可以追加一次：

```bash
echo 'source ~/elite_ros_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

### 验证驱动启动

先按[机器人端配置](robot_setup.md)准备实体机器人或虚拟示教器，再替换参数执行：

```bash
ros2 launch eli_cs_robot_driver elite_control.launch.py \
  robot_ip:=<robot_ip> \
  local_ip:=<local_ip> \
  cs_type:=<cs_type>
```

| 参数 | 含义 |
| --- | --- |
| `robot_ip` | 实体机器人 IP；原手册的虚拟示教器场景填写本地计算机 IP |
| `local_ip` | 运行驱动的计算机 IP |
| `cs_type` | 机器人型号，例如 `cs66`、`cs63` |

原手册还列出了 `cc612` 这一型号字符串，其准确拼写待后续核对。本版不将其擅自替换为其他型号。

完成后继续阅读[驱动入门](driver.md)，验证状态反馈与基本控制。
