import agent
import vespa.agents.window_agent as window_agent


class Config(agent.Config):
    _launcher = window_agent.WindowAgent
    win_x = 400
    win_y = 300
    win_name = 'Simulator'
    mouse_x = 0
    mouse_y = 0
