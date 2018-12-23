""" Event listeners for event busses """
import abc
from esframework.domain import DomainEvent


class EventListener(object, metaclass=abc.ABCMeta):
    """ A base class for listening to events """

    @abc.abstractmethod
    def receive(self, domain_event: DomainEvent):
        raise NotImplementedError("Eventlistener must have receive method")

