import time
import pickle

from vespa.utilities.helpers import generate_random_string, Enum


class Event(object):
    """
    Base event class, to be overridden to create specific event types

    """
    def __init__(self, senderid, event_type, target='local', **data):
        # Uses KWARGS for data to be passed in the event object, keywords must match the
        # attrs in the event type.
        assert issubclass(event_type, EventType)
        self.senderid = senderid
        self.eventid = generate_random_string()
        self.timestamp = time.time()
        self.event_type = event_type
        self.target = target
        self.data = data
        self.check_data_from_kwargs()

    def check_data_from_kwargs(self):
        for attr in self.event_type.attrs:
            try:
                self.data[attr]
            except AttributeError:
                raise AttributeError(
                    'event object was not initialized with attribute: {0}'.format(attr))

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

# ##################### Target Type ###########################
# message can be sent to, all, local, or specific agentid

Target = Enum(['local', 'all'])


# ##################### Event Type ############################
# Each event type must define its specific data atributes

class EventType:
    attrs = []


class RegistrationRequest(EventType):
    attrs = ['name', 'senderaddr', 'actortype', 'interfaces']


class RegistrationConfirmed(EventType):
    attrs = ['name', 'senderaddr', 'actortype', 'interfaces']


class Heartbeat(EventType):
    attrs = ['status']


class Shutdown(EventType):
    attrs = ['errors']
