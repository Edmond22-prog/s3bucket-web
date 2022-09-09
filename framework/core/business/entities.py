from dataclasses import dataclass, field
from typing import Optional, Dict
from uuid import UUID, uuid4

from core.business.interface.ibucket import IBucket


@dataclass
class AwsBucketEntity(IBucket):
    _name: str
    _access_browser: str
    _location: str
    _url: str
    # _properties: Dict = field(default_factory=dict)
    _uuid: UUID = field(default=uuid4())

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def url(self) -> str:
        return self._url

    @property
    def location(self) -> str:
        return self._location

    # @property
    # def properties(self) -> Optional[Dict]:
    #     return self._properties
    #
    # @properties.setter
    # def properties(self, properties: Dict) -> None:
    #     self._properties = properties

    @property
    def access_browser(self) -> str:
        return self._access_browser

    @classmethod
    def factory(
        cls,
        name: str,
        access_browser: str,
        url: str,
        location: str,
        # properties: Optional[dict] = None,
        uuid: Optional[UUID] = None,
    ) -> IBucket:
        uuid = uuid or uuid4()
        # properties = properties or {}
        obj = cls(
            _name=name,
            _access_browser=access_browser,
            _url=url,
            _location=location,
            # _properties=properties,
            _uuid=uuid,
        )
        return obj
