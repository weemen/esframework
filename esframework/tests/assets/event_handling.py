""" assets needed for event handling """
from typing import List

from esframework.domain import DomainEvent
from esframework.event_handling.event_listener import EventListener


class SimpleEventListener(EventListener):
    """ a super basic event listener for testing purposes """

    def __init__(self):
        self.__received_messages = []

    def get_received_messages(self) -> List[DomainEvent]:
        return self.__received_messages

    def receive(self, domain_event: DomainEvent):
        self.__received_messages.append(domain_event)

