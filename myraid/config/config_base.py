class OverrideRequired:
    def __str__(self):
        return 'Attribute must be over written in config'

class Config:
    @classmethod
    def attribute_set(config):
        attrs = set([key for key in config.__dict__ if\
                                ('__' not in key and type(config.__dict__[key]) != classmethod)])
        if len(config.__bases__) > 0:
            return config.__bases__[0].attribute_set().union(attrs)
        return attrs

    @classmethod
    def attribute_list(config):
        return list(config.attribute_set())

    @classmethod
    def verify_override(config):
        attrs = config.attribute_list()
        for attr in attrs:
            if getattr(config, attr) == OverrideRequired:
                mod = config.__dict__['__module__']
                raise NotImplementedError('{0} must be overridden in subconfig {1}'.format(attr, mod))