import abc


class IRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def name(self):
        ...

    @abc.abstractmethod
    def owner(self):
        ...

    @abc.abstractmethod
    def url(self):
        ...

    @abc.abstractmethod
    def created_at(self):
        ...

    @abc.abstractmethod
    def updated_at(self):
        ...

    @abc.abstractmethod
    def languages(self):
        ...

    @abc.abstractmethod
    def vulnerabilities(self) -> list:
        ...
