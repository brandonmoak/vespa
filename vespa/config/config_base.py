class Config:
    @classmethod
    def attribute_set(config):
        attrs = set([key for key in config.__dict__ if
                    ('__' not in key and type(config.__dict__[key]) != classmethod)])
        if len(config.__bases__) > 0:
            return config.__bases__[0].attribute_set().union(attrs)
        return attrs

    @classmethod
    def attribute_list(config):
        list(config.attribute_set())
