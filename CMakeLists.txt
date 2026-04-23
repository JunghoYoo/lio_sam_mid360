cmake_minimum_required(VERSION 3.5)
project(lio_sam_mid360)

# =========================
# Build type
# =========================
if(NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
  set(CMAKE_BUILD_TYPE Release)
endif()

# =========================
# Dependencies
# =========================
find_package(ament_cmake REQUIRED)

find_package(rclcpp REQUIRED)
find_package(rclpy REQUIRED)

find_package(std_msgs REQUIRED)
find_package(sensor_msgs REQUIRED)
find_package(geometry_msgs REQUIRED)
find_package(nav_msgs REQUIRED)
find_package(visualization_msgs REQUIRED)

find_package(cv_bridge REQUIRED)

find_package(pcl_conversions REQUIRED)
find_package(pcl_msgs REQUIRED)

find_package(tf2 REQUIRED)
find_package(tf2_ros REQUIRED)
find_package(tf2_geometry_msgs REQUIRED)
find_package(tf2_sensor_msgs REQUIRED)
find_package(tf2_eigen REQUIRED)

find_package(OpenCV REQUIRED)
find_package(PCL REQUIRED)
find_package(GTSAM REQUIRED)
find_package(Eigen3 REQUIRED)
find_package(OpenMP REQUIRED)

# =========================
# ROS2 interfaces (ONLY ONCE)
# =========================
find_package(rosidl_default_generators REQUIRED)

rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/CloudInfo.msg"
  "srv/SaveMap.srv"
  DEPENDENCIES std_msgs sensor_msgs
)

# =========================
# Include directories
# =========================
include_directories(
  include/lio_sam
  ${PCL_INCLUDE_DIRS}
  ${OpenCV_INCLUDE_DIRS}
)

add_definitions(${PCL_DEFINITIONS})

# =========================
# Executable: featureExtraction
# =========================
add_executable(featureExtraction src/featureExtraction.cpp)

ament_target_dependencies(featureExtraction
  rclcpp rclpy
  std_msgs sensor_msgs geometry_msgs nav_msgs visualization_msgs
  pcl_conversions pcl_msgs
  tf2 tf2_ros tf2_eigen tf2_geometry_msgs tf2_sensor_msgs
  OpenCV PCL
)

add_dependencies(featureExtraction ${PROJECT_NAME})

# =========================
# Executable: imageProjection
# =========================
add_executable(imageProjection src/imageProjection.cpp)

ament_target_dependencies(imageProjection
  rclcpp rclpy
  std_msgs sensor_msgs geometry_msgs nav_msgs visualization_msgs
  pcl_conversions pcl_msgs
  tf2 tf2_ros tf2_eigen tf2_geometry_msgs tf2_sensor_msgs
  OpenCV PCL
)

add_dependencies(imageProjection ${PROJECT_NAME})

# =========================
# Executable: imuPreintegration
# =========================
add_executable(imuPreintegration src/imuPreintegration.cpp)

ament_target_dependencies(imuPreintegration
  rclcpp rclpy
  std_msgs sensor_msgs geometry_msgs nav_msgs visualization_msgs
  pcl_conversions pcl_msgs
  tf2 tf2_ros tf2_eigen tf2_geometry_msgs tf2_sensor_msgs
  OpenCV PCL
  GTSAM Eigen3
)

target_link_libraries(imuPreintegration
  gtsam
)

add_dependencies(imuPreintegration ${PROJECT_NAME})

# =========================
# Executable: mapOptimization
# =========================
add_executable(mapOptimization src/mapOptimization.cpp)

ament_target_dependencies(mapOptimization
  rclcpp rclpy
  std_msgs sensor_msgs geometry_msgs nav_msgs visualization_msgs
  pcl_conversions pcl_msgs
  tf2 tf2_ros tf2_eigen tf2_geometry_msgs tf2_sensor_msgs
  OpenCV PCL
  GTSAM
)
ament_target_dependencies(featureExtraction rosidl_default_runtime)
ament_target_dependencies(imageProjection rosidl_default_runtime)
ament_target_dependencies(mapOptimization rosidl_default_runtime)
ament_target_dependencies(imuPreintegration rosidl_default_runtime)

target_link_libraries(mapOptimization
  gtsam
)

if(OpenMP_CXX_FOUND)
  target_link_libraries(mapOptimization OpenMP::OpenMP_CXX)
endif()

add_dependencies(mapOptimization ${PROJECT_NAME})

rosidl_target_interfaces(featureExtraction
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

rosidl_target_interfaces(imageProjection
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

rosidl_target_interfaces(mapOptimization
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

rosidl_target_interfaces(imuPreintegration
  ${PROJECT_NAME} "rosidl_typesupport_cpp")

# =========================
# Install
# =========================
install(TARGETS
  featureExtraction
  imageProjection
  imuPreintegration
  mapOptimization
  DESTINATION lib/${PROJECT_NAME}
)

install(DIRECTORY
  launch
  config
  DESTINATION share/${PROJECT_NAME}
)

install(DIRECTORY include/
  DESTINATION include
)

# =========================
# Export
# =========================
ament_export_include_directories(include)
ament_package()