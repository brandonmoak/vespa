import random
import string


class Enum(set):
    def __getattr__(self, name):
        if name in self:
            return name
        raise AttributeError(name + " not in enumeration " + str(type(self)))


def generate_random_string():
    return ''.join(random.SystemRandom().choice(
                   string.ascii_lowercase +
                   string.digits)
                   for _ in range(24))
