""" Exceptions """


class CommandException(Exception):
    pass


class DomainException(Exception):
    """ Domain exception is thrown when event cannot be applied """
    pass
