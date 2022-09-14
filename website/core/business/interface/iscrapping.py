import abc
from typing import Optional

from website.core.business.interface.ibucket import IBucket


class IScrapping(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def run(self) -> Optional[IBucket]:
        ...
