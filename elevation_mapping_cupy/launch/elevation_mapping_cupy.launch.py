from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory
import launch_ros.actions

def generate_launch_description():
    elevation_mapping_cupy_dir = get_package_share_directory('elevation_mapping_cupy')

    rviz_config = PathJoinSubstitution([
        elevation_mapping_cupy_dir, 'rviz', 'normal_map.rviz'  
    ])

    return LaunchDescription([
        launch_ros.actions.SetParameter(name='use_sim_time', value=True),
        Node(
            package='elevation_mapping_cupy',
            executable='elevation_mapping_node',
            name='elevation_mapping',
            parameters=[
                PathJoinSubstitution([
                    elevation_mapping_cupy_dir,
                    'config',
                    'core',
                    'core_param.yaml'
                ]),
                PathJoinSubstitution([
                    elevation_mapping_cupy_dir,
                    'config',
                    'core',
                    'example_setup.yaml'
                ])
            ],
            output='screen'
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            parameters=[{'use_sim_time': False}],
            output='screen'
        )
    ])










# from launch import LaunchDescription
# from launch_ros.actions import Node
# from launch.substitutions import PathJoinSubstitution
# from ament_index_python.packages import get_package_share_directory
# import launch_ros.actions

# def generate_launch_description():
#     elevation_mapping_cupy_dir = get_package_share_directory('elevation_mapping_cupy')

#     return LaunchDescription([
#         launch_ros.actions.SetParameter(name='use_sim_time', value=True),
#         Node(
#             package='elevation_mapping_cupy',
#             executable='elevation_mapping_node',
#             name='elevation_mapping',
#             parameters=[
#                 PathJoinSubstitution([
#                     elevation_mapping_cupy_dir,
#                     'config',
#                     'core',
#                     'core_param.yaml'
#                 ]),
#                 PathJoinSubstitution([
#                     elevation_mapping_cupy_dir,
#                     'config',
#                     'core',
#                     'example_setup.yaml'
#                 ])
#             ],
#             output='screen'
#         )
#     ]) 