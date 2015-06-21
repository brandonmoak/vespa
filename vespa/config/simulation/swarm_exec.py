import vespa.config.swarm_exec as swarm_exec
import constraints


class Config(swarm_exec.Config):
    address = ('127.0.0.1', 45010)
    constraints = constraints.defined_constraints