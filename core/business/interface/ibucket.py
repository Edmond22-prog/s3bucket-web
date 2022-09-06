import abc
from typing import Optional
from uuid import UUID


class IBucket(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def uuid(self) -> UUID:
        ...

    @abc.abstractmethod
    def name(self) -> str:
        ...

    @abc.abstractmethod
    def url(self) -> str:
        ...

    @abc.abstractmethod
    def location(self) -> str:
        ...

    @abc.abstractmethod
    def properties(self) -> dict:
        ...

    # @classmethod
    # def factory(
    #         cls,
    #         name: str,
    #         url: str,
    #         location: str,
    #         properties: dict,
    #         uuid: Optional[UUID] = None
    # ) -> "IBucket":
    #     ...