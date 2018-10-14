""" Imports """
import abc
from typing import List
from esframework.domain import Event
from esframework.exceptions import AggregateRootIdNotFoundError


class Store(object):
    """ Abstract class for a storing event streams """

    @abc.abstractmethod
    def load(self, aggregate_root_id: str):
        """ Should be implemented by child class for loading from storage """
        raise NotImplementedError('Every repository must have an load method.')

    @abc.abstractmethod
    def save(self, event_stream: List[Event], aggregate_root_id: str):
        """ Should be implemented by child class for saving to storage """
        raise NotImplementedError('Every repository must have an save method.')


class InMemoryStore(Store):
    """ An in memory event store """

    __store = []

    def load(self, aggregate_root_id: str) -> List[Event]:
        """ Load stream from memory """
        try:
            return self.__store[aggregate_root_id]
        except ValueError:
            raise AggregateRootIdNotFoundError(
                'Aggregate root id does not exist',
                aggregate_root_id)

    def save(self, event_stream: List[Event], aggregate_root_id: str):
        """ Store / Append stream to memory """

        if self.__store[aggregate_root_id] is None:
            self.__store[aggregate_root_id] = event_stream
        else:
            self.__store[aggregate_root_id].append(event_stream)
