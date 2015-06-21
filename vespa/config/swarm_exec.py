import vespa.config.agent as agent
import vespa.agents.swarm_exec
import config_base


class Config(agent.Config):
    _launcher = vespa.agents.swarm_exec.SwarmExecutive
    # pointer to the constraints config file
    constraints = config_base.OverrideRequired
    # name
    name = 'swarm_exec'
    # address = needs override in subclass
    # address = (ip, port)

