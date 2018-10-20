""" Imports """
import abc

from esframework import import_path
from esframework.domain import AggregateRoot
from esframework.store import Store


class Repository(object, metaclass=abc.ABCMeta):
    """
    Base repository class which should be extended for loading and saving
    from different sources """

    _aggregate_root_class = None
    _store = None

    def __init__(self, aggregate_root_class: str, store: Store):
        self._aggregate_root_class = aggregate_root_class
        self._store = store

    @abc.abstractmethod
    def load(self, aggregate_root_id: str):
        """ Should be implemented by child class for loading from storage """
        raise NotImplementedError('Every repository must have an load method.')

    @abc.abstractmethod
    def save(self, aggregate_root: AggregateRoot):
        """ Should be implemented by child class for saving to storage """
        raise NotImplementedError('Every repository must have an save method.')


class DefaultRepository(Repository):
    """ Default repository """

    def load(self, aggregate_root_id: str) -> AggregateRoot:
        """ Try to find the eventstream from the store and initialize the start
        state of the aggregate root
        """

        aggregate_root_class = import_path(self._aggregate_root_class)
        aggregate_root = aggregate_root_class()
        aggregate_root.initialize_state(self._store.load(aggregate_root_id))
        return aggregate_root

    def save(self, aggregate_root: AggregateRoot):
        """ Get the uncommitted and append it to the eventstream in the store
        """
        uncommitted_events = aggregate_root.get_uncommitted_events()
        self._store.save(uncommitted_events,
                         aggregate_root.get_aggregate_root_id())
        aggregate_root.clear_uncommitted_events()
