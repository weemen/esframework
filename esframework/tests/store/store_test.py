""" Imports """
import unittest
from pytest import raises

from esframework.domain import DomainEvent
from esframework.exceptions import AggregateRootIdNotFoundError
from esframework.store import InMemoryStore


class EventA(DomainEvent):
    """ Dummy EventA class for testing """

    def __init__(self, aggregate_root_id, an_event_property):
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_an_event_property(self):
        """ Gets an_event_property of this event """
        return self.__an_event_property

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'an_event_property': self.__an_event_property,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(
            event_data['aggregate_root_id'],
            event_data['an_event_property'])


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

        with raises(AggregateRootIdNotFoundError,
                    message="Aggregate root id does not exist"):
            store.load('108AEB44-7842-4F36-A113-60A3786670C2')
