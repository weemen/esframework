""" init.py """
import unittest
from pytest import raises
from esframework.domain import (AggregateRoot, Event)
from esframework.exceptions import (WrongExceptionRaised,
                                    InvalidMessageException)
from esframework.tooling.aggregate import AggregateRootTestCase


class EventA(Event):
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

    def event_b(self, param_one, param_two):
        """ deliberately raise an RuntimeError here"""
        raise RuntimeError('done on purpose')

    def get_aggregate_root_id(self):
        """ Get the aggregate root id of this aggregate """
        return self.__aggregate_root_id


class AggregateRootTestCaseTest(unittest.TestCase):
    """ test the AggregateRootTestCase """

    def test_it_can_set_an_aggregate_root(self):
        """ test if withAggregateRoot method actually sets the aggregate """
        aggregate_root = MyTestAggregate()
        testcase = AggregateRootTestCase()
        testcase.withAggregate(aggregate_root)
        self.assertEqual(
            testcase.__dict__.get('_AggregateRootTestCase__aggregate_root'),
            aggregate_root)

    def test_it_can_set_an_eventstream(self):
        """ test if the aggregate root can be set at a default state """
        eventstream = [
            EventA(aggregate_root_id='D60A2BD0-AE8D-4FF1-A5AE-B4F706356389',
                   an_event_property='a')
        ]
        testcase = AggregateRootTestCase()
        testcase.withAggregate(MyTestAggregate())
        testcase.has_eventstream(eventstream)

        self.assertEqual(
            testcase.__dict__.get(
                '_AggregateRootTestCase__eventstream_at_initialisation'),
            eventstream)

    def test_it_cant_set_eventstream_if_aggregate_is_not_set(self):
        """ test that eventstream can be set if aggregate root exists """
        testcase = AggregateRootTestCase()
        with raises(RuntimeError) as excinfo :
            testcase.has_eventstream([])
        assert 'Aggregate root is not set!' in str(excinfo.value)

    def test_it_can_assert_aggregate_root_properties_with_correct_assertion(
            self):
        """ test if aggregate root properties can be tested (valid comparison)
        """
        aggregate_root = MyTestAggregate().event_a(
            aggregate_root_id='F91E36AC-597B-43FC-BA44-5F045D2C9C47',
            an_event_property='myValue'
        )

        testcase = AggregateRootTestCase()
        testcase.withAggregate(aggregate_root)
        self.assertEqual(
            testcase.assert_aggregate_property_state_equal_to(
                '__an_event_property', 'myValue'),
            None)

    def test_it_can_assert_aggregate_root_properties_with_incorrect_assertion(
            self):
        """ test if aggregate root properties can be tested (invalid comparison)
        """
        aggregate_root = MyTestAggregate().event_a(
            aggregate_root_id='F91E36AC-597B-43FC-BA44-5F045D2C9C47',
            an_event_property='myValue'
        )

        testcase = AggregateRootTestCase()
        testcase.withAggregate(aggregate_root)

        with raises(AssertionError) as excinfo:
            self.assertEqual(
                testcase.assert_aggregate_property_state_equal_to(
                    '__an_event_property', 'incorrect_value'),
                None)
        msg = "'myValue' != 'incorrect_value'\n- myValue\n+ incorrect_value\n"
        assert msg in str(excinfo.value)

    def test_it_cant_assert_aggregate_properties_if_aggregate_is_not_set(self):
        """ validate that aggregate root properties can only be tested with
        when an aggregate root is set """
        testcase = AggregateRootTestCase()
        with raises(RuntimeError) as excinfo:
            testcase.assert_aggregate_property_state_equal_to(
                '__an_event_property', 'incorrect_value')
        assert 'Aggregate root is not set!' in str(excinfo.value)

    def test_it_can_assert_that_aggregate_root_throws_exception(self):
        """ validate assertion that exceptions are caught when the
        aggregate root should throw an exception when applying an event """
        aggregate_root = MyTestAggregate().event_a(
            aggregate_root_id='F91E36AC-597B-43FC-BA44-5F045D2C9C47',
            an_event_property='myValue'
        )
        testcase = AggregateRootTestCase()
        testcase.withAggregate(aggregate_root)\
            .expects_exception(
            RuntimeError, 'done on purpose', 'event_b', 'myVal1', 'myVal2')

    def test_it_can_throw_WrongExceptionRaised(self):
        """ WrongException is raised when expected exception does not match
        the actual exception """
        aggregate_root = MyTestAggregate().event_a(
            aggregate_root_id='F91E36AC-597B-43FC-BA44-5F045D2C9C47',
            an_event_property='myValue'
        )
        testcase = AggregateRootTestCase()

        with raises(WrongExceptionRaised):
            testcase.withAggregate(aggregate_root).expects_exception(
                AttributeError, 'done on purpose', 'event_b', 'myVal1',
                'myVal2')

    def test_it_can_throw_InvalidMessageException(self):
        """ WrongException is raised when expected exception does not match
        the actual exception """
        aggregate_root = MyTestAggregate().event_a(
            aggregate_root_id='F91E36AC-597B-43FC-BA44-5F045D2C9C47',
            an_event_property='myValue'
        )
        testcase = AggregateRootTestCase()

        with raises(InvalidMessageException):
            testcase.withAggregate(aggregate_root).expects_exception(
                RuntimeError, 'wrong message', 'event_b', 'myVal1', 'myVal2')

    def test_it_cant_assert_exception_if_aggregate_root_is_not_set(self):
        """ validate that aggregate root is there when asserting for
        exceptions """
        testcase = AggregateRootTestCase()
        with raises(RuntimeError) as excinfo :
            testcase.expects_exception(
                RuntimeError, 'done on purpose', 'event_b')
        assert 'Aggregate root is not set!' in str(excinfo.value)
