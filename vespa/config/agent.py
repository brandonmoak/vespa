import config_base


class Config(config_base.Config):
    """
    data that exists in the agent, must be predefined here
    so that the local copies of networked agents can store
    these attributes

    """
    # reference to the Agent class that will run
    _launcher = config_base.OverrideRequired
    # location of agent
    address = config_base.OverrideRequired
    # port
    # port = 45750
    # address of host agent
    hostaddr = object
    # agent id generated when agent spawns
    agentid = str
    # name of agent
    name = config_base.OverrideRequired
    # type of agent
    agenttype = str
    # local agents to run
    local_agents = []
