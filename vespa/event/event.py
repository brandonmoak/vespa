import time
import pickle

from vespa.utilities.helpers import generate_random_string, Enum


class Event(object):
    """
    Base event class, to be overridden to create specific event types

    """
    def __init__(self, senderid, event_type, **data):
        # Uses KWARGS for data to be passed in the event object, keywords must match the
        # attrs in the event type.
        assert issubclass(event_type, EventType)
        self.senderid = senderid
        self.eventid = generate_random_string()
        self.timestamp = time.time()
        self.event_type = event_type
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
        return ', '.join(map(str, [self.senderid,
                                   self.eventid,
                                   self.timestamp,
                                   self.event_type,
                                   self.data]))

    def flatten(self):
        st = pickle.dumps(self)
        return st
        # check if all field are filled in

    @classmethod
    def unflatten(self, msg):
        return pickle.loads(msg)
        # recontruct event object

# ##################### Target Type ###########################
# message can be sent to, all, local, networked

BroadcastLevel = Enum(['local', 'all', 'networked'])


# ##################### Event Type ############################
# Each event type must define its specific data atributes

class EventType:
    attrs = []


class TransAction:
    attrs = ['event', 'interface', 'target']


class LocalRegistrationRequest(EventType):
    attrs = ['name', 'actor', 'interfaces']


class LocalRegistrationConfirmed(EventType):
    attrs = ['name', 'actor', 'interfaces']


class Heartbeat(EventType):
    attrs = ['status']


class Shutdown(EventType):
    attrs = ['errors']


class IdentifierExchange(EventType):
    attrs = ['actor', 'address', 'identifiers']
