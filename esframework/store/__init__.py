""" Imports """
import abc
import datetime
import uuid
from typing import List

from esframework import (get_fully_qualified_path_name, import_path)
from esframework.data_sources.sqlalchemy.models import SqlDomainRecord
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


class SQLStore(Store):
    """ A store for storing in SQL databases """

    def __init__(self, session):
        self.__session = session

    def load(self, aggregate_root_id: str) -> List[DomainEvent]:

        records = self.__session.query(SqlDomainRecord)\
            .filter_by(aggregate_root_id=aggregate_root_id).all()

        if not records:
            """ Read event stream from relational database """
            raise AggregateRootIdNotFoundError(
                'Aggregate root id does not exist',
                aggregate_root_id)

        return self.convert_to_domain_events(records)

    def save(self, event_stream: List[DomainEvent], aggregate_root_id: str):

        causation_id = None
        for domain_event in event_stream:

            domain_event_id = str(uuid.uuid4())
            if domain_event.get_causation_id() is None and causation_id is None:
                domain_event.set_causation_id(domain_event_id)
            elif domain_event.get_causation_id() is None:
                domain_event.set_causation_id(causation_id)

            event = SqlDomainRecord(
                domain_event_id=domain_event_id,
                aggregate_root_id=aggregate_root_id,
                version=domain_event.get_version(),
                domain_event_name=get_fully_qualified_path_name(domain_event),
                domain_event_body=domain_event.serialize(),
                store_date=datetime.datetime.now().isoformat(),
                event_date=domain_event.get_event_date(),
                correlation_id=aggregate_root_id,
                causation_id=domain_event.get_causation_id(),
                event_metadata={}
            )

            self.__session.add(event)
            self.__session.commit()
            causation_id = domain_event_id

    def convert_to_domain_events(self, records: List[SqlDomainRecord]) -> List[DomainEvent]:
        domain_events = []  # domain_events: List[DomainEvent]

        for record in records:
            event_class = import_path(record.domain_event_name)
            event = event_class.deserialize(record.domain_event_body)
            event.set_event_id(record.domain_event_id)
            event.set_causation_id(record.causation_id)
            event.set_version(record.version)
            event.set_correlation_id(record.correlation_id)
            domain_events.append(event)

        return domain_events
