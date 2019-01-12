""" schema mapper factory tests """
import unittest

from esframework.exceptions import SchemaMapperException
from esframework.preprocessing.schema import SchemaMapperFactory, WeakSchemaMapper


class TestProcessWeakSchema(unittest.TestCase):

    def test_it_can_return_weak_schema_mapper(self):
        mapper = SchemaMapperFactory.factory('weak-schema')
        self.assertIsInstance(mapper, WeakSchemaMapper)

    def test_it_can_raise_when_no_mapper_found(self):
        with self.assertRaises(SchemaMapperException) as ex:
            SchemaMapperFactory.factory('strong-schema')
        self.assertEqual(str(ex.exception),'Versioning type does not exist')
