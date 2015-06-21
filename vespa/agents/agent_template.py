import agent_base
# from vespa.event.messagehandler import message_handler

###############################################################
# Arguments passed from launching the agent
# to add argument try parser.add_argument()
###############################################################

parser = agent_base.get_default_parser()
args = parser.parse_args()


###############################################################
# Definition of customized agent
###############################################################

class Agent(agent_base.AgentBase):
    """
    An actor is a node on the network, its process runs independantly of
    other nodes on the nework, each node must register with the swarm executive to
    get its positional information. An actor load a configuration file from 
    config directory, which will define the workers(agents) that will execute commands
    such as reading and writing to drivers. Each agent/actor communicates through predefined 
    messages that can be subscribed to. A network of actors is called a collection,
    the colleaction has an executive that all nodes will initialize with, following
    that the nodes can communicate with each other directly based on their
    specified function.
    """
    def __init__(self, config, args):
        super(Agent, self).__init__(config, args)

    def tick(self, dt):
        """
        called on a regular basis, this is the main loop for each agent
        to process its own tasks
        """
        print 'tick'

# ################# MESSAGE HANDLERS #######################
# To subscribe message to predefined message type
#
# self.handler.subscribe_to_message_type(message.Type,
#                           self.how_to_handle_message)
#
# To create Message Handlers
# @message_handler(message.Type)
# def how_to_handle_message(self, message):
#     message.contains.attributes
# ##########################################################


# ################# NETWORKED AGENTS #######################
# To communicate with agents seen on the network that have
# been predefined in config
# self.networkedagents['name'].send_to(message)
# ##########################################################

if __name__ == '__main__':
    Agent(agent_base.load_config(args.collection, args.agent), args)
