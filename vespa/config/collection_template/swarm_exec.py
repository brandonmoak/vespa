import vespa.config.swarm_exec as swarm_exec
import constraints


class Config(swarm_exec.Config):
    constraints = constraints.defined_constraints
    # address = ('127.0.0.1', 45010)

    