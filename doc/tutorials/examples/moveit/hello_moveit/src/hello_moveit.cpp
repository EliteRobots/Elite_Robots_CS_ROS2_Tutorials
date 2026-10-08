// Adapted from Elite Robots ROS 2 tutorials (Apache-2.0).
#include <exception>
#include <memory>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

#include <geometry_msgs/msg/pose.hpp>
#include <moveit/move_group_interface/move_group_interface.h>
#include <rclcpp/rclcpp.hpp>

int main(int argc, char * argv[])
{
  rclcpp::init(argc, argv);
  auto node = std::make_shared<rclcpp::Node>(
    "hello_moveit",
    rclcpp::NodeOptions().automatically_declare_parameters_from_overrides(true));
  if (!node->has_parameter("execute")) {
    node->declare_parameter("execute", false);
  }
  const bool execute = node->get_parameter("execute").as_bool();
  const auto logger = node->get_logger();
  rclcpp::executors::SingleThreadedExecutor executor;
  executor.add_node(node);
  std::thread spinner([&executor]() { executor.spin(); });
  int result = 0;
  try {
    using moveit::planning_interface::MoveGroupInterface;
    MoveGroupInterface arm(node, "elite_arm");
    arm.setPoseReferenceFrame("world");
    arm.setEndEffectorLink("cs63_tool0");
    arm.setMaxVelocityScalingFactor(0.1);
    arm.setMaxAccelerationScalingFactor(0.1);
    arm.setPlanningTime(10.0);
    if (!arm.getCurrentState(10.0)) {
      throw std::runtime_error("No current joint state; check the driver and joint_states.");
    }
    auto plan_target = [&](const std::string & label) {
      arm.setStartStateToCurrentState();
      MoveGroupInterface::Plan plan;
      if (arm.plan(plan) != moveit::core::MoveItErrorCode::SUCCESS) {
        RCLCPP_ERROR(logger, "%s planning failed", label.c_str());
        return false;
      }
      RCLCPP_INFO(logger, "%s planned; execute=%s", label.c_str(), execute ? "true" : "false");
      if (execute && arm.execute(plan) != moveit::core::MoveItErrorCode::SUCCESS) {
        RCLCPP_ERROR(logger, "%s execution failed", label.c_str());
        return false;
      }
      return true;
    };

    geometry_msgs::msg::Pose pose;
    pose.orientation.w = 1.0;
    pose.position.x = 1.3;
    pose.position.y = 0.3;
    pose.position.z = 1.5;
    if (!arm.setPoseTarget(pose) || !plan_target("pose")) {
      result = 1;
    } else {
      arm.clearPoseTargets();
      const std::vector<std::string> names = {
        "cs63_shoulder_pan_joint", "cs63_shoulder_lift_joint", "cs63_elbow_joint",
        "cs63_wrist_1_joint", "cs63_wrist_2_joint", "cs63_wrist_3_joint"};
      const std::vector<double> values = {0.0, -0.5, 0.3, -1.2, 0.8, 0.5};
      if (!arm.setJointValueTarget(names, values) || !plan_target("joints")) {
        result = 1;
      }
    }
  } catch (const std::exception & error) {
    RCLCPP_ERROR(logger, "%s", error.what());
    result = 1;
  }
  executor.cancel();
  spinner.join();
  rclcpp::shutdown();
  return result;
}
