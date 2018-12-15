""" Imports """
import abc
import datetime
import re

from typing import List

from esframework.exceptions import DomainEventException


class Event(object, metaclass=abc.ABCMeta):

    __causation_id = None
    __correlation_id = None
    __event_date = datetime.datetime.now().isoformat()
    __event_id = None
    __metadata = list()
    __version = None

    def __init__(self):
        self.__causation_id = None
        self.__correlation_id = None
        self.__event_date = datetime.datetime.now().isoformat()
        self.__event_id = None
        self.__metadata = list()
        self.__version = None

    def get_version(self) -> int:
        return self.__version

    def set_version(self, version_number: int):
        if self.__version is not None:
            raise DomainEventException("Version can only be set once!")
        self.__version = version_number

    def get_causation_id(self) -> str:
        return self.__causation_id

    def set_causation_id(self, causation_id: str):
        if self.__causation_id is not None:
            raise DomainEventException("Causation id can only be set once!")
        self.__causation_id = causation_id

    def get_correlation_id(self) -> str:
        return self.__correlation_id

    def set_correlation_id(self, correlation_id: str):
        if self.__correlation_id is not None:
            raise DomainEventException("Correlation id can only be set once!")
        self.__correlation_id = correlation_id

    def get_event_id(self) -> str:
        return self.__event_id

    def set_event_id(self, event_id: str):
        if self.__event_id is not None:
            raise DomainEventException("Event id can only be set once!")
        self.__event_id = event_id

    def get_event_date(self) -> str:
        return self.__event_date

    def get_metadata(self, include_classname=False):
        if include_classname:
            return self.__metadata

        clean_list = []
        for metadata in self.__metadata:
            for key in metadata:
                metadata[key] = metadata[key].replace(
                    "_{}".format(self.__class__.__name__),
                    "")
            clean_list.append(metadata)
        return clean_list

    def add_metadata(self, key: str, event_property: str):
        event_property = "_{}{}".format(
            self.__class__.__name__, event_property)

        if event_property not in self.__dict__:
            raise DomainEventException(
                "Can't set metadata on non existing event properties")

        value = {key: event_property}
        if value in self.__metadata:
            raise DomainEventException("Metadata is already set!")
        self.__metadata.append(value)

    def remove_metadata(self, key, event_property):
        value = {key: event_property}
        if value not in self.__metadata:
            raise DomainEventException("Can't remove non existent metadata!")
        self.__metadata.remove(value)


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
        self.__loaded_version = 0
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
