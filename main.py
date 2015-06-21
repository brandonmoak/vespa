import sys
import subprocess


def launch_windows_basic_locally():
    '''
    run in windows terminal or powershell
    '''
    collection = 'basic_group'
    commtype = 'udp'
    config_to_launch = ['first', 'second', 'third']
    for config in config_to_launch:
        subprocess.Popen([sys.executable,
                          'launcher.py',
                          '--agent',  config,
                          '--commtype', commtype,
                          '--collection', collection],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
# launch_windows_basic_locally()


def lanch_windows_simulation_locally():
    '''
    run in windows terminal or powershell
    '''
    collection = 'simulation'
    commtype = 'udp'
    config_to_launch = ['window', 'first', 'swarm_exec']
    for config in config_to_launch:
        subprocess.Popen([sys.executable,
                          'launcher.py',
                          '--agent',  config,
                          '--commtype', commtype,
                          '--collection', collection],
                         creationflags=subprocess.CREATE_NEW_CONSOLE)
lanch_windows_simulation_locally()
