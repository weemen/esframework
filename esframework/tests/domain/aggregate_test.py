""" Imports """
import unittest

from esframework.domain import (AggregateRoot, DomainEvent)


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


class TestAggregateRoot(unittest.TestCase):

    def test_it_can_add_an_unsaved_event_a(self):
        """
        Creates an aggregate and will apply EventA but aggregate
        will not be stored """

        uuid = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        an_event_prop = 'event_a_property'
        aggregate = MyTestAggregate.event_a(uuid, an_event_prop)
        self.assertIsInstance(aggregate, MyTestAggregate)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 1)
        self.assertIsInstance(aggregate.get_uncommitted_events()[0], EventA)

    def test_it_can_clear_uncommitted_events(self):
        """ Creates an aggregate, apply an event and clear the uncommited
        events
        """

        uuid = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        an_event_prop = 'event_a_property'

        aggregate = MyTestAggregate.event_a(uuid, an_event_prop)
        self.assertIsInstance(aggregate, MyTestAggregate)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 1)

        aggregate.clear_uncommitted_events()
        self.assertEqual(len(aggregate.get_uncommitted_events()), 0)

    def test_it_can_restore_state_with_one_event(self):
        """ Creates an aggregate and try to restore state with adding one event
        """

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        events = [EventA(aggregate_root_id, 'my_prop')]
        aggregate = MyTestAggregate()
        aggregate.initialize_state(events)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 0)
        self.assertEqual(aggregate.get_aggregate_root_id(), aggregate_root_id)
        self.assertEqual(
            aggregate.__dict__.get('_MyTestAggregate__an_event_property'),
            'my_prop')

    def test_it_can_restore_state_with_three_events(self):
        """ Creates an aggregate and try to restore state with adding trhee
        events
        """

        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        events = [
            EventA(aggregate_root_id, 'my_prop'),
            EventA(aggregate_root_id, 'my_prop1'),
            EventA(aggregate_root_id, 'my_prop2'),
        ]
        aggregate = MyTestAggregate()
        aggregate.initialize_state(events)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 0)
        self.assertEqual(aggregate.get_aggregate_root_id(), aggregate_root_id)
        self.assertEqual(
            aggregate.__dict__.get('_MyTestAggregate__an_event_property'),
            'my_prop2')
