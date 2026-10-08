# Adapted from Elite Robots ROS 2 tutorials.
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    arguments = [
        DeclareLaunchArgument("cs_type", default_value="cs63", choices=["cs63"]),
        DeclareLaunchArgument("robot_ip", default_value="0.0.0.0"),
        DeclareLaunchArgument("local_ip", default_value="0.0.0.0"),
        DeclareLaunchArgument("use_fake_hardware", default_value="true"),
        DeclareLaunchArgument("headless_mode", default_value="false"),
        DeclareLaunchArgument("launch_rviz", default_value="true"),
        DeclareLaunchArgument(
            "initial_joint_controller",
            default_value="joint_trajectory_controller",
            choices=["scaled_joint_trajectory_controller", "joint_trajectory_controller"],
        ),
    ]
    forwarded = {name: LaunchConfiguration(name) for name in (
        "cs_type", "robot_ip", "local_ip", "use_fake_hardware",
        "headless_mode", "launch_rviz", "initial_joint_controller",
    )}
    forwarded.update({
        "tf_prefix": "cs63_",
        "description_package": "my_elite_robot_cell_control",
        "description_file": "my_elite_robot_cell_controlled.urdf.xacro",
        "runtime_config_package": "elite_robots_driver",
        "controllers_file": "elite_cs_controllers.yaml",
        "activate_joint_controller": "true",
    })
    driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(PathJoinSubstitution([
            FindPackageShare("elite_robots_driver"),
            "launch", "elite_control.launch.py",
        ])),
        launch_arguments=forwarded.items(),
    )
    return LaunchDescription(arguments + [driver])
