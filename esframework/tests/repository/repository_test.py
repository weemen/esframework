""" imports """
import unittest
from esframework.domain import (AggregateRoot, Event)
from esframework.repository import DefaultRepository
from esframework.store import InMemoryStore


class MyTestAggregate(AggregateRoot):
    """ A test aggregate for unittesting """

    __aggregate_root_id = None
    __an_event_property = ''

    @staticmethod
    def event_a(aggregate_root_id, an_event_property):
        """ Creates MyTestAggregate and will try to apply EventA """
        my_test_aggr = MyTestAggregate()
        my_test_aggr.apply(EventA(aggregate_root_id, an_event_property))

        return my_test_aggr

    def apply_event_a(self, event):
        """ Apply EventA on the aggregate root """
        self.__aggregate_root_id = event.get_aggregate_root_id()
        self.__an_event_property = event.get_an_event_property()

    def get_aggregate_root_id(self):
        """ Get the aggregate root id of this aggregate """
        return self.__aggregate_root_id


class EventA(Event):
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
            'esframework.tests.domain.aggregate_test.MyTestAggregate',
            store,
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
            'esframework.tests.domain.aggregate_test.MyTestAggregate',
            InMemoryStore(),
        )

        repository.save(aggregate_root=aggregate)
        stored = repository._store.__dict__.get('_InMemoryStore__store')

        self.assertIn(aggregate_id, stored)
        self.assertEqual(1, len(stored[aggregate_id]))