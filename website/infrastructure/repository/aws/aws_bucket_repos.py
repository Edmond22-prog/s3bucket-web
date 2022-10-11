# from typing import List
# from uuid import UUID
#
# from website.core.business.entities import AwsBucketEntity
# from website.core.business.interface.ibucket_repos import IBucketRepository
# from website.core.business.interface.ibucket import IBucket
# from website.models import AwsBucket
#
#
# class AwsBucketRepository(IBucketRepository):
#     def __init__(self, model: AwsBucket):
#         self._model = model
#
#     def find(self, uuid: UUID) -> IBucket:
#         instance = self._model.objects.get(uuid=uuid)
#         return self._factory_bucket_entity(instance)
#
#     def find_by_name(self, name: str) -> IBucket:
#         instance = self._model.objects.get(name=name)
#         return self._factory_bucket_entity(instance)
#
#     def create(self, bucket: IBucket) -> None:
#         self._model.objects.create(
#             name=bucket.name,
#             uuid=bucket.uuid,
#             region=bucket.location,
#             url=bucket.url,
#             access_browser=bucket.access_browser,
#             # properties=bucket.properties,
#         )
#
#     def list(self) -> List[IBucket]:
#         instances = self._model.objects.all()
#         return [self._factory_bucket_entity(instance) for instance in instances]
#
#     def delete(self, uuid: UUID) -> None:
#         self._model.objects.get(uuid=uuid).delete()
#
#     def update(self, bucket: IBucket) -> None:
#         obj = self._model.objects.get(name=bucket.name())
#         obj.access_browser = bucket.access_browser()
#         # obj.properties = bucket.properties()
#         obj.save()
#
#     @staticmethod
#     def _factory_bucket_entity(instance: AwsBucket) -> IBucket:
#         return AwsBucketEntity.factory(
#             name=instance.name,
#             access_browser=instance.access_browser,
#             url=instance.url,
#             location=instance.region,
#             uuid=instance.uuid,
#             # properties=instance.properties,
#         )
