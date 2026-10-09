#!/usr/bin/env python3

import re
import tempfile

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    LogInfo,
    OpaqueFunction,
    RegisterEventHandler,
)
from launch.event_handlers import OnProcessExit
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node, PushRosNamespace
from launch_ros.substitutions import FindPackageShare


CONTROLLERS = [
    "joint_state_broadcaster",
    "io_and_status_controller",
    "speed_scaling_state_broadcaster",
    "force_torque_sensor_broadcaster",
    "tcp_pose_broadcaster",
    "scaled_joint_trajectory_controller",
    "forward_position_controller",
    "freedrive_controller",
]


def make_controller_file(namespace, prefix, cs_type):
    controller_filename = (
        "elite_cs_controllers_5f.yaml"
        if cs_type.endswith("h")
        else "elite_cs_controllers.yaml"
    )
    source_path = (
        get_package_share_directory("elite_robots_driver")
        + "/config/"
        + controller_filename
    )
    with open(source_path, "r", encoding="utf-8") as source_file:
        content = source_file.read()

    content = content.replace(
        "controller_manager:",
        f"/{namespace}/controller_manager:",
        1,
    )
    content = content.replace("$(var tf_prefix)", prefix)
    content = re.sub(
        r"^([A-Za-z_][A-Za-z0-9_]*):$",
        lambda match: f"/{namespace}/{match.group(1)}:",
        content,
        flags=re.MULTILINE,
    )

    output = tempfile.NamedTemporaryFile(
        prefix=f"{namespace}_controllers_",
        suffix=".yaml",
        mode="w",
        encoding="utf-8",
        delete=False,
    )
    output.write(content)
    output.close()
    return output.name


def arm_group(
    namespace,
    prefix,
    robot_ip,
    ports,
    cs_type,
    use_fake_hardware,
    headless_mode,
    spawner_timeout,
):
    controller_file = make_controller_file(namespace, prefix, cs_type)
    single_arm_launch = PathJoinSubstitution(
        [
            FindPackageShare("elite_robots_driver"),
            "launch",
            "elite_control.launch.py",
        ]
    )

    spawner_nodes = []
    for controller_name in CONTROLLERS:
        arguments = [
            controller_name,
            "--controller-manager",
            f"/{namespace}/controller_manager",
            "--controller-manager-timeout",
            spawner_timeout,
        ]
        if controller_name in ("forward_position_controller", "freedrive_controller"):
            arguments.append("--inactive")
        spawner_nodes.append(
            Node(
                package="controller_manager",
                executable="spawner",
                arguments=arguments,
                output="screen",
            )
        )

    spawner_chain = [spawner_nodes[0]]
    spawner_chain.extend(
        RegisterEventHandler(
            OnProcessExit(target_action=previous, on_exit=[next_node])
        )
        for previous, next_node in zip(spawner_nodes, spawner_nodes[1:])
    )

    if namespace == "arm2":
        spawner_chain.append(
            RegisterEventHandler(
                OnProcessExit(
                    target_action=spawner_nodes[-1],
                    on_exit=[
                        LogInfo(msg="\033[92mAll required controllers are ready.\033[0m")
                    ],
                )
            )
        )

    return GroupAction(
        actions=[
            PushRosNamespace(namespace),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(single_arm_launch),
                launch_arguments={
                    "cs_type": cs_type,
                    "robot_ip": robot_ip,
                    "tf_prefix": prefix,
                    "use_fake_hardware": use_fake_hardware,
                    "headless_mode": headless_mode,
                    "launch_rviz": "false",
                    "controllers_file": controller_file,
                    "controller_spawner_timeout": spawner_timeout,
                    "controller_manager_name": f"/{namespace}/controller_manager",
                    "spawn_controllers": "false",
                    "reverse_port": ports[0],
                    "script_sender_port": ports[1],
                    "trajectory_port": ports[2],
                    "script_command_port": ports[3],
                }.items(),
            ),
        ]
        + spawner_chain
    )


def setup_arms(context, *args, **kwargs):
    arm1_cs_type = LaunchConfiguration("arm1_cs_type").perform(context)
    arm2_cs_type = LaunchConfiguration("arm2_cs_type").perform(context)
    return [
        arm_group(
            "arm1", "arm1_", LaunchConfiguration("arm1_ip"),
            (
                LaunchConfiguration("arm1_reverse_port"),
                LaunchConfiguration("arm1_script_sender_port"),
                LaunchConfiguration("arm1_trajectory_port"),
                LaunchConfiguration("arm1_script_command_port"),
            ),
            arm1_cs_type,
            LaunchConfiguration("use_fake_hardware"),
            LaunchConfiguration("headless_mode"),
            LaunchConfiguration("controller_spawner_timeout"),
        ),
        arm_group(
            "arm2", "arm2_", LaunchConfiguration("arm2_ip"),
            (
                LaunchConfiguration("arm2_reverse_port"),
                LaunchConfiguration("arm2_script_sender_port"),
                LaunchConfiguration("arm2_trajectory_port"),
                LaunchConfiguration("arm2_script_command_port"),
            ),
            arm2_cs_type,
            LaunchConfiguration("use_fake_hardware"),
            LaunchConfiguration("headless_mode"),
            LaunchConfiguration("controller_spawner_timeout"),
        ),
    ]


def generate_launch_description():
    arm1_ip = LaunchConfiguration("arm1_ip")
    arm2_ip = LaunchConfiguration("arm2_ip")
    arm1_cs_type = LaunchConfiguration("arm1_cs_type")
    arm2_cs_type = LaunchConfiguration("arm2_cs_type")
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    headless_mode = LaunchConfiguration("headless_mode")
    spawner_timeout = LaunchConfiguration("controller_spawner_timeout")
    arm1_reverse_port = LaunchConfiguration("arm1_reverse_port")
    arm1_script_sender_port = LaunchConfiguration("arm1_script_sender_port")
    arm1_trajectory_port = LaunchConfiguration("arm1_trajectory_port")
    arm1_script_command_port = LaunchConfiguration("arm1_script_command_port")
    arm2_reverse_port = LaunchConfiguration("arm2_reverse_port")
    arm2_script_sender_port = LaunchConfiguration("arm2_script_sender_port")
    arm2_trajectory_port = LaunchConfiguration("arm2_trajectory_port")
    arm2_script_command_port = LaunchConfiguration("arm2_script_command_port")

    return LaunchDescription(
        [
            DeclareLaunchArgument("arm1_ip", default_value="192.168.1.101"),
            DeclareLaunchArgument("arm2_ip", default_value="192.168.1.102"),
            DeclareLaunchArgument("arm1_cs_type", default_value="cs63"),
            DeclareLaunchArgument("arm2_cs_type", default_value="cs63"),
            DeclareLaunchArgument("use_fake_hardware", default_value="false"),
            DeclareLaunchArgument("headless_mode", default_value="true"),
            DeclareLaunchArgument("controller_spawner_timeout", default_value="30"),
            DeclareLaunchArgument("arm1_reverse_port", default_value="50001"),
            DeclareLaunchArgument("arm1_script_sender_port", default_value="50002"),
            DeclareLaunchArgument("arm1_trajectory_port", default_value="50003"),
            DeclareLaunchArgument("arm1_script_command_port", default_value="50004"),
            DeclareLaunchArgument("arm2_reverse_port", default_value="50101"),
            DeclareLaunchArgument("arm2_script_sender_port", default_value="50102"),
            DeclareLaunchArgument("arm2_trajectory_port", default_value="50103"),
            DeclareLaunchArgument("arm2_script_command_port", default_value="50104"),
            OpaqueFunction(function=setup_arms),
        ]
    )
