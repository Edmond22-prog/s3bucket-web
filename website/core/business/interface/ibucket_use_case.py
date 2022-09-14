import abc
from typing import List
from uuid import UUID

from website.core.business.interface.ibucket import IBucket


class IBucketUseCase(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def find_bucket(self, uuid: UUID) -> IBucket:
        ...

    @abc.abstractmethod
    def find_bucket_by_name(self, name: str) -> IBucket:
        ...

    @abc.abstractmethod
    def create_bucket(self, bucket: IBucket) -> None:
        ...

    @abc.abstractmethod
    def list_buckets(self) -> List[IBucket]:
        ...

    @abc.abstractmethod
    def delete_bucket(self, uuid: UUID) -> None:
        ...

    @abc.abstractmethod
    def update_bucket(self, bucket: IBucket) -> None:
        ...
