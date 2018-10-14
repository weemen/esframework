import abc


class Repository(object, metaclass=abc.ABCMeta):
    """
    Base repository class which should be extended for loading and saving
    from different sources """

    __store = None

    def __init__(self, store):
        self.__store = store

    @abc.abstractmethod
    def load(self, aggregate_root):
        """ Should be implemented by child class for loading from storage """
        raise NotImplementedError('Every repository must have an load method.')

    @abc.abstractmethod
    def save(self, aggregate_root):
        """ Should be implemented by child class for saving to storage """
        raise NotImplementedError('Every repository must have an save method.')


class InMemoryRepository(Repository):
    """ An in Memory repository """

    def load(self, aggregate_root):
        pass

    def save(self, aggregate_root):
        pass
