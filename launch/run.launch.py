import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    share_dir = get_package_share_directory('lio_sam_mid360')
    parameter_file = LaunchConfiguration('params_file')
    rviz_config_file = os.path.join(share_dir, 'config', 'rviz2.rviz')

    params_declare = DeclareLaunchArgument(
        'params_file',
        default_value=os.path.join(share_dir, 'config', 'params.yaml'),
        description='Full path to the ROS2 parameters file to use.'
    )

    return LaunchDescription([
        params_declare,

        # --- Static TFs ---
        # map -> odom (example, already present)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0', '0', '0', '0', '0', '0', 'map', 'odom'],
            output='screen'
        ),

        # base_link -> lidar_link
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0.7646', '0.0', '0.93514',
                       '0.0', '0.0', '0.0',
                       'base_link', 'lidar_link'],
            output='screen'
        ),

        # base_link -> imu_link  (same coordinates since Livox IMU is co-located)
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=['0.7646', '0.0', '0.93514',
                       '0.0', '0.0', '0.0',
                       'base_link', 'imu_link'],
            output='screen'
        ),

        # --- LIO-SAM Nodes ---
        Node(
            package='lio_sam_mid360',
            executable='imuPreintegration',
            name='imuPreintegration',
            parameters=[parameter_file],
            output='screen'
        ),
        Node(
            package='lio_sam_mid360',
            executable='imageProjection',
            name='imageProjection',
            parameters=[parameter_file],
            output='screen'
        ),
        Node(
            package='lio_sam_mid360',
            executable='featureExtraction',
            name='featureExtraction',
            parameters=[parameter_file],
            output='screen'
        ),
        Node(
            package='lio_sam_mid360',
            executable='mapOptimization',
            name='mapOptimization',
            parameters=[parameter_file],
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_file],
            output='screen'
        )
    ])

