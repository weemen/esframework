import unittest

from esframework.domain import (AggregateRoot, Event)


class EventA(Event):

    def __init__(self, aggregate_root_id, an_event_property):
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id

    def get_an_event_property(self):
        return self.__an_event_property

    def serialize(self):
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'an_event_property': self.__an_event_property,
        }

    @staticmethod
    def deserialize(event_data):
        return EventA(
            event_data['aggregate_root_id'],
            event_data['an_event_property'])


class MyTestAggregate(AggregateRoot):

    __aggregate_root_id = None
    __an_event_property = ''

    @staticmethod
    def event_a(aggregate_root_id, an_event_property):
        my_test_aggr = MyTestAggregate()
        my_test_aggr.apply(EventA(aggregate_root_id, an_event_property))

        return my_test_aggr

    def apply_event_a(self, event):
        self.__aggregate_root_id = event.get_aggregate_root_id()
        self.__an_event_property = event.get_an_event_property()

    def get_aggregate_root_id(self):
        return self.__aggregate_root_id


class TestAggregateRoot(unittest.TestCase):

    def test_it_can_add_an_unsaved_event_a(self):
        uuid = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        an_event_prop = 'event_a_property'
        aggregate = MyTestAggregate.event_a(uuid, an_event_prop)
        self.assertIsInstance(aggregate, MyTestAggregate)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 1)
        self.assertIsInstance(aggregate.get_uncommitted_events()[0], EventA)

    def test_it_can_clear_uncommitted_events(self):
        uuid = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        an_event_prop = 'event_a_property'

        aggregate = MyTestAggregate.event_a(uuid, an_event_prop)
        self.assertIsInstance(aggregate, MyTestAggregate)
        self.assertEqual(len(aggregate.get_uncommitted_events()), 1)

        aggregate.clear_uncommitted_events()
        self.assertEqual(len(aggregate.get_uncommitted_events()), 0)

    def test_it_can_restore_state_with_one_event(self):
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
