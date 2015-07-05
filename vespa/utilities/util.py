import random
import string
import argparse


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


def get_default_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--collection',
                        help='group that agent is a member of')
    parser.add_argument('--agent',
                        help='name of agent that is to be launched')
    parser.add_argument('--comm',
                        help='type of communication that agents use')
    parser.add_argument('--commtype',
                        help='type of communication that agents use')
    parser.add_argument('--log_level',
                        help='severity of logging to print')
    parser.add_argument('--primary',
                        help='top level agent to be launched by actor')
    parser.add_argument('--actor',
                        help='name of actor')
    parser.add_argument('--actortype',
                        help='type of actor. [entity, executive...]')
    return parser

