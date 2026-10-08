from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
from moveit_configs_utils import MoveItConfigsBuilder


def generate_launch_description():
    config = (
        MoveItConfigsBuilder(
            "my_elite_robot_cell",
            package_name="my_elite_robot_cell_moveit_config",
        )
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    return LaunchDescription([
        DeclareLaunchArgument("execute", default_value="false"),
        Node(
            package="hello_moveit", executable="hello_moveit", output="screen",
            parameters=[
                config.robot_description,
                config.robot_description_semantic,
                config.robot_description_kinematics,
                {"execute": ParameterValue(LaunchConfiguration("execute"), value_type=bool)},
            ],
        ),
    ])
