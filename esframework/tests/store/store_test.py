""" Imports """
import unittest
from pytest import raises
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from esframework.config import ESConfig
from esframework.data_sources.sqlalchemy.models import SqlDomainRecord
from esframework.exceptions import AggregateRootIdNotFoundError
from esframework.store import (InMemoryStore, SQLStore)
from esframework.tests.assets import EventA


class TestInMemoryStore(unittest.TestCase):
    """ Test class for testing the InMemoryStore """

    def test_it_can_store_and_load_an_event(self):
        """ test if InMemoryStore can actually store an event """
        store = InMemoryStore()

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        eventstream = [
            EventA(aggregate_root_id, 'my_prop'),
        ]

        store.save(eventstream, aggregate_root_id)
        self.assertEqual(1, len(store.load(aggregate_root_id)))

    def test_it_can_store_and_load_multiple_events(self):
        """ test if InMemoryStore can store and load multiple events """
        store = InMemoryStore()

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        eventstream = [
            EventA(aggregate_root_id, 'my_prop'),
            EventA(aggregate_root_id, 'my_prop1'),
            EventA(aggregate_root_id, 'my_prop2'),
        ]

        store.save(eventstream, aggregate_root_id)
        self.assertEqual(3, len(store.load(aggregate_root_id)))

    def test_it_can_store_and_load_multiple_events_multiple_aggregates(self):
        """ test if InMemoryStore can deal with multiple aggregates """
        store = InMemoryStore()

        aggr_root_id_1 = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        eventstream = [
            EventA(aggr_root_id_1, 'my_prop'),
            EventA(aggr_root_id_1, 'my_prop1'),
            EventA(aggr_root_id_1, 'my_prop2'),
        ]

        store.save(eventstream, aggr_root_id_1)

        aggr_root_id_2 = '108AEB44-7842-4F36-A113-60A3786670C2'
        eventstream = [
            EventA(aggr_root_id_2, 'my_prop'),
            EventA(aggr_root_id_2, 'my_prop1'),
        ]

        store.save(eventstream, aggr_root_id_2)

        self.assertEqual(3, len(store.load(aggr_root_id_1)))
        self.assertEqual(2, len(store.load(aggr_root_id_2)))

    def test_it_throws_when_id_doesnt_exists(self):
        """ test if InMemoryStore throws AggregateRootIdNotFoundError """
        store = InMemoryStore()

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        eventstream = [
            EventA(aggregate_root_id, 'my_prop'),
            EventA(aggregate_root_id, 'my_prop1'),
            EventA(aggregate_root_id, 'my_prop2'),
        ]
        store.save(eventstream, aggregate_root_id)

        with self.assertRaises(AggregateRootIdNotFoundError) as ex:
            store.load('108AEB44-7842-4F36-A113-60A3786670C2')
        self.assertEqual(
            "Aggregate root id does not exist: 108AEB44-7842-4F36-A113-60A3786670C2",
            str(ex.exception))


class TestSqlStore(unittest.TestCase):
    """ testing the SqlStore """
    def setUp(self):
        es_config = ESConfig()
        es_config.load('./config/esframework.ini')
        engine = create_engine(es_config.get('esframework.storage', 'host'), echo=True)
        self.__session = sessionmaker(bind=engine)()
        model = SqlDomainRecord()
        model.metadata.create_all(engine)

    def test_it_can_store_and_load_an_event(self):
        """ test if InMemoryStore can actually store an event """

        store = SQLStore(self.__session)

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        event_a = EventA(aggregate_root_id, 'my_prop')
        event_a.set_aggregate_root_version(1)
        eventstream = [
            event_a,
        ]

        store.save(eventstream, aggregate_root_id)
        self.assertEqual(1, len(store.load(aggregate_root_id)))

    def test_it_can_store_and_load_multiple_events(self):
        """ test if SQLStore can store and load multiple events """
        store = SQLStore(self.__session)

        aggregate_root_id = '52B6A306-540C-4796-92E4-A10520EA3ED7'
        event1 = EventA(aggregate_root_id, 'my_prop')
        event1.set_aggregate_root_version(1)
        event2 = EventA(aggregate_root_id, 'my_prop1')
        event2.set_aggregate_root_version(2)
        event3 = EventA(aggregate_root_id, 'my_prop2')
        event3.set_aggregate_root_version(3)

        eventstream = [
            event1,
            event2,
            event3
        ]

        store.save(eventstream, aggregate_root_id)
        self.assertEqual(3, len(store.load(aggregate_root_id)))

    def test_it_can_store_and_load_multiple_events_multiple_aggregates(self):
        """ test if SQLStore can deal with multiple aggregates """
        store = SQLStore(self.__session)

        aggr_root_id_1 = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        event1 = EventA(aggr_root_id_1, 'my_prop')
        event1.set_aggregate_root_version(1)
        event2 = EventA(aggr_root_id_1, 'my_prop1')
        event2.set_aggregate_root_version(2)
        event3 = EventA(aggr_root_id_1, 'my_prop2')
        event3.set_aggregate_root_version(3)

        eventstream = [
            event1,
            event2,
            event3
        ]

        store.save(eventstream, aggr_root_id_1)

        aggr_root_id_2 = '108AEB44-7842-4F36-A113-60A3786670C2'
        event4 = EventA(aggr_root_id_2, 'my_prop')
        event4.set_aggregate_root_version(1)
        event5 = EventA(aggr_root_id_2, 'my_prop1')
        event5.set_aggregate_root_version(2)

        eventstream = [
            event4,
            event5
        ]

        store.save(eventstream, aggr_root_id_2)

        self.assertEqual(3, len(store.load(aggr_root_id_1)))
        self.assertEqual(2, len(store.load(aggr_root_id_2)))

    def test_it_throws_when_id_doesnt_exists(self):
        """ test if SQLStore throws AggregateRootIdNotFoundError """
        store = SQLStore(self.__session)

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        event1 = EventA(aggregate_root_id, 'my_prop')
        event1.set_aggregate_root_version(1)

        eventstream = [
            event1
        ]
        store.save(eventstream, aggregate_root_id)

        with self.assertRaises(AggregateRootIdNotFoundError) as ex:
            store.load('108AEB44-7842-4F36-A113-60A3786670C2')

        self.assertEqual(
            "Aggregate root id does not exist: 108AEB44-7842-4F36-A113-60A3786670C2",
            str(ex.exception))

    def test_it_can_set_correct_causation_ids(self):
        """ test if SQLStore can deal properly with causation ids """
        store = SQLStore(self.__session)

        aggr_root = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        event1 = EventA(aggr_root, 'my_prop')
        event1.set_aggregate_root_version(1)
        event2 = EventA(aggr_root, 'my_prop1')
        event2.set_aggregate_root_version(2)
        event3 = EventA(aggr_root, 'my_prop2')
        event3.set_aggregate_root_version(3)

        eventstream = [
            event1,
            event2,
            event3
        ]

        store.save(eventstream, aggr_root)

        # stored_eventstream: List[DomainEvent]
        stored_eventstream = store.load(aggr_root)

        event4 = EventA(aggr_root, 'my_prop')
        event4.set_aggregate_root_version(4)
        event4.set_causation_id(stored_eventstream[1].get_event_id())
        event5 = EventA(aggr_root, 'my_prop1')
        event5.set_aggregate_root_version(5)
        event5.set_causation_id(stored_eventstream[1].get_event_id())

        eventstream = [
            event4,
            event5
        ]

        store.save(eventstream, aggr_root)

        stored_eventstream = store.load(aggr_root)

        self.assertEqual(5, len(stored_eventstream))

        self.assertEqual(
            stored_eventstream[1].get_event_id(),
            stored_eventstream[2].get_causation_id()
        )

        self.assertEqual(
            aggr_root,
            stored_eventstream[2].get_correlation_id()
        )

        self.assertEqual(
            stored_eventstream[1].get_event_id(),
            stored_eventstream[3].get_causation_id()
        )

        self.assertEqual(
            aggr_root,
            stored_eventstream[3].get_correlation_id()
        )

        self.assertEqual(
            stored_eventstream[1].get_event_id(),
            stored_eventstream[4].get_causation_id()
        )

        self.assertEqual(
            aggr_root,
            stored_eventstream[4].get_correlation_id()
        )
