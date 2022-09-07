import abc
from typing import Optional, Any


class ISettings(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def get_region(self) -> Optional[str]:
        ...

    @abc.abstractmethod
    def set_credentials(self, *args) -> None:
        ...

    @abc.abstractmethod
    def get_credentials(self) -> Optional[Any]:
        ...

    @abc.abstractmethod
    def authentication(self, access_key: str, secret_access_key: str) -> Any:
        ...
