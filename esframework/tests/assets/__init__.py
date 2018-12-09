""" Prepared test asssts """

from esframework.domain import DomainEvent, AggregateRoot


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
