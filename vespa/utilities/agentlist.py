class AgentList(list):
    def filter_agents(self,  agentname=None, agentid=None, agenttype=None, address=None):
        params = {'agentname': agentname,
                  'agentid': agentid,
                  'agenttype': agenttype,
                  'address': address}
        fil = self
        for k, val in params.iteritems():
            if val is not None:
                fil = filter(lambda x: getattr(x.config, k) == val, fil)
        return fil

    def first_agent_with(self, agentname=None, agentid=None, agenttype=None, address=None):
        fil = self.filter_agents(self. agentname, agentid, agenttype, address)
        return fil[0] if len(fil) > 0 else None
