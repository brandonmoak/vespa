import vespa.config.agents.agent as agent
import vespa.agents.transactor_agent
import config_base


class Config(agent.Config):
    _launcher = vespa.agents.transactor_agent.TransActorAgent
    address = config_base.OverrideRequired
    exec_address = config_base.OverrideRequired
