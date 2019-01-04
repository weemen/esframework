""" processing with weak schema tests """
import unittest

from esframework.preprocessing.schema import WeakSchemaMapper
from esframework.tests.assets import EventA, EventAV2, EventAV3, EventAV4, EventAV5


class TestProcessWeakSchema(unittest.TestCase):

    def test_it_can_map_to_current_schema(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
        }

        output = processor.map(serialized_data, EventA.__dict__)
        self.assertDictEqual(serialized_data, output)

    def test_it_can_map_newer_messages_to_current_schema(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property_v2': 'foobar'
        }

        output = processor.map(serialized_data, EventA.__dict__)
        self.assertDictEqual(serialized_data, output)

    def test_it_can_map_old_messages_to_newer_schema(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value'
        }

        output = processor.map(serialized_data, EventAV2.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_old_messages_to_newer_schema_with_dicts(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one'
            }
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            }
        }

        output = processor.map(serialized_data, EventAV3.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_newer_messages_to_old_schema_with_dicts(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            }
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            }
        }

        output = processor.map(serialized_data, EventAV2.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_old_messages_to_newer_schema_with_dicts_in_dicts(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two',
                'some_key_three': {
                    "sub_key_one": {
                        "sub_sub_key_one": "existing string 1",
                    }
                }
            }
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two',
                'some_key_three': {
                    "sub_key_one": {
                        "sub_sub_key_one": "existing string 1",
                        "sub_sub_key_two": "some string two"
                    },
                    "sub_key_two": {
                        "sub_sub_key_one": "default string one",
                        "sub_sub_key_two": "default string two"
                    }
                }
            }
        }

        output = processor.map(serialized_data, EventAV4.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_newer_messages_to_old_schema_with_dicts_in_dicts(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two',
                'some_key_three': {
                    "sub_key_one": {
                        "sub_sub_key_one": "existing string 1",
                        "sub_sub_key_two": "some string two"
                    },
                    "sub_key_two": {
                        "sub_sub_key_one": "default string one",
                        "sub_sub_key_two": "default string two"
                    }
                }
            }
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two',
                'some_key_three': {
                    "sub_key_one": {
                        "sub_sub_key_one": "existing string 1",
                        "sub_sub_key_two": "some string two"
                    },
                    "sub_key_two": {
                        "sub_sub_key_one": "default string one",
                        "sub_sub_key_two": "default string two"
                    }
                }
            }
        }

        output = processor.map(serialized_data, EventAV3.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_old_messages_to_newer_schema_with_lists(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one'
            },
            'new_list_prop': [
                'item-1'
            ]
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            },
            'new_list_prop': [
                'item-1',
                'item-2'
            ]
        }

        output = processor.map(serialized_data, EventAV5.__dict__)
        self.assertDictEqual(expected_output_data, output)

    def test_it_can_map_new_messages_to_old_schema_with_lists(self):
        processor = WeakSchemaMapper()
        serialized_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            },
            'new_list_prop': [
                'item-1',
                'item-2'
            ]
        }

        expected_output_data = {
            'aggregate_root_id': '61C99C6A-D7E8-4C2F-8290-97B3CFB360B6',
            'an_event_property': 'foo',
            'new_property': 'My default value',
            'new_dict_prop': {
                'some_key_one': 'dict_value_one',
                'some_key_two': 'dict_value_two'
            },
            'new_list_prop': [
                'item-1',
                'item-2'
            ]
        }

        output = processor.map(serialized_data, EventAV3.__dict__)
        self.assertDictEqual(expected_output_data, output)
