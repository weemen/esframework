""" Tooling for testing aggregates """
import unittest
from pytest import raises
from typing import List
from esframework.domain import (AggregateRoot, DomainEvent)
from esframework.exceptions import (
    InvalidMessageException, WrongExceptionRaised)


class AggregateRootTestCase(unittest.TestCase):
    """ Helper class for testing aggregate root logic """
    __eventstream_at_initialisation = []
    __eventstream_to_apply = []

    __aggregate_root = None

    def withAggregate(self, aggregate: AggregateRoot):
        self.__aggregate_root = aggregate
        return self

    def has_eventstream(self, list_of_events: List[DomainEvent]):
        """ has eventstream """
        if self.__aggregate_root is None:
            raise RuntimeError("Aggregate root is not set!")

        self.__eventstream_at_initialisation = list_of_events
        return self

    def then_add_event(self, event: DomainEvent):
        """ Apply DomainEvent on Aggregate """
        self.eventstream_to_apply.append(event)
        return self

    def assert_aggregate_property_state_equal_to(
            self, property: str, value: any):
        """ Asserting if property of aggregate root is equal to value """
        if self.__aggregate_root is None:
            raise RuntimeError("Aggregate root is not set!")

        className = self.__aggregate_root.__class__.__name__
        actualValue = self.__aggregate_root.__dict__.get(
            '_' + className + property)

        self.assertEqual(value, actualValue)

    def expects_exception(
            self, exception: Exception, message: str, method: str, *args):
        """ Asserting when applying events that """

        if self.__aggregate_root is None:
            raise RuntimeError("Aggregate root is not set!")

        try:
            with raises(exception) as excinfo:
                getattr(self.__aggregate_root, method)(*args)
        except Exception:
            raise WrongExceptionRaised(
                "'{0}' expected but got '{1}' ".format(
                    excinfo.typename, exception.__name__))

        try:
            assert message in str(excinfo.value)
        except AssertionError:
            raise InvalidMessageException(
                "'{0}' expected but got '{1}' ".format(
                    message, str(excinfo.value)))
        return self

    def assert_aggregate_event_count(self, number_of_events: int):
        """ Asserting that aggregate root has now number of events in total """

        if self.__aggregate_root is None:
            raise RuntimeError("Aggregate root is not set!")

        return self

    def assert_aggregate_root_eventstream_equal_to(
            self, eventstream: List[DomainEvent]):
        """ asserting that eventstream of aggregate root is equal to the
        eventstream given """

        if self.__aggregate_root is None:
            raise RuntimeError("Aggregate root is not set!")

        return self
