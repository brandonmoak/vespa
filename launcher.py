#! /usr/bin/python
# Launches an agent in a new window, currently only tested on windows
from subprocess import Popen, STDOUT
import psutil
import sys
import time


def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.get_children(recursive=True):
        proc.kill()
    process.kill()


if __name__ == '__main__':
    try:
        args = " ".join(sys.argv[1:])
        p = Popen('python -m vespa.agents.basic_agent {0}'.format(args),
                  stderr=STDOUT,
                  shell=True)
        while True:
            try:
                time.sleep(.1)
            except KeyboardInterrupt:
                print 'killing process'
                kill(p.pid)
                break

        raw_input("press enter to continue...")

    except Exception, e:
        raw_input(str(e) +
                  '\nError occuured during launch!'
                  '\nPress enter to continue...')
