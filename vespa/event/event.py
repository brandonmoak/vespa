import time
import pickle

from vespa.utilities.helpers import generate_random_string


class Event(object):
    """
    Base event class, to be overridden to create specific event types
    """
    eventid = None
    senderid = None
    recieverid = None
    eventid = None
    timestamp = None

    def __init__(self, senderid, recieverid):
        self.senderid = senderid
        self.recieverid = recieverid
        self.eventid = generate_random_string()
        self.timestamp = time.time()
        self.event_type = str(self)

    def __str__(self):
        return self.__class__.__name__

    def flatten(self):
        st = pickle.dumps(self)
        return st
        # check if all field are filled in

    @classmethod
    def unflatten(self, msg):
        return pickle.loads(msg)
        # recontruct event object


class RegistrationRequest(Event):
    def __init__(self, collection, name, agenttype, senderid, senderaddr):
        super(RegistrationRequest, self).__init__(senderid, 'exec')
        self.name = name
        self.senderaddr = senderaddr
        self.type = agenttype
        self.collection = collection


class RegistrationConfirmed(Event):
    def __init__(self, collection, name, agenttype, senderid):
        super(RegistrationConfirmed, self).__init__(senderid, 'undefined')
        self.name = name
        self.type = agenttype
        self.collection = collection


class Heartbeat(Event):
    pass


class Shutdown(Event):
    pass
