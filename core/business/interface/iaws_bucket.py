import abc
from typing import Optional
from uuid import UUID

from core.business.interface.ibucket import IBucket


class IAwsBucket(IBucket):
    @abc.abstractmethod
    def access_browser(self) -> str:
        ...

    @classmethod
    def factory(
        cls, name: str, access_browser: str, url: str, location: str, properties: dict, uuid: Optional[UUID] = None
    ) -> "IAwsBucket":
        ...
