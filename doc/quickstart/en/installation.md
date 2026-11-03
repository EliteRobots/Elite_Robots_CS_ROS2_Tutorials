# Local environment setup

ROS 2 has multiple distributions. This procedure installs **ROS 2 Humble** from binary packages on **Ubuntu 22.04**. For other distributions or installation methods, see the [official ROS 2 installation documentation](https://docs.ros.org/en/humble/Installation.html).

## Install ROS 2 Humble

### Configure the locale

Make sure your system uses a locale that supports UTF-8. Minimal environments, such as Docker containers, may use a minimal locale such as POSIX. The following settings are used in the official installation instructions; other UTF-8 locales generally work as well.

```bash
locale  # check for UTF-8

sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

locale  # verify settings
```

### Configure package repositories

Add the ROS 2 apt repository to your system.

First, make sure the [Ubuntu Universe repository](https://help.ubuntu.com/community/Repositories/Ubuntu) is enabled.

```bash
sudo apt install software-properties-common
sudo add-apt-repository universe
```

The [ros-apt-source](https://github.com/ros-infrastructure/ros-apt-source/) packages provide signing keys and apt repository configuration for ROS repositories. Installing `ros2-apt-source` configures the ROS 2 repository. Repository configuration is also updated when a new version of that package is released.

```bash
sudo apt update && sudo apt install curl -y
export ROS_APT_SOURCE_VERSION=$(curl -s https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest | grep -F "tag_name" | awk -F'"' '{print $4}')
curl -L -o /tmp/ros2-apt-source.deb "https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
sudo dpkg -i /tmp/ros2-apt-source.deb
```

### Install ROS 2 packages

After configuring the repository, update the apt package index:

```bash
sudo apt update
```

Install the desktop variant, which includes ROS, RViz, demos, and tutorials:

```bash
sudo apt install ros-humble-desktop
```

Install development tools, including compilers and other tools used to build ROS packages:

```bash
sudo apt install ros-dev-tools
```

### Configure the environment

#### Source the setup file

Load the following file to configure your environment:

```bash
source /opt/ros/humble/setup.bash
```

```{note}
If you use a shell other than Bash, replace `.bash` with the appropriate suffix. Available files include `setup.bash`, `setup.sh`, and `setup.zsh`.
```

For convenience, add the following command to `~/.bashrc` so that new Bash terminals load the ROS 2 environment automatically. Do not add it again if it is already present:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

### Run the demos

Run the C++ talker in one terminal:

```bash
ros2 run demo_nodes_cpp talker
```

Run the Python listener in another terminal. If you configured `.bashrc` and the new terminal has loaded the environment automatically, skip the `source` command below:

```bash
source /opt/ros/humble/setup.bash
ros2 run demo_nodes_py listener
```

The talker should display messages starting with `Publishing`, and the listener should display `I heard`. This confirms that the C++ and Python APIs are working.

## Install the Elite Robots ROS 2 driver

### Install binary packages (recommended)

First source the environment for your ROS distribution and confirm that `ROS_DISTRO` is set. This method requires the corresponding binary packages to be available in that distribution's repository. Check for a candidate version with `apt-cache policy ros-${ROS_DISTRO}-elite-robots`. If none is available, use the source build procedure below.

```bash
sudo apt install ros-${ROS_DISTRO}-elite-robots

# Optional: Gazebo support (Humble only)
sudo apt install ros-humble-elite-robots-simulation-gz
```

Packages installed with apt are loaded by `/opt/ros/humble/setup.bash`; you do not need to create or source `~/elite_ros_ws`. If you only use binary packages, skip “Build from source” and proceed to verification below.

### Build from source

**1. Create a workspace and download the source.**

```bash
mkdir -p ~/elite_ros_ws/src

cd ~/elite_ros_ws/src

# ROS 2 driver
git clone --branch ${ROS_DISTRO} --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Driver.git

# Robot description files and models
git clone --branch ${ROS_DISTRO} --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_Description.git

# Robot SDK
git clone https://github.com/EliteRobots/Elite_Robots_CS_SDK.git

# Optional: Gazebo support (Humble only)
git clone --branch humble --single-branch https://github.com/EliteRobots/Elite_Robots_CS_ROS2_GZ_Simulation.git
```

**2. Install dependencies.**

```bash
cd ~/elite_ros_ws

sudo rosdep init # Required only for the initial setup

rosdep update

rosdep install --ignore-src --rosdistro "$ROS_DISTRO" --from-paths src -y
```

**3. Build and source the workspace.**

```bash
colcon build
```

A successful build produces output similar to the following:

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

The build is successful if the final `Summary` reports no failed or aborted packages.

Source the workspace:

```bash
source ~/elite_ros_ws/install/setup.bash
```

To load the workspace automatically in new Bash terminals, add the following command to `~/.bashrc`, after the ROS 2 setup command. Do not add it again if it is already present:

```bash
echo 'source ~/elite_ros_ws/install/setup.bash' >> ~/.bashrc
```

(terminal-environment)=
## Terminal environment setup

In later chapters, “environment loaded” means that the terminal has the environment required to run the installed packages. It does not mean you must run `source` manually every time. Choose according to your installation method:

- **apt installation**: Load only the ROS 2 environment. You do not need `~/elite_ros_ws/install/setup.bash`.
- **Source installation**: After loading ROS 2, also load the built workspace. Use its actual path if it differs from the example.
- **`~/.bashrc` already configured**: New Bash terminals run the setup commands automatically; you do not need to repeat them. Terminals opened before you edited `.bashrc` do not update automatically. Open a new terminal or load the environment manually as shown below.

Run this only if the current terminal has not loaded the environment (this guide uses Humble):

```bash
source /opt/ros/humble/setup.bash
```

Only when using a workspace built from source, also run:

```bash
source ~/elite_ros_ws/install/setup.bash
```

Every terminal used for the driver, service calls, MoveIt 2, or Gazebo must meet these conditions.

## Verify the installation

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs66
```

An RViz window showing the CS66 model and a control panel should open.

Continue with [Getting started with the driver](driver.md) to verify state feedback and basic control.

## Rendering issues in virtual machines

If you see flickering meshes or a blank rendering window in an Ubuntu virtual machine, try software rendering:

```bash
echo 'export LIBGL_ALWAYS_SOFTWARE=true' >> ~/.bashrc
source ~/.bashrc
```

This setting can help when graphics acceleration in the virtual machine is limited.
