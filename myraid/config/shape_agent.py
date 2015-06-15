import agent
import myraid.agents.shape_agent as shape_agent


class Config(agent.Config):
    _launcher = shape_agent.ShapeAgent
    x = 0
    y = 0
    shape = 'circle'
    size = 15
