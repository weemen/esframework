import abc
import re
from typing import List


class Event(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def serialize(self):
        raise NotImplementedError('an event must be serializable')

    @staticmethod
    @abc.abstractmethod
    def deserialize(event_data):
        raise NotImplementedError('an event must be deserializable')


class AggregateRoot(object):

    __uncommitted_events = []

    def __init__(self):
        self.__uncommitted_events = []

    def apply(self, event: Event):
        self.__uncommitted_events.append(event)
        self.apply_event(event)

    def apply_event(self, event):
        method = "apply{0}".format(
            re.sub('([A-Z]+)', r'_\1', event.__class__.__name__).lower()
        )

        self.__getattribute__(method)(event)

    def get_uncommitted_events(self) -> List[Event]:
        return self.__uncommitted_events

    def clear_uncommited_events(self):
        self.__uncommitted_events = []

    def initialize_state(self, list_of_events: List[Event]):
        for event in list_of_events:
            self.apply_event(event)

    @abc.abstractmethod
    def get_aggregate_root_id(self):
        raise NotImplementedError('Every aggregate must have an unique id!')