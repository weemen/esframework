""" Imports """
import abc

from esframework import import_path
from esframework.domain import AggregateRoot
from esframework.event_handling.event_bus import EventBus
from esframework.exceptions import AggregateRootIdNotFoundError, AggregateRootOutOfSyncError, RepositoryException
from esframework.store import Store


class Repository(object, metaclass=abc.ABCMeta):
    """
    Base repository class which should be extended for loading and saving
    from different sources """

    _aggregate_root_class = None
    _store = None
    _eventbus = None

    def __init__(self, aggregate_root_class: str, store: Store, eventbus: EventBus):
        if not isinstance(store, Store):
            raise RepositoryException("Store parameter is not type Store!")

        if not isinstance(eventbus, EventBus):
            raise RepositoryException("Eventbus parameter is not of type EventBus!")

        self._aggregate_root_class = aggregate_root_class
        self._store = store
        self._eventbus = eventbus

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

        try:
            aggr_from_store = self.load(aggregate_root.get_aggregate_root_id())
            if not self.is_outdated(
                    aggr_from_store.get_version(),
                    uncommitted_events[0].get_version()):
                self._store.save(uncommitted_events,
                                 aggregate_root.get_aggregate_root_id())
                self._eventbus.emit(uncommitted_events)
            else:
                raise AggregateRootOutOfSyncError(
                    "Aggregate root in store is newer then current aggregate")
        except AggregateRootIdNotFoundError:
            """ no risk of conflicts here """
            self._store.save(uncommitted_events,
                             aggregate_root.get_aggregate_root_id())
        finally:
            aggregate_root.clear_uncommitted_events()

    def is_outdated(self, version_from_store: int, current_version: int) -> bool:
        """ if the first uncommitted event -1 is not equal to the version in the
         store then the aggregate is out of sync """
        return (current_version - 1) != version_from_store
