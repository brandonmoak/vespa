# Host name must be defined here
hostname = 'first'
hostpath = '.'.join([__name__, hostname])
host = __import__(hostpath, fromlist=__name__)
