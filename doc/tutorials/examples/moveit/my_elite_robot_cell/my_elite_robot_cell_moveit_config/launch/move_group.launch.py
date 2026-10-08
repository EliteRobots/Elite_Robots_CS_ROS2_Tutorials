from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration
from moveit_configs_utils import MoveItConfigsBuilder
from moveit_configs_utils.launches import generate_move_group_launch


def launch_setup(context):
    fake = LaunchConfiguration("use_fake_hardware").perform(context) == "true"
    controller_file = (
        "config/moveit_controllers_fake.yaml" if fake
        else "config/moveit_controllers.yaml"
    )
    config = (
        MoveItConfigsBuilder(
            "my_elite_robot_cell",
            package_name="my_elite_robot_cell_moveit_config",
        )
        .trajectory_execution(file_path=controller_file)
        .planning_pipelines(pipelines=["ompl"])
        .to_moveit_configs()
    )
    return list(generate_move_group_launch(config).entities)


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument(
            "use_fake_hardware", default_value="true", choices=["true", "false"]),
        OpaqueFunction(function=launch_setup),
    ])
