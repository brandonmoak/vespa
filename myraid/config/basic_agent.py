import myraid.config.agent as agent
import myraid.agents.basic_agent


class Config(agent.Config):
    _launcher = myraid.agents.basic_agent.BasicAgent