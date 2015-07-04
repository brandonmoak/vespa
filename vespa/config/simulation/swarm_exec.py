import vespa.config.swarm_exec as swarm_exec
import constraints


class Config(swarm_exec.Config):
    address = ('127.0.0.2', 45001)
    constraints = constraints.defined_constraints
