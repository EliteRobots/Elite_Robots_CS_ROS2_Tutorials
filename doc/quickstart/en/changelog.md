# Changelog

This chapter records changes to the published guide that affect its use. The document is versioned independently; see {ref}`Applicable versions <applicable-versions>` for matching package versions. Detailed source-code review records are kept in the repository's maintenance documentation.

## 1.0.0 (2026-11-03)

- Establish an independently versioned MyST quickstart guide with HTML and PDF output, organized by document type and language.
- Update installation, driver startup, service calls, controllers, and Python/C++ motion examples against the current workspace source code; correct parameter syntax and the units of `max_vel`.
- Update the MoveIt 2 launch command and add separate Gazebo startup steps, controller selection, and simulation clock checks.
- Organize figure numbering, file names, and references.
- Add a package version table: 1.2.0 for the ROS packages in the Driver repository, 1.0.0 for Description, and 1.4.7 for the SDK. The Gazebo package version is 1.0.2.
- Apply a shared HTML brand style with chapter navigation, an on-page table of contents, search, code copying, and mobile navigation.
- Add the English edition, including translated instructions, captions, and alternative text. Retain the existing screenshots and produce independent English HTML and PDF output.

This revision has undergone documentation builds and source-code review. Motion on physical hardware has not been verified.
