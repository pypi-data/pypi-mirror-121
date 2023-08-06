from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from deeplib.platform.generic import GenericPlatform
    from deeplib.platform.nvidia import NvidiaPlatform


class PlatformInterface(ABC):
    @abstractmethod
    def create_hw_accelerated_element(self, _type) -> None:
        pass

    @classmethod
    @abstractmethod
    def create(cls) -> Union["GenericPlatform", "NvidiaPlatform"]:
        pass
