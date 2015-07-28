import vespa.config.agents.transactor as transactor


class Config(transactor.Config):
    name = 'transactor'
    address = ('127.0.0.1', 45005)
    exec_address = ('127.0.0.10', 45005)
