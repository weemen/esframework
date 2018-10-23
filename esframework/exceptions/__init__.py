""" Exceptions """


class AggregateRootIdNotFoundError(Exception):
    """ Exception Class when the aggregate root cannot loaded from the store """
    pass


class WrongExceptionRaised(Exception):
    """ An exception was expected but not the given one """
    pass


class InvalidMessageException(Exception):
    """ An exception was expected but not the given one """
    pass
