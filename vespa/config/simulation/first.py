import vespa.config.shape_agent as shape_agent


class Config(shape_agent.Config):
    address = ('127.0.0.1', 45001)
    name = 'first'
    # initial positions
    pos = None
