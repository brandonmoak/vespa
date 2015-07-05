hostname = 'swarm_exec'
hostpath = '.'.join([__name__, hostname])
host = __import__(hostpath, fromlist=__name__)

