""" Event busses """
import abc
from typing import List

from esframework.domain import DomainEvent
from esframework.event_handling.event_listener import EventListener
from esframework.exceptions import EventBusException


class EventBus(object, metaclass=abc.ABCMeta):
    """ a base class for passing events through busses """

    @abc.abstractmethod
    def subscribe(self, event_listener: EventListener):
        """ subscribe to event stream """
        raise NotImplementedError('Eventbus must be able to subscribe')

    @abc.abstractmethod
    def unsubscribe(self, event_listener: EventListener):
        """ unsubscribe to event stream"""
        raise NotImplementedError('Eventbus must be able to unsubscribe')

    @abc.abstractmethod
    def emit(self, event_stream: List[DomainEvent]):
        """ unsubscribe to event stream"""
        raise NotImplementedError('Eventbus must be able to publish')


class BasicBus(EventBus):
    """ A very simple bus without fancy stuff """

    def __init__(self):
        self.__listeners = []

    def get_event_listeners(self) -> List[EventListener]:
        return self.__listeners

    def subscribe(self, event_listener: EventListener):

        if not isinstance(event_listener, EventListener):
            raise EventBusException("Only classes based on EventListener can subscribe")
        self.__listeners.append(event_listener)

    def unsubscribe(self, event_listener: EventListener):
        if not isinstance(event_listener, EventListener):
            raise EventBusException("Only classes based on EventListener can unsubscribe")
        try:
            self.__listeners.remove(event_listener)
        except ValueError:
            raise EventBusException("Cannot unsubscribe non existing listener from list")

    def emit(self, event_stream: List[DomainEvent]):
        if not isinstance(event_stream, list):
            raise EventBusException("event stream must be a list")

        for domain_event in event_stream:
            if not isinstance(domain_event, DomainEvent):
                raise EventBusException("domain event must be of type DomainEvent")
            for listener in self.__listeners:
                listener.receive(domain_event)

