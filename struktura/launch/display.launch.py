import os
import subprocess
from launch import LaunchDescription
from launch_ros.actions import Node

# Eloquent uses node_executable, Foxy+ uses executable
import inspect
_node_params = inspect.signature(Node.__init__).parameters
_EXEC_KEY = 'node_executable' if 'node_executable' in _node_params else 'executable'


def generate_launch_description():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    pkg_dir = os.path.dirname(this_dir)
    xacro_file = os.path.join(pkg_dir, 'urdf', 'qubertmk1.urdf.xacro')

    # Run xacro in subprocess to handle spaces in path
    robot_description_xml = subprocess.check_output(
        ['xacro', xacro_file]
    ).decode('utf-8')

    return LaunchDescription([
        Node(
            package='robot_state_publisher',
            parameters=[{'robot_description': robot_description_xml}],
            **{_EXEC_KEY: 'robot_state_publisher'},
        ),
        Node(
            package='joint_state_publisher_gui',
            **{_EXEC_KEY: 'joint_state_publisher_gui'},
        ),
        Node(
            package='rviz2',
            arguments=['-d', os.path.join(pkg_dir, 'rviz', 'qubertmk1.rviz')],
            **{_EXEC_KEY: 'rviz2'},
        ),
    ])
