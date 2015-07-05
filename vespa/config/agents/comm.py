import vespa.config.agents.agent as agent
import vespa.agents.comm_agent
import config_base


class Config(agent.Config):
    _launcher = vespa.agents.comm_agent.CommAgent
    address = config_base.OverrideRequired
