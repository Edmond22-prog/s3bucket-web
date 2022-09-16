from dataclasses import dataclass, field
from typing import Optional, Dict, List
from uuid import UUID, uuid4

from website.core.business.interface.irepository import IRepository
from website.core.business.interface.ivulnerability import IVulnerability
from website.core.business.interface.ibucket import IBucket


@dataclass
class AwsBucketEntity(IBucket):
    _name: str
    _access_browser: str
    _location: str
    _url: str
    _properties: Dict = field(default_factory=dict)
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

    @property
    def properties(self) -> Optional[Dict]:
        return self._properties

    @properties.setter
    def properties(self, properties: Dict) -> None:
        self._properties = properties

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


@dataclass
class VulnerabilityEntity(IVulnerability):
    _name: str
    _location: str
    _code_line: int
    _code_vulnerability: str
    _uuid: UUID = field(default=uuid4())

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def location(self) -> str:
        return self._location

    @property
    def code_line(self) -> int:
        return self._code_line

    @property
    def code_vulnerability(self) -> str:
        return self._code_vulnerability

    @classmethod
    def factory(
        cls,
        name: str,
        location: str,
        code_line: int,
        code_vulnerability: str,
        uuid: Optional[UUID] = None,
    ) -> IVulnerability:
        uuid = uuid or uuid4()
        obj = cls(
            _name=name,
            _location=location,
            _code_line=code_line,
            _code_vulnerability=code_vulnerability,
            _uuid=uuid,
        )
        return obj


@dataclass
class RepositoryEntity(IRepository):
    _name: str
    _owner: str
    _url: str
    _created_at: str
    _updated_at: str
    _languages: Dict
    _vulnerabilities: List[IVulnerability] = field(default_factory=list)
    _uuid: UUID = field(default=uuid4())

    @property
    def uuid(self) -> UUID:
        return self._uuid

    @property
    def name(self) -> str:
        return self._name

    @property
    def owner(self) -> str:
        return self._owner

    @property
    def url(self) -> str:
        return self._url

    @property
    def created_at(self) -> str:
        return self._created_at

    @property
    def updated_at(self) -> str:
        return self._updated_at

    @property
    def languages(self) -> Dict:
        return self._languages

    @property
    def vulnerabilities(self) -> List[IVulnerability]:
        return self._vulnerabilities

    @vulnerabilities.setter
    def vulnerabilities(self, vulnerabilities: List[IVulnerability]) -> None:
        self._vulnerabilities = vulnerabilities

    @classmethod
    def factory(
        cls,
        name: str,
        owner: str,
        url: str,
        created_at: str,
        updated_at: str,
        languages: Dict,
        uuid: Optional[UUID] = None,
    ) -> "RepositoryEntity":
        uuid = uuid or uuid4()
        obj = cls(
            _name=name,
            _owner=owner,
            _url=url,
            _created_at=created_at,
            _updated_at=updated_at,
            _languages=languages,
            _uuid=uuid,
        )
        return obj
