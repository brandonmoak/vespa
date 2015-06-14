import sys
import subprocess

host_group = 'basic_group'
commtype = 'udp'


def launch_windows_basic_locally():
    config_to_launch = ['first', 'second', 'third']
    for config in config_to_launch:
        subprocess.Popen([sys.executable,
                          'launcher.py',
                          '--agent',  config,
                          '--commtype', commtype,
                          '--host_group', host_group],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)

launch_windows_basic_locally()


def lanch_windows_simulation_locally():
    pass
