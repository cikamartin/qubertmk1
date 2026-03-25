import os
import subprocess
import tempfile
from launch import LaunchDescription
from launch_ros.actions import Node
import inspect

# Eloquent uses node_executable, Foxy+ uses executable
_node_params = inspect.signature(Node.__init__).parameters
_EXEC_KEY = 'node_executable' if 'node_executable' in _node_params else 'executable'
_ELOQUENT = 'node_executable' in _node_params


def generate_launch_description():
    this_dir = os.path.dirname(os.path.realpath(__file__))
    pkg_dir = os.path.dirname(this_dir)
    xacro_file = os.path.join(pkg_dir, 'urdf', 'qubertmk1.urdf.xacro')

    # Process xacro to URDF
    robot_description_xml = subprocess.check_output(
        ['xacro', xacro_file]
    ).decode('utf-8')

    nodes = []

    if _ELOQUENT:
        # Eloquent robot_state_publisher takes URDF file as argument
        urdf_tmp = os.path.join(tempfile.gettempdir(), 'qubertmk1.urdf')
        with open(urdf_tmp, 'w') as f:
            f.write(robot_description_xml)
        nodes.append(Node(
            package='robot_state_publisher',
            arguments=[urdf_tmp],
            output='screen',
            **{_EXEC_KEY: 'robot_state_publisher'},
        ))
    else:
        nodes.append(Node(
            package='robot_state_publisher',
            parameters=[{'robot_description': robot_description_xml}],
            output='screen',
            **{_EXEC_KEY: 'robot_state_publisher'},
        ))

    nodes.append(Node(
        package='joint_state_publisher',
        output='screen',
        **{_EXEC_KEY: 'joint_state_publisher'},
    ))

    return LaunchDescription(nodes)
