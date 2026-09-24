# 机器人端配置

驱动可以连接实体机器人，也可以连接 ELIBOTSim 虚拟示教器。两种方式任选其一；仅使用 [Gazebo 物理仿真](gazebo.md)（仅 Humble）时，无需启动 ELIBOTSim。

## 实体机器人配置

### 连接控制柜网络

**CS 系列标准控制柜**采用双处理器架构，通常需要将 FB1、FB2 和运行 ROS 2 驱动的计算机接入同一局域网，并配置 IP 地址。

| 网口 | 说明 |
| --- | --- |
| FB1 | 对应运行 Dashboard 功能的处理器 |
| FB2 | 对应运行与 ROS 2 驱动通信的控制软件的处理器 |

> 机器人软件自 **2.14.3** 起，可以仅连接 FB2。**CS 系列 B1 控制柜**仅需连接一个网口。

计算机与机器人相连网口的 IP 应在同一网段，且不能冲突。后文将计算机该网口的地址称为 **Local IP**。

### 设置远程控制模式

1. 点击示教器右上角的 Elite 图标，进入“设置”。
2. 在设置页面启用“远程控制模式”，然后从左下角退出。
3. 在界面右侧出现的“本地控制”选项处，切换到“远程控制”。

```{figure} images/fig-2-1-settings.png
:name: fig-2-1-settings
:alt: 示教器设置
:width: 90%
:align: center

示教器设置
```

```{figure} images/fig-2-2-remote-mode-settings.png
:name: fig-2-2-remote-mode-settings
:alt: 远程控制模式设置
:width: 90%
:align: center

远程控制模式设置
```

```{figure} images/fig-2-3-remote-option.png
:name: fig-2-3-remote-option
:alt: 远程控制选项
:width: 90%
:align: center

远程控制选项
```

```{figure} images/fig-2-4-remote-control.png
:name: fig-2-4-remote-control
:alt: 远程控制界面
:width: 90%
:align: center

远程控制界面
```

```{note}
CS、ES 系列禁用远程控制模式时会处于“混合模式”，外部控制和示教器本地控制均可生效。因此，也允许在上述步骤中禁用远程控制模式。
```

## 测试网络连接

推荐使用机器人脚本测试，因为该方法实际验证了机器人到计算机 TCP 服务端口的连接。`ping` 适合初步排查，但成功响应不代表后续运动通信一定可用。

### 方法一：机器人脚本与 TCP 服务端

#### 获取计算机 IP

在运行 ROS 2 驱动的 Linux 计算机上执行：

```bash
ifconfig
```

记录与机器人连接的网口地址。若提示找不到命令，可安装：

```bash
sudo apt install net-tools
```

#### 在示教器创建脚本

进入“任务”，选择“占位节点 → 高级 → 脚本”，在下拉框中选择“文件”，然后点击“编辑”。

```{figure} images/fig-2-5-task.png
:name: fig-2-5-task
:alt: 选择任务
:width: 90%
:align: center

选择任务
```

```{figure} images/fig-2-6-script.png
:name: fig-2-6-script
:alt: 选择脚本
:width: 90%
:align: center

选择脚本
```

```{figure} images/fig-2-7-edit-file.png
:name: fig-2-7-edit-file
:alt: 编辑文件
:width: 90%
:align: center

编辑文件
```

```{figure} images/fig-2-8-edit-script.png
:name: fig-2-8-edit-script
:alt: 编辑脚本
:width: 90%
:align: center

编辑脚本
```

写入下列内容，把 `Your.Local.IP.Addr` 替换为刚才记录的计算机 Local IP：

```text
socket_open("Your.Local.IP.Addr", 50001)
socket_send_string("Hello SDK\n")
sleep(1)
```

点击“保存”，设置脚本文件名。

```{figure} images/fig-2-9-save-script.png
:name: fig-2-9-save-script
:alt: 保存脚本
:width: 90%
:align: center

保存脚本
```

```{figure} images/fig-2-10-script-name.png
:name: fig-2-10-script-name
:alt: 设置脚本名称
:width: 90%
:align: center

设置脚本名称
```

#### 在计算机启动 TCP 服务

将下列代码保存为 `sdk_connection_test.py`。本版将原示例的监听地址改为通过参数传入 Local IP，以便机器人通过局域网连接；仅监听 `localhost` 无法接受远端机器人的连接。

```python
import argparse
import socket


def start_tcp_server(host, port=50001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(1.0)
        server.bind((host, port))
        server.listen(5)
        print(f"TCP 服务已启动：{host}:{port}，等待机器人连接……")
        try:
            while True:
                try:
                    client, address = server.accept()
                except socket.timeout:
                    continue
                print(f"客户端已连接：{address}")
                with client:
                    client.settimeout(1.0)
                    try:
                        while True:
                            try:
                                data = client.recv(1024)
                            except socket.timeout:
                                continue
                            if not data:
                                break
                            print(data.decode("utf-8", errors="replace"),
                                  end="", flush=True)
                    except ConnectionResetError:
                        print("客户端已断开连接")
        except KeyboardInterrupt:
            print("\nTCP 服务已停止")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="计算机 Local IP")
    parser.add_argument("--port", type=int, default=50001)
    args = parser.parse_args()
    start_tcp_server(args.host, args.port)
```

启动服务，把 `<local_ip>` 替换为计算机实际地址：

```bash
python3 sdk_connection_test.py --host <local_ip>
```

#### 运行脚本并确认结果

在示教器点击任务运行按钮。若终端打印 `Hello SDK`，说明这条 TCP 连接正常。

```{figure} images/fig-2-11-run-test.png
:name: fig-2-11-run-test
:alt: 运行测试任务
:width: 90%
:align: center

运行测试任务
```

测试结束后停止示教器中的测试任务，再在计算机终端按 `Ctrl+C` 停止服务，释放端口。

#### 常见连接问题

**TCP 服务无法启动**：检查 Local IP 是否属于本机，以及 `50001` 端口是否被占用。如改用其他端口，需同时修改机器人 `socket_open` 中的端口和服务端 `--port` 参数。

**示教器提示 `socket_send_string` 未连接服务端 `socket_0`**：依次检查以下内容。

- 若使用虚拟机，网卡是否采用桥接模式，并桥接到连接机器人的物理网卡。
- CS 系列标准控制柜的 FB2 是否已连接。
- 网络是否允许相互连接；可以通过交换机连接计算机、FB1、FB2，简化网络环境。
- 计算机与机器人网口 IP 是否位于同一网段，是否存在地址冲突。
- 计算机是否开启 VPN；可关闭后重试。
- 服务端是否已成功启动，端口是否与脚本一致。
- 是否已经关闭服务端，但机器人仍在循环执行测试脚本。

以上均无问题仍无法连接时，重启控制柜后再试。

### 方法二：使用 Bash 检查双向网络

先通过 `ifconfig` 获取计算机 Local IP。随后从计算机登录机器人操作系统：

```bash
ssh root@<robot_ip>
```

CS 系列标准控制柜使用 FB2 的 IP。登录密码为 `elibot`。

登录成功后，从机器人一侧测试到计算机的连接：

```bash
ping <local_ip>
```

成功时会持续出现类似下列响应：

```text
64 bytes from 192.168.1.110: seq=0 ttl=64 time=0.373 ms
```

按 `Ctrl+C` 停止测试，执行 `exit` 退出 SSH，然后从计算机测试到机器人的连接：

```bash
ping <robot_ip>
```

CS 系列标准控制柜按使用场景分别检查 FB1、FB2。若不通，检查地址冲突、网段和局域网设置。若 `ping` 成功但控制失败，仍应执行方法一的 TCP 测试。

## ELIBOTSim 虚拟示教器

没有实体机器人时，可使用 Docker 中的 ELIBOTSim。

### 安装 Docker 并准备启动脚本

使用以下方式安装 Docker：

```bash
curl -fsSL https://get.docker.com | sudo sh
```

从 [Elite SDK 的 script 目录](https://github.com/EliteRobots/Elite_Robots_CS_SDK/tree/main/script/)下载 `start_elibotsim.sh`，进入脚本所在目录执行：

```bash
chmod +x start_elibotsim.sh
sudo usermod -aG docker "$USER"
```

用户组变更通常需要重新登录后生效。

```{figure} images/fig-2-12-simulation-script.png
:name: fig-2-12-simulation-script
:alt: 找到仿真脚本
:width: 90%
:align: center

找到仿真脚本
```

### 启动并打开虚拟示教器

```bash
./start_elibotsim.sh
```

脚本当前默认镜像标签为 `2.14.5`，但当前 SDK 的 README 声明最低控制软件版本为 `2.15.0`。连接 ROS 驱动前，请通过 `-v <version>` 选择与所用 SDK 兼容且实际可获取的镜像版本，不能将脚本默认值视为兼容性保证。

首次运行会拉取镜像。如果出现 `Failed to create network` 等启动错误时，可尝试：

```bash
sudo ./start_elibotsim.sh
```

随后在浏览器访问 <http://localhost:6080>，确认虚拟示教器已显示。

```{figure} images/fig-2-13-image-ready.png
:name: fig-2-13-image-ready
:alt: 拉取仿真镜像成功
:width: 90%
:align: center

拉取仿真镜像成功
```

```{figure} images/fig-2-14-simulator.png
:name: fig-2-14-simulator
:alt: 仿真器启动成功
:width: 90%
:align: center

仿真器启动成功
```

### 脚本参数

| 参数 | 含义 |
| --- | --- |
| `-m <model>` | 机器人型号，默认 `CS66`，如 CS63、CS66、ES66 |
| `-c <id>` | `CONTROL_BOX_ID`，默认 `1`（可由环境变量 `ARG_CONTROL_BOX_ID` 覆盖） |
| `-t <id>` | `TOOL_TYPE_ID`，默认 `1`（可由环境变量 `ARG_TOOL_TYPE_ID` 覆盖） |
| `-v <version>` | 镜像标签，默认 `2.14.5` |
| `-p <folder>` | 宿主机程序目录 |
| `-u <folder>` | 宿主机 ELITECO 目录 |
| `-n <name>` | 容器名称，默认 `elibotsim` |
| `-i <ip>` | 容器 IP，默认 `192.168.56.101` |
| `-d` | 后台运行 |
| `-f <mapping>` | 端口转发字符串，如 `"-p 6080:6080 -p 5900:5900"` |
| `-r <0或1>` | 机器人系列：`0` 为 CS，`1` 为 ES；脚本会根据 `-m` 的型号重新设置此值 |
| `-h` | 显示帮助 |

例如：

```bash
./start_elibotsim.sh -m cs616
```

启动虚拟示教器后，可继续安装或启动 ROS 2 驱动。在运行 Docker 的同一台 Linux 计算机上，默认可使用容器地址 `192.168.56.101` 作为 `robot_ip`。修改了 `-i` 时应使用实际容器地址。浏览器的 `localhost:6080` 只是示教器网页入口，不是驱动的机器人地址；跨主机或虚拟机部署还需确认机器人能够反向连接 ROS 计算机。
