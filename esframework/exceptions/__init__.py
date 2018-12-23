""" Exceptions """


class AggregateRootIdNotFoundError(Exception):
    """ Exception Class when the aggregate root cannot loaded from the store """
    pass


class AggregateRootOutOfSyncError(Exception):
    """ Exception Class when the aggregate in the store is newer then the
    loaded aggregate """
    pass


class DomainEventException(Exception):
    """ Exception for illegal actions within Domain events"""
    pass


class WrongExceptionRaised(Exception):
    """ An exception was expected but not the given one """
    pass


class InvalidMessageException(Exception):
    """ An exception was expected but not the given one """
    pass


class EncryptionCodecError(Exception):
    """ An exception class when encryption and decryption errors """
    pass


class EventBusException(Exception):
    """ An exception class when errors occur in eventbusses """
    pass
