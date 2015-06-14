import config_base


class Config(config_base.Config):
    """
    data that exists in the agent, must be predefined here
    so that the local copies of networked agents can store
    these attributes

    """
    # location of agent
    address = object
    # address of host agent
    hostaddr = object
    # agent id generated when agent spawns
    agentid = str
    # name of agent
    name = str
    # type of agent
    agenttype = str
