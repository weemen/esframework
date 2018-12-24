""" Event listeners for event busses """
import re
from esframework.domain import DomainEvent
from esframework.exceptions import EventListenerException


class EventListener(object):
    """ A base class for listening to events """

    def receive(self, domain_event: DomainEvent):
        if not isinstance(domain_event, DomainEvent):
            raise EventListenerException("Incoming event is not a domain event")

        method = "apply{0}".format(
            re.sub('([A-Z]+)', r'_\1', domain_event.__class__.__name__).lower()
        )

        if hasattr(self.__class__, method) and callable(getattr(self.__class__, method)):
            self.__getattribute__(method)(domain_event)
