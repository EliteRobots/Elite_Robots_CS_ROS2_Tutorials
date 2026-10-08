cmake_minimum_required(VERSION 3.16)
project(elite_robots_cs_tutorials)

find_package(ament_cmake REQUIRED)
find_package(Python3 REQUIRED COMPONENTS Interpreter)

option(BUILD_DOCS "Build the enabled manuals" ON)
option(BUILD_DOCS_PDF "Also build PDF manuals (requires LaTeX)" OFF)
set(DOCS_DOCUMENT "all" CACHE STRING "all or a document ID in doc/documents.json")
set(DOCS_LANGUAGE "all" CACHE STRING "all or a language code from doc/languages.json")

# Keep the documentation environment separate from ament's system Python.
# An empty override is resolved on every configure, so an old Python3 cache
# entry cannot prevent discovery of a newly created documentation environment.
set(DOCS_PYTHON_EXECUTABLE "" CACHE FILEPATH "Documentation Python; empty selects .venv/bin/python or Python3_EXECUTABLE")

if(BUILD_DOCS)
  if(DOCS_PYTHON_EXECUTABLE)
    set(_docs_python "${DOCS_PYTHON_EXECUTABLE}")
  elseif(EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python")
    set(_docs_python "${CMAKE_CURRENT_SOURCE_DIR}/.venv/bin/python")
  else()
    set(_docs_python "${Python3_EXECUTABLE}")
  endif()
  execute_process(
    COMMAND "${_docs_python}" -c "import sphinx, myst_parser"
    RESULT_VARIABLE _docs_import_result
    ERROR_VARIABLE _docs_import_error
    OUTPUT_QUIET)
  if(NOT "${_docs_import_result}" STREQUAL "0")
    message(FATAL_ERROR
      "Documentation Python: ${_docs_python}\n"
      "Cannot import Sphinx and MyST: ${_docs_import_error}\n"
      "Create .venv and install requirements.txt as described in README.md, "
      "or set -DDOCS_PYTHON_EXECUTABLE=/path/to/python with those dependencies. "
      "Use -DBUILD_DOCS=OFF to skip documentation.")
  endif()
  message(STATUS "Documentation Python: ${_docs_python}")
  set(DOCS_FORMAT html)
  if(BUILD_DOCS_PDF)
    set(DOCS_FORMAT all)
  endif()
  add_custom_target(manuals ALL
    COMMAND "${_docs_python}" "${CMAKE_CURRENT_SOURCE_DIR}/scripts/build_docs.py"
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
