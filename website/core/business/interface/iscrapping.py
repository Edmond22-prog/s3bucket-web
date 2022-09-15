import abc


class IScrapping(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self):
        ...
