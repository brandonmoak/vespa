import vespa.config.agent as agent
import vespa.agents.swarm_exec
import config_base


class Config(agent.Config):
    _launcher = vespa.agents.swarm_exec.SwarmExecutive
    # pointer to the constraints config file
    constraints = config_base.OverrideRequired
    # name
    name = 'swarm_exec'
    # address needs override in subclass
    # address = (ip, port)
    centroid = None

    @classmethod
    def resolve(config, agent_positions):
        # sets the target for the agent postiton
        # agent_positions = {'name' : {'pos': val, 'target': []}}
        for constraint in config.constraints:
            seln = [agent_positions[n]['pos'][:constraint.ndim] for n in constraint.agents]
            results = constraint.resolve(*seln)
            for name, result in zip(constraint.agents, results):
                agent_positions[name]['target'].append(result)
        return agent_positions

    @classmethod
    def position_template(config, agents):
        tem = {}
        for agent in agents:
            tem[agent] = {'pos': None, 'target': []}
        return tem

