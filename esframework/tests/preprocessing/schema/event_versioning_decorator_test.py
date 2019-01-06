""" testing the event versioning decorator """
import unittest

from esframework.exceptions import SchemaMapperException
from esframework.preprocessing.schema import event_versioning
from esframework.tests.assets import EventVersioningNone, EventA


class TestProcessWeakSchema(unittest.TestCase):

    # def test_it_can_raise_when_method_not_from_domain_event(self):
    #
    #     class X(object):
    #
    #         @event_versioning(None)
    #         def my_method(self,y):
    #             pass
    #
    #     with self.assertRaises(SchemaMapperException) as ex:
    #         obj = X()
    #         obj.my_method('1')
    #
    #     self.assertEqual(
    #         str(ex.exception),
    #         'TestProcessWeakSchema is not a subclass of DomainEvent')

    # def test_it_can_deserialize_when_event_versioning_is_none(self):
    #     event = EventVersioningNone
    #     self.assertEqual('x', event.deserialize({'aggregate_root_id': 'x'}).get_aggregate_root_id())

    def test_it_can_deserialize_with_an_existing_schema_mapping(self):
        event = EventA
        serialized = {
            'aggregate_root_id': 'x',
            'an_event_property': 'foobar'
        }
        self.assertEqual('x', event.deserialize(serialized).get_aggregate_root_id())
