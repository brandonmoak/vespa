import vespa.config.window_agent as window_agent


class Config(window_agent.Config):
    address = ('127.0.0.3', 45001)
    name = 'window'
