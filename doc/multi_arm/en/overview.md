# Before you start

## Environment and files

Install the Elite Robots ROS 2 driver correctly. If it is not installed, follow the relevant installation chapter in the Quick Start Guide.

In a terminal with ROS 2 and the target workspace sourced, check the installed package versions:

```bash
ros2 pkg xml -t version elite_robots

ros2 pkg xml -t version elite_robots_description
```

## Operating scenarios

- Physical robots: both controllers must be reachable and able to connect back to the ROS computer. Enable remote control as required by robot configuration when using headless mode.
- ELIBOTSim: use reachable addresses of two independent simulated controllers, with the same reverse connection and port requirements. Do not point both arms to the same controller instance.
- Fake hardware: no robot connection; useful for joint and namespace integration, but not a complete controller simulator.
