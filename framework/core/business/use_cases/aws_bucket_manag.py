from dataclasses import dataclass
from typing import List
from uuid import UUID

from core.business.interface.ibucket import IBucket
from core.business.interface.ibucket_use_case import IBucketUseCase
from infrastructure.repository.aws_bucket_repos import AwsBucketRepository


@dataclass
class AwsBucketManagement(IBucketUseCase):
    _aws_bucket_repo: AwsBucketRepository

    def find_bucket(self, uuid: UUID) -> IBucket:
        return self._aws_bucket_repo.find(uuid)

    def find_bucket_by_name(self, name: str) -> IBucket:
        return self._aws_bucket_repo.find_by_name(name)

    def create_bucket(self, bucket: IBucket) -> None:
        self._aws_bucket_repo.create(bucket)

    def list_buckets(self) -> List[IBucket]:
        return self._aws_bucket_repo.list()

    def delete_bucket(self, uuid: UUID) -> None:
        self._aws_bucket_repo.delete(uuid)

    def update_bucket(self, bucket: IBucket) -> None:
        self._aws_bucket_repo.update(bucket)
