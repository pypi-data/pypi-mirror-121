from ..platform.generic import GenericPlatform
from ..platform.interface import PlatformInterface
from typing import TYPE_CHECKING, Union, Any

if TYPE_CHECKING:
    from ..platform.nvidia import NvidiaPlatform


class Platform(PlatformInterface):
    def create_hw_accelerated_element(self, _type, props=None) -> Any:
        return None

    @classmethod
    def create(cls) -> Union["GenericPlatform", "NvidiaPlatform"]:
        # Nvidia
        from ..platform.nvidia import NvidiaPlatform

        nvidia = NvidiaPlatform.create()

        if nvidia:
            return nvidia

        # Xilinx
        from ..platform.xilinx import XilinxPlatform

        xilinx = XilinxPlatform.create()

        if xilinx:
            return xilinx

        # Generic
        return GenericPlatform.create()
