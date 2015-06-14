import time
import pickle

from myraid.utilities.helpers import generate_random_string


class Message(object):
    """
    Base message class, to be overridden to create specific message types
    """
    messageid = None
    senderid = None
    recieverid = None
    messageid = None
    timestamp = None

    def __init__(self, senderid, recieverid):
        self.senderid = senderid
        self.recieverid = recieverid
        self.messageid = generate_random_string()
        self.timestamp = time.time()
        self.message_type = str(self)

    def __str__(self):
        return self.__class__.__name__

    def flatten(self):
        st = pickle.dumps(self)
        return st
        # check if all field are filled in

    @classmethod
    def unflatten(self, msg):
        return pickle.loads(msg)
        # recontruct message object


class Registration(Message):
    def __init__(self, host_group, name, agenttype, senderid, senderaddr):
        super(Registration, self).__init__(senderid, 'host')
        self.name = name
        self.senderaddr = senderaddr
        self.type = agenttype
        self.host_group = host_group


class Heartbeat(Message):
    pass


class Shutdown(Message):
    pass
