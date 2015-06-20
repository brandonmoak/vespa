import vespa.config.agent as agent
import vespa.agents.basic_agent


class Config(agent.Config):
    _launcher = vespa.agents.basic_agent.BasicAgent