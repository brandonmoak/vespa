import myraid.config.window_agent as window_agent

class Config(window_agent.Config):
    address = ('127.0.0.1', 45001)
    name = 'window'