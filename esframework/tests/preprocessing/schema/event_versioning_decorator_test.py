""" testing the event versioning decorator """
import unittest

from esframework.tests.assets import EventA


class TestProcessWeakSchema(unittest.TestCase):

    def test_it_can_deserialize_with_an_existing_schema_mapping(self):
        event = EventA
        serialized = {
            'aggregate_root_id': 'x',
            'an_event_property': 'foobar'
        }
        self.assertEqual('x', event.deserialize(serialized).get_aggregate_root_id())
