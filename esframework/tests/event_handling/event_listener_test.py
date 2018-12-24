""" event listener unit test file """
import unittest

from esframework.event_handling.event_listener import EventListener
from esframework.exceptions import EventListenerException


class EventListenerTest(unittest.TestCase):
    """ testing the eventlistener base class """

    def test_it_can_only_deal_with_domain_events(self):
        event_listener = EventListener()

        with self.assertRaises(EventListenerException) as ex:
            event_listener.receive(object())
        self.assertEqual(str(ex.exception), "Incoming event is not a domain event")


