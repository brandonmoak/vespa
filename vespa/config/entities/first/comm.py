import vespa.config.agents.comm as comm


class Config(comm.Config):
    name = 'comm'
    address = ('127.0.0.1', 45005)