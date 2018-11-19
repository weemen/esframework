""" Imports """
import abc
from typing import List
from esframework.domain import DomainEvent
from esframework.exceptions import AggregateRootIdNotFoundError


class Store(object):
    """ Abstract class for a storing event streams """

    @abc.abstractmethod
    def load(self, aggregate_root_id: str):
        """ Should be implemented by child class for loading from storage """
        raise NotImplementedError('Every repository must have an load method.')

    @abc.abstractmethod
    def save(self, event_stream: List[DomainEvent], aggregate_root_id: str):
        """ Should be implemented by child class for saving to storage """
        raise NotImplementedError('Every repository must have an save method.')


class InMemoryStore(Store):
    """ An in memory event store """

    __store = {}

    def __init__(self):
        self.__store = {}

    def load(self, aggregate_root_id: str) -> List[DomainEvent]:
        """ Load stream from memory """
        if aggregate_root_id not in self.__store:
            raise AggregateRootIdNotFoundError(
                'Aggregate root id does not exist',
                aggregate_root_id)

        return self.__store[aggregate_root_id]

    def save(self, event_stream: List[DomainEvent], aggregate_root_id: str):
        """ Store / Append stream to memory """

        """ overwriting the event stream is not ok """
        if aggregate_root_id not in self.__store:
            self.__store[aggregate_root_id] = event_stream
        else:
            self.__store[aggregate_root_id] += event_stream
