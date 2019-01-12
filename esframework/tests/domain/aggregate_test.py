""" Imports """
import unittest

from esframework.tests.assets import EventA, MyTestAggregate


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

    def test_it_has_a_loaded_version(self):
        """ test if events are versioned when aggregate is loaded """
        aggregate_root_id = '897878D0-1230-408B-A980-7A9C24EBDEFA'
        events = [
            EventA(aggregate_root_id, 'my_prop'),
            EventA(aggregate_root_id, 'my_prop1'),
            EventA(aggregate_root_id, 'my_prop2'),
        ]
        aggregate = MyTestAggregate()
        aggregate.initialize_state(events)
        self.assertEqual(aggregate.get_aggregate_root_version(), 3)

    def test_it_can_version_uncommitted_events(self):
        """ test if newly added events are versioned """
        uuid = 'AB9850E7-B590-4A65-B513-91ABD6DC6F40'
        an_event_prop = 'event_a_property'

        aggregate = MyTestAggregate.event_a(uuid, an_event_prop)
        self.assertEqual(aggregate.get_aggregate_root_version(), 0)

        uncommitted_events = aggregate.get_uncommitted_events()
        self.assertEqual(uncommitted_events[0].get_aggregate_root_version(), 1)
