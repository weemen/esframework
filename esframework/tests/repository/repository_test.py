""" imports """
import unittest
from pytest import raises

from esframework.event_handling.event_bus import BasicBus
from esframework.exceptions import AggregateRootOutOfSyncError, RepositoryException
from esframework.repository import DefaultRepository
from esframework.store import InMemoryStore
from esframework.tests.assets import EventA, MyTestAggregate


class DefaultRepositoryTest(unittest.TestCase):

    def test_it_can_load_an_eventstream(self):
        aggregate_id = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        eventStream = [
            EventA(aggregate_root_id=aggregate_id, an_event_property='prop1'),
            EventA(aggregate_root_id=aggregate_id, an_event_property='prop2'),
            EventA(aggregate_root_id=aggregate_id, an_event_property='prop3')
        ]
        store = InMemoryStore()
        store.save(eventStream, aggregate_id)

        repository = DefaultRepository(
            'esframework.tests.repository.repository_test.MyTestAggregate',
            store,
            BasicBus()
        )

        aggregate = repository.load(aggregate_root_id=aggregate_id)
        self.assertEqual(aggregate.get_aggregate_root_id(), aggregate_id)
        self.assertEqual(
            aggregate.__dict__.get('_MyTestAggregate__an_event_property'),
            'prop3')

    def test_it_can_save_an_eventstream(self):
        aggregate_id = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        aggregate = MyTestAggregate.event_a(
            aggregate_root_id=aggregate_id, an_event_property='prop1')

        repository = DefaultRepository(
            'esframework.tests.repository.repository_test.MyTestAggregate',
            InMemoryStore(),
            BasicBus()
        )

        repository.save(aggregate_root=aggregate)
        stored = repository._store.__dict__.get('_InMemoryStore__store')

        self.assertIn(aggregate_id, stored)
        self.assertEqual(1, len(stored[aggregate_id]))

    def test_it_can_detect_outdated_aggregates(self):
        aggregate_id = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        eventStream = [
            EventA(aggregate_root_id=aggregate_id, an_event_property='prop1'),
        ]
        store = InMemoryStore()
        store.save(eventStream, aggregate_id)

        repository = DefaultRepository(
            'esframework.tests.repository.repository_test.MyTestAggregate',
            store,
            BasicBus()
        )

        aggregate_one = repository.load(aggregate_root_id=aggregate_id)
        aggregate_two = repository.load(aggregate_root_id=aggregate_id)

        aggregate_one.event_b(aggregate_id, 'my_prop_value')
        repository.save(aggregate_one)

        with self.assertRaises(AggregateRootOutOfSyncError) as ex:
            aggregate_two.event_b(aggregate_id, 'my_prop_value')
            repository.save(aggregate_two)
        self.assertEqual(str(ex.exception), "Aggregate root in store is newer then current aggregate")

    def test_it_cannot_accept_an_invalid_created_store(self):
        with self.assertRaises(RepositoryException) as ex:
            DefaultRepository(
                'esframework.tests.repository.repository_test.MyTestAggregate',
                object(),
                BasicBus()
            )
        self.assertEqual(str(ex.exception), "Store parameter is not type Store!")

    def test_it_cannot_accept_an_invalid_created_eventbus(self):
        with self.assertRaises(RepositoryException) as ex:
            DefaultRepository(
                'esframework.tests.repository.repository_test.MyTestAggregate',
                InMemoryStore(),
                object()
            )
        self.assertEqual(str(ex.exception), "Eventbus parameter is not of type EventBus!")
