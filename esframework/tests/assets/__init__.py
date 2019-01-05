""" Prepared test assets """

from esframework.domain import DomainEvent, AggregateRoot
from esframework.preprocessing.schema import event_versioning


class EventA(DomainEvent):
    """ Dummy EventA class for testing """
    __aggregate_root_id = None
    __an_event_property = None

    def __init__(self, aggregate_root_id, an_event_property):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_an_event_property(self):
        """ Gets an_event_property of this event """
        return self.__an_event_property

    @staticmethod
    @event_versioning('weak-schema')
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(
            event_data['aggregate_root_id'],
            event_data['an_event_property'])

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'an_event_property': self.__an_event_property,
        }


class EventB(DomainEvent):
    """ Dummy EventB class for testing """

    def __init__(self, aggregate_root_id, an_event_property):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__my_prop = an_event_property

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    def get_my_prop(self):
        """ Gets an_event_property of this event """
        return self.__my_prop

    def serialize(self):
        """ Serialize the event for storing """
        return {
            'aggregate_root_id': self.__aggregate_root_id,
            'my_prop': self.__my_prop,
        }

    @staticmethod
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventA(
            event_data['aggregate_root_id'],
            event_data['my_prop'])


class EventAV2(DomainEvent):
    """ Dummy EventA version 2 class for testing """
    __aggregate_root_id = None
    __an_event_property = None
    __new_property = 'My default value'

    def __init__(self, aggregate_root_id, an_event_property, new_property):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property
        self.__new_property = new_property

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


class EventAV3(DomainEvent):
    """ Dummy EventA version 2 class for testing """
    __aggregate_root_id = None
    __an_event_property = None
    __new_property = 'My default value'
    __new_dict_prop = {
        'some_key_one': 'dict_value_one',
        'some_key_two': 'dict_value_two'
    }

    def __init__(self, aggregate_root_id, an_event_property, new_property, new_dict_prop):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property
        self.__new_property = new_property
        self.__new_dict_prop = new_dict_prop

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


class EventAV4(DomainEvent):
    """ Dummy EventA version 2 class for testing """
    __aggregate_root_id = None
    __an_event_property = None
    __new_property = 'My default value'
    __new_dict_prop = {
        'some_key_one': 'dict_value_one',
        'some_key_two': 'dict_value_two',
        'some_key_three': {
            "sub_key_one": {
                "sub_sub_key_one": "some string one",
                "sub_sub_key_two": "some string two"
            },
            "sub_key_two": {
                "sub_sub_key_one": "default string one",
                "sub_sub_key_two": "default string two"
            }
        }
    }

    def __init__(self, aggregate_root_id, an_event_property, new_property, new_dict_prop):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property
        self.__new_property = new_property
        self.__new_dict_prop = new_dict_prop

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


class EventAV5(DomainEvent):
    """ Dummy EventA version 2 class for testing """
    __aggregate_root_id = None
    __an_event_property = None
    __new_property = 'My default value'
    __new_dict_prop = {
        'some_key_one': 'dict_value_one',
        'some_key_two': 'dict_value_two'
    }
    __new_list_prop = [
        'item-1',
        'item-2'
    ]

    def __init__(self, aggregate_root_id, an_event_property, new_property, new_dict_prop, new_list_prop):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id
        self.__an_event_property = an_event_property
        self.__new_property = new_property
        self.__new_dict_prop = new_dict_prop
        self.__new_list_prop = new_list_prop

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


class EventVersioningNone(DomainEvent):
    """ Dummy EventA class for testing """
    __aggregate_root_id = None

    def __init__(self, aggregate_root_id):
        super().__init__()
        self.__aggregate_root_id = aggregate_root_id

    def get_aggregate_root_id(self):
        """ returns the property aggregate_root_id of this event """
        return self.__aggregate_root_id

    @staticmethod
    @event_versioning(None)
    def deserialize(event_data):
        """ deserialize the event for building the aggregate root """
        return EventVersioningNone(event_data['aggregate_root_id'])

    def serialize(self):
        """ Serialize the event for storing """
        return {'aggregate_root_id': self.__aggregate_root_id}


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

    def event_b(self, aggregate_root_id, my_prop):
        """ apply event b"""
        self.apply(EventB(aggregate_root_id, my_prop))

    def apply_event_b(self, event: EventB):
        """ apply event b"""
        self.__an_event_property = event.get_my_prop()

    def event_c(self, param_one, param_two):
        """ deliberately raise an RuntimeError here"""
        raise RuntimeError('done on purpose')

    def get_aggregate_root_id(self):
        """ Get the aggregate root id of this aggregate """
        return self.__aggregate_root_id
