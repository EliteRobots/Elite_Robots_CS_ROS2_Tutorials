#!/usr/bin/env python3

import os
import tempfile

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    GroupAction,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import PushRosNamespace
from launch_ros.substitutions import FindPackageShare


def make_controller_file(prefix, cs_type):
    controller_filename = "controllers_5f.yaml" if cs_type.endswith("h") else "controllers.yaml"
    source_path = os.path.join(
        get_package_share_directory("elite_robots_moveit_config"),
        "config",
        controller_filename,
    )
    with open(source_path, "r", encoding="utf-8") as source_file:
        content = source_file.read()
    content = content.replace("shoulder_", prefix + "shoulder_")
    content = content.replace("elbow_joint", prefix + "elbow_joint")
    content = content.replace("wrist_", prefix + "wrist_")
    output = tempfile.NamedTemporaryFile(
        prefix=prefix + "moveit_controllers_",
        suffix=".yaml",
        mode="w",
        encoding="utf-8",
        delete=False,
    )
    output.write(content)
    output.close()
    return output.name


def make_kinematics_file(group):
    source_path = os.path.join(
        get_package_share_directory("elite_robots_moveit_config"),
        "config",
        "kinematics.yaml",
    )
    with open(source_path, "r", encoding="utf-8") as source_file:
        content = source_file.read().replace("cs_manipulator:", group + ":")
    output = tempfile.NamedTemporaryFile(
        prefix=group + "_kinematics_",
        suffix=".yaml",
        mode="w",
        encoding="utf-8",
        delete=False,
    )
    output.write(content)
    output.close()
    return output.name


def make_rviz_file(group, namespace):
    source_path = os.path.join(
        get_package_share_directory("elite_robots_moveit_config"),
        "rviz",
        "view_robot.rviz",
    )
    with open(source_path, "r", encoding="utf-8") as source_file:
        content = source_file.read()
    content = content.replace("Planning Group: cs_manipulator", "Planning Group: " + group)
    content = content.replace(
        'Move Group Namespace: ""',
        "Move Group Namespace: /" + namespace,
    )
    content = content.replace(
        "Trajectory Topic: /display_planned_path",
        "Trajectory Topic: /" + namespace + "/display_planned_path",
    )
    output = tempfile.NamedTemporaryFile(
        prefix=group + "_rviz_",
        suffix=".rviz",
        mode="w",
        encoding="utf-8",
        delete=False,
    )
    output.write(content)
    output.close()
    return output.name


def arm_moveit(namespace, prefix, cs_type, use_fake_hardware, launch_rviz):
    group = namespace + "_cs_manipulator"
    moveit_launch = PathJoinSubstitution(
        [
            FindPackageShare("elite_robots_moveit_config"),
            "launch",
            "elite_moveit.launch.py",
        ]
    )
    return GroupAction(actions=[
        PushRosNamespace(namespace),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(moveit_launch),
            launch_arguments={
                "cs_type": cs_type,
                "prefix": prefix,
                "use_fake_hardware": use_fake_hardware,
                "launch_rviz": launch_rviz,
                "launch_servo": "false",
                "moveit_controllers_file": make_controller_file(prefix, cs_type),
                "kinematics_file": make_kinematics_file(group),
                "rviz_config_file": make_rviz_file(group, namespace),
                "prefer_scaled_controller": "true",
            }.items(),
        ),
    ])


def setup_arms(context, *args, **kwargs):
    arm1_cs_type = LaunchConfiguration("arm1_cs_type").perform(context)
    arm2_cs_type = LaunchConfiguration("arm2_cs_type").perform(context)
    return [
        arm_moveit(
            "arm1", "arm1_", arm1_cs_type,
            LaunchConfiguration("use_fake_hardware"),
            LaunchConfiguration("launch_rviz"),
        ),
        arm_moveit(
            "arm2", "arm2_", arm2_cs_type,
            LaunchConfiguration("use_fake_hardware"),
            LaunchConfiguration("launch_rviz"),
        ),
    ]


def generate_launch_description():
    use_fake_hardware = LaunchConfiguration("use_fake_hardware")
    launch_rviz = LaunchConfiguration("launch_rviz")
    return LaunchDescription([
        DeclareLaunchArgument("use_fake_hardware", default_value="false"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument("arm1_cs_type", default_value="cs63"),
        DeclareLaunchArgument("arm2_cs_type", default_value="cs63"),
        OpaqueFunction(function=setup_arms),
    ])
