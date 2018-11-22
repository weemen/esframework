""" Imports """
import abc
import re
from typing import List


class Event(object, metaclass=abc.ABCMeta):

    __version = None

    def __init__(self):
        self.__version = None

    def set_version(self, version_number: int):
        self.__version = version_number

    def get_version(self):
        return self.__version


class DomainEvent(Event):
    """ Abstract event class with serialize and deserialize method """

    @abc.abstractmethod
    def serialize(self):
        """ serialize event when implemented by child class """
        raise NotImplementedError('an event must be serializable')

    @staticmethod
    @abc.abstractmethod
    def deserialize(event_data):
        """ deserialize event when implemented by child class """
        raise NotImplementedError('an event must be deserializable')


class AggregateRoot(object):
    """ A base aggregate root class with basics already implemented """
    __loaded_version = 0
    __uncommitted_events = []

    def __init__(self):
        __loaded_version = 0
        self.__uncommitted_events = []

    def apply(self, event: DomainEvent):
        """ Apply an event and put it to the uncommitted events list """
        event_version = self.__loaded_version + len(self.__uncommitted_events) + 1
        event.set_version(event_version)

        self.__uncommitted_events.append(event)
        self.apply_event(event)

    def apply_event(self, event):
        """ applies the actual event """
        method = "apply{0}".format(
            re.sub('([A-Z]+)', r'_\1', event.__class__.__name__).lower()
        )

        self.__getattribute__(method)(event)

    def get_uncommitted_events(self) -> List[DomainEvent]:
        """ returns the list of uncommitted events """
        return self.__uncommitted_events

    def clear_uncommitted_events(self):
        """ clear the list of uncommitted events """
        self.__uncommitted_events = []

    def initialize_state(self, list_of_events: List[DomainEvent]):
        """ initializes the default state of the aggregate root based on the
        list of incoming events
        """
        for event in list_of_events:
            self.apply_event(event)
            self.__loaded_version += 1

    def get_version(self) -> int:
        """ returns the initialized state version """
        return self.__loaded_version

    @abc.abstractmethod
    def get_aggregate_root_id(self):
        """ Every aggregate should have a function to get the aggregate id """
        raise NotImplementedError('Every aggregate must have an unique id!')
