from agent_base import get_default_parser, load_config

parser = get_default_parser()

if __name__ == '__main__':
    args = parser.parse_args()
    config = load_config(args.collection, args.agent)
    AgentLaunch = config._launcher
    AgentLaunch(config, args)
