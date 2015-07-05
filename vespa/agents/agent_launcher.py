from agent_base import load_config
from vespa.utilities.util import get_default_parser

parser = get_default_parser()

if __name__ == '__main__':
    args = parser.parse_args()
    config = load_config(args.collection, args.agent)
    AgentLaunch = config._launcher
    AgentLaunch(config, args)
