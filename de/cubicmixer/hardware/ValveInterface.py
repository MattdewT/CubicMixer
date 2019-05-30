import abc


class ValveInterface:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def open(self):
        raise NotImplementedError

    @abc.abstractmethod
    def get_position(self):
        raise NotImplementedError
