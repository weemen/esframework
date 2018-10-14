""" Imports """
import abc
import re
from typing import List


class Event(object, metaclass=abc.ABCMeta):
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

    __uncommitted_events = []

    def __init__(self):
        self.__uncommitted_events = []

    def apply(self, event: Event):
        """ Apply an event and put it to the uncommitted events list """
        self.__uncommitted_events.append(event)
        self.apply_event(event)

    def apply_event(self, event):
        """ applies the actual event """
        method = "apply{0}".format(
            re.sub('([A-Z]+)', r'_\1', event.__class__.__name__).lower()
        )

        self.__getattribute__(method)(event)

    def get_uncommitted_events(self) -> List[Event]:
        """ returns the list of uncommitted events """
        return self.__uncommitted_events

    def clear_uncommitted_events(self):
        """ clear the list of uncommitted events """
        self.__uncommitted_events = []

    def initialize_state(self, list_of_events: List[Event]):
        """ initializes the default state of the aggregate root based on the
        list of incoming events
        """
        for event in list_of_events:
            self.apply_event(event)

    @abc.abstractmethod
    def get_aggregate_root_id():
        """ Every aggregate should have a function to get the aggregate id """
        raise NotImplementedError('Every aggregate must have an unique id!')
