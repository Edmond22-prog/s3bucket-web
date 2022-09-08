import abc
from typing import List

from uuid import UUID

from core.business.interface.ibucket import IBucket


class IBucketRepository(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find(self, uuid: UUID) -> IBucket:
        ...

    @abc.abstractmethod
    def find_by_name(self, name: str) -> IBucket:
        ...

    @abc.abstractmethod
    def create(self, bucket: IBucket) -> None:
        ...

    @abc.abstractmethod
    def list(self) -> List[IBucket]:
        ...

    @abc.abstractmethod
    def delete(self, uuid: UUID) -> None:
        ...

    @abc.abstractmethod
    def update(self, name: UUID) -> None:
        ...
