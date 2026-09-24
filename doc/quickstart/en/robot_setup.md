# Robot setup

The driver can connect to either a physical robot or the ELIBOTSim virtual teach pendant. Choose one of these options. If you only use [Gazebo physics simulation](gazebo.md) (Humble only), ELIBOTSim is not required.

## Set up a physical robot

### Connect the control cabinet to the network

The **standard CS-series control cabinet** uses a dual-processor architecture. Normally, connect FB1, FB2, and the computer running the ROS 2 driver to the same local network and configure their IP addresses.

| Network port | Description |
| --- | --- |
| FB1 | Processor running Dashboard functionality |
| FB2 | Processor running the control software that communicates with the ROS 2 driver |

> Starting with robot software **2.14.3**, connecting only FB2 is supported. The **CS-series B1 control cabinet** requires only one network connection.

The computer interface connected to the robot must be on the same subnet, with no IP address conflict. This guide refers to the address of that computer interface as the **Local IP**.

### Configure remote control mode

1. Click the Elite icon in the upper-right corner of the teach pendant and open **Settings**.
2. Enable **Remote Control Mode** in Settings, then exit using the control at the lower left.
3. On the right side of the interface, change **Local Control** to **Remote Control**.

```{figure} images/fig-2-1-settings.png
:name: fig-2-1-settings
:alt: Teach pendant settings
:width: 90%
:align: center

Teach pendant settings
```

```{figure} images/fig-2-2-remote-mode-settings.png
:name: fig-2-2-remote-mode-settings
:alt: Remote control mode settings
:width: 90%
:align: center

Remote control mode settings
```

```{figure} images/fig-2-3-remote-option.png
:name: fig-2-3-remote-option
:alt: Remote control option
:width: 90%
:align: center

Remote control option
```

```{figure} images/fig-2-4-remote-control.png
:name: fig-2-4-remote-control
:alt: Remote control interface
:width: 90%
:align: center

Remote control interface
```

```{note}
When remote control mode is disabled on CS- and ES-series robots, the robot operates in mixed mode: both external control and local teach pendant control can take effect. It is therefore also possible to leave remote control mode disabled in the steps above.
```

## Test the network connection

The robot script test is recommended because it checks the connection from the robot to a TCP server port on the computer. `ping` is useful for preliminary troubleshooting, but a successful response does not guarantee that motion-control communication will work.

### Method 1: Robot script and TCP server

#### Find the computer's IP address

On the Linux computer running the ROS 2 driver, run:

```bash
ifconfig
```

Note the address of the network interface connected to the robot. If the command is not found, install it:

```bash
sudo apt install net-tools
```

#### Create a script on the teach pendant

Open **Task**, select **Placeholder node → Advanced → Script**, select **File** in the drop-down list, and click **Edit**.

```{figure} images/fig-2-5-task.png
:name: fig-2-5-task
:alt: Select a task
:width: 90%
:align: center

Select a task
```

```{figure} images/fig-2-6-script.png
:name: fig-2-6-script
:alt: Select a script
:width: 90%
:align: center

Select a script
```

```{figure} images/fig-2-7-edit-file.png
:name: fig-2-7-edit-file
:alt: Edit the file
:width: 90%
:align: center

Edit the file
```

```{figure} images/fig-2-8-edit-script.png
:name: fig-2-8-edit-script
:alt: Edit the script
:width: 90%
:align: center

Edit the script
```

Enter the following code, replacing `Your.Local.IP.Addr` with the computer's Local IP noted above:

```text
socket_open("Your.Local.IP.Addr", 50001)
socket_send_string("Hello SDK\n")
sleep(1)
```

Click **Save** and enter a script file name.

```{figure} images/fig-2-9-save-script.png
:name: fig-2-9-save-script
:alt: Save the script
:width: 90%
:align: center

Save the script
```

```{figure} images/fig-2-10-script-name.png
:name: fig-2-10-script-name
:alt: Set the script name
:width: 90%
:align: center

Set the script name
```

#### Start a TCP server on the computer

Save the following code as `sdk_connection_test.py`. Pass the Local IP as an argument so that the robot can connect over the local network. Listening only on `localhost` will not accept connections from a remote robot.

```python
import argparse
import socket


def start_tcp_server(host, port=50001):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.settimeout(1.0)
        server.bind((host, port))
        server.listen(5)
        print(f"TCP server started at {host}:{port}; waiting for the robot...")
        try:
            while True:
                try:
                    client, address = server.accept()
                except socket.timeout:
                    continue
                print(f"Client connected: {address}")
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
                        print("Client disconnected")
        except KeyboardInterrupt:
            print("\nTCP server stopped")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", required=True, help="Computer Local IP")
    parser.add_argument("--port", type=int, default=50001)
    args = parser.parse_args()
    start_tcp_server(args.host, args.port)
```

Start the server, replacing `<local_ip>` with the computer's actual address:

```bash
python3 sdk_connection_test.py --host <local_ip>
```

#### Run the script and check the result

Press the task run button on the teach pendant. If the terminal prints `Hello SDK`, this TCP connection is working.

```{figure} images/fig-2-11-run-test.png
:name: fig-2-11-run-test
:alt: Run the connection test task
:width: 90%
:align: center

Run the connection test task
```

After the test, stop the test task on the teach pendant. Then press `Ctrl+C` in the computer terminal to stop the server and release the port.

#### Common connection issues

**The TCP server does not start**: Check that the Local IP belongs to the computer and that port `50001` is not already in use. If you use another port, update both the port in the robot's `socket_open` call and the server's `--port` argument.

**The teach pendant reports that `socket_send_string` is not connected to server `socket_0`**: Check the following in order.

- If using a virtual machine, check that its network adapter is in bridged mode and bridged to the physical interface connected to the robot.
- Check that FB2 is connected on a standard CS-series control cabinet.
- Check that the network permits connections in both directions. Connecting the computer, FB1, and FB2 through a switch can simplify the network setup.
- Check that the computer and robot interface addresses are on the same subnet and that there are no address conflicts.
- Check whether a VPN is enabled on the computer; disable it and retry if necessary.
- Check that the server started successfully and its port matches the script.
- Check whether the server has been stopped while the robot is still running the test script in a loop.

If these checks reveal no issues and the connection still fails, restart the control cabinet and try again.

### Method 2: Check both directions using Bash

Use `ifconfig` to find the computer's Local IP. Then log in to the robot operating system from the computer:

```bash
ssh root@<robot_ip>
```

For a standard CS-series control cabinet, use the FB2 IP address. The login password is `elibot`.

After logging in, test the connection from the robot to the computer:

```bash
ping <local_ip>
```

A successful connection produces repeated responses similar to:

```text
64 bytes from 192.168.1.110: seq=0 ttl=64 time=0.373 ms
```

Press `Ctrl+C` to stop the test and run `exit` to end the SSH session. Then test the connection from the computer to the robot:

```bash
ping <robot_ip>
```

For a standard CS-series control cabinet, check FB1 and FB2 as required by your setup. If either is unreachable, check address conflicts, subnet configuration, and local network settings. If `ping` succeeds but control fails, still perform the TCP test in Method 1.

## ELIBOTSim virtual teach pendant

If no physical robot is available, use ELIBOTSim in Docker.

### Install Docker and prepare the startup script

Install Docker using:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Download `start_elibotsim.sh` from the [Elite SDK script directory](https://github.com/EliteRobots/Elite_Robots_CS_SDK/tree/main/script/). Change to the directory containing the script and run:

```bash
chmod +x start_elibotsim.sh
sudo usermod -aG docker "$USER"
```

You usually need to log out and log back in for the group membership change to take effect.

```{figure} images/fig-2-12-simulation-script.png
:name: fig-2-12-simulation-script
:alt: Locate the simulation startup script
:width: 90%
:align: center

Locate the simulation startup script
```

### Start and open the virtual teach pendant

```bash
./start_elibotsim.sh
```

The script currently defaults to image tag `2.14.5`, but the current SDK README specifies a minimum control software version of `2.15.0`. Before connecting the ROS driver, use `-v <version>` to select an available image version compatible with your SDK. The script's default value is not a compatibility guarantee.

The image is pulled on the first run. If startup fails with an error such as `Failed to create network`, try:

```bash
sudo ./start_elibotsim.sh
```

Open <http://localhost:6080> in a browser and confirm that the virtual teach pendant appears.

```{figure} images/fig-2-13-image-ready.png
:name: fig-2-13-image-ready
:alt: Simulation image pulled successfully
:width: 90%
:align: center

Simulation image pulled successfully
```

```{figure} images/fig-2-14-simulator.png
:name: fig-2-14-simulator
:alt: Simulator started successfully
:width: 90%
:align: center

Simulator started successfully
```

### Script arguments

| Argument | Meaning |
| --- | --- |
| `-m <model>` | Robot model; default: `CS66`. Examples: CS63, CS66, ES66 |
| `-c <id>` | `CONTROL_BOX_ID`; default: `1`, overridable with environment variable `ARG_CONTROL_BOX_ID` |
| `-t <id>` | `TOOL_TYPE_ID`; default: `1`, overridable with environment variable `ARG_TOOL_TYPE_ID` |
| `-v <version>` | Image tag; default: `2.14.5` |
| `-p <folder>` | Program directory on the host |
| `-u <folder>` | ELITECO directory on the host |
| `-n <name>` | Container name; default: `elibotsim` |
| `-i <ip>` | Container IP; default: `192.168.56.101` |
| `-d` | Run in the background |
| `-f <mapping>` | Port forwarding string, such as `"-p 6080:6080 -p 5900:5900"` |
| `-r <0 or 1>` | Robot series: `0` for CS, `1` for ES; the script resets this value based on the model supplied with `-m` |
| `-h` | Show help |

For example:

```bash
./start_elibotsim.sh -m cs616
```

After starting the virtual teach pendant, install or start the ROS 2 driver. On the same Linux computer that runs Docker, the default container address `192.168.56.101` can be used as `robot_ip`. If you change `-i`, use the actual container address. The browser address `localhost:6080` is only the teach pendant's web entry point, not the robot address for the driver. When using separate hosts or a virtual machine, also confirm that the robot can connect back to the ROS computer.
