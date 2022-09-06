from typing import List
from uuid import UUID

from core.business.entities import AwsBucketEntity
from core.business.interface.iaws_bucket import IAwsBucket
from core.business.interface.iaws_bucket_repos import IAwsBucketRepository
from infrastructure.framework.website.models import AwsBucket


class AwsBucketRepository(IAwsBucketRepository):
    def __init__(self, model: AwsBucket):
        self._model = model

    def find(self, uuid: UUID) -> IAwsBucket:
        instance = self._model.objects.get(uuid=uuid)
        return self._factory_bucket_entity(instance)

    def find_by_name(self, name: str) -> IAwsBucket:
        instance = self._model.objects.get(name=name)
        return self._factory_bucket_entity(instance)

    def create(self, bucket: IAwsBucket) -> None:
        self._model.objects.create(
            name=bucket.name,
            uuid=bucket.uuid,
            region=bucket.location,
            url=bucket.url,
            access_browser=bucket.access_browser,
        )

    def list(self) -> List[IAwsBucket]:
        instances = self._model.objects.all()
        return [self._factory_bucket_entity(instance) for instance in instances]

    def delete(self, uuid: UUID) -> None:
        self._model.objects.get(uuid=uuid).delete()

    @staticmethod
    def _factory_bucket_entity(instance: AwsBucket) -> IAwsBucket:
        return AwsBucketEntity.factory(
            name=instance.name,
            access_browser=instance.access_browser,
            url=instance.url,
            location=instance.region,
            uuid=instance.uuid,
        )
