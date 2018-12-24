import unittest

from esframework.event_handling.event_bus import BasicBus
from esframework.exceptions import EventBusException
from esframework.tests.assets import EventA
from esframework.tests.assets.event_handling import SimpleEventListener


class TestBasicBus(unittest.TestCase):
    """ testing the basic bus features """

    def test_it_can_subscribe_listeners(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()
        event_bus.subscribe(event_listener)

        self.assertEqual(1, len(event_bus.get_event_listeners()))

    def test_it_can_unsubscribe_listeners(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()
        event_bus.subscribe(event_listener)
        event_bus.unsubscribe(event_listener)
        self.assertEqual(0, len(event_bus.get_event_listeners()))

    def test_it_can_emit_a_stream_of_events(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()
        event_bus.subscribe(event_listener)

        stream_of_events = [
            EventA("792E4DDA-5AE2-4BF3-A834-62D09892DC62", "foo"),
            EventA("EC407041-8454-44E2-873F-951B227B3BFB", "bar")
        ]

        event_bus.emit(stream_of_events)

        self.assertEqual(2, len(event_listener.get_received_messages()))

    def test_it_cannot_subscribe_to_non_event_listeners(self):
        event_bus = BasicBus()
        listener = object()

        with self.assertRaises(EventBusException) as ex:
            event_bus.subscribe(listener)
        self.assertEqual(
            str(ex.exception),
            "Only classes based on EventListener can subscribe")

    def test_it_cannot_unsubscribe_from_non_event_listeners(self):
        event_bus = BasicBus()
        listener = object()

        with self.assertRaises(EventBusException) as ex:
            event_bus.unsubscribe(listener)
        self.assertEqual(
            str(ex.exception),
            "Only classes based on EventListener can unsubscribe")

    def test_it_cannot_unsubscribe_a_non_existing_event_listener(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()

        with self.assertRaises(EventBusException) as ex:
            event_bus.unsubscribe(event_listener)
        self.assertEqual(
            str(ex.exception),
            "Cannot unsubscribe non existing listener from list")

    def test_it_can_only_emit_a_list_as_stream(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()
        event_bus.subscribe(event_listener)

        with self.assertRaises(EventBusException) as ex:
            event_bus.emit(object())
        self.assertEqual(
            str(ex.exception),
            "event stream must be a list")

    def test_it_can_only_emit_a_list_with_domain_events(self):
        event_listener = SimpleEventListener()
        event_bus = BasicBus()
        event_bus.subscribe(event_listener)

        with self.assertRaises(EventBusException) as ex:
            event_bus.emit([
                1
            ])
        self.assertEqual(
            str(ex.exception),
            "domain event must be of type DomainEvent")

