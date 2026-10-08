cmake_minimum_required(VERSION 3.5)
project(my_elite_robot_cell_control)

find_package(ament_cmake REQUIRED)

install(
  DIRECTORY launch urdf rviz
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY ../my_elite_robot_cell_description/config/
  DESTINATION share/${PROJECT_NAME}/config)

ament_package()
