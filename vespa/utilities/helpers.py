import random
import string


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name + " is not a member of enumeration " + str(type(self)))


class LoggingMixIn:
    pass


def generate_random_string():
    return ''.join(random.SystemRandom().choice(string.ascii_lowercase + string.digits) for _ in range(24))
