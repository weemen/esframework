import abc


class Repository(object, metaclass=abc.ABCMeta):

    __store = None

    def __init__(self, store):
        self.__store = store

    @abc.abstractmethod
    def load(self, aggregate_root):
        raise NotImplementedError('Every repository must have an load method.')

    @abc.abstractmethod
    def save(self, aggregate_root):
        raise NotImplementedError('Every repository must have an save method.')


class InMemoryRepository(Repository):

    def load(self, aggregate_root):
        pass

    def save(self, aggregate_root):
        pass