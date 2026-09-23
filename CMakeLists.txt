cmake_minimum_required(VERSION 3.16)
project(elite_robots_cs_tutorials)

find_package(ament_cmake REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

option(BUILD_DOCS "Build the enabled manuals" ON)
option(BUILD_DOCS_PDF "Also build PDF manuals (requires LaTeX)" OFF)
set(DOCS_DOCUMENT "all" CACHE STRING "all, quickstart, usage, or interfaces")
set(DOCS_LANGUAGE "all" CACHE STRING "all or a language code from doc/languages.json")

if(BUILD_DOCS)
  set(DOCS_FORMAT html)
  if(BUILD_DOCS_PDF)
    set(DOCS_FORMAT all)
  endif()
  add_custom_target(manuals ALL
    COMMAND "${Python3_EXECUTABLE}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/build_docs.py"
      --document "${DOCS_DOCUMENT}" --language "${DOCS_LANGUAGE}"
      --format "${DOCS_FORMAT}"
      --output "${CMAKE_CURRENT_BINARY_DIR}/docs"
    WORKING_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}"
    COMMENT "Building independent Elite ROS 2 manuals"
    VERBATIM)
  install(DIRECTORY "${CMAKE_CURRENT_BINARY_DIR}/docs/"
    DESTINATION "share/${PROJECT_NAME}/manuals"
    PATTERN doctrees EXCLUDE
    PATTERN latex EXCLUDE)
endif()

install(DIRECTORY doc scripts DESTINATION "share/${PROJECT_NAME}"
  PATTERN __pycache__ EXCLUDE)
install(FILES README.md requirements.txt MAINTENANCE.md
  DESTINATION "share/${PROJECT_NAME}")
ament_package()
