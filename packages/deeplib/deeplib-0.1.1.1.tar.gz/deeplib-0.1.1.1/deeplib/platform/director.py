from typing import TYPE_CHECKING, Union

from deeplib.platform.generic import GenericPlatform
from deeplib.platform.interface import PlatformInterface

if TYPE_CHECKING:
    from deeplib.platform.nvidia import NvidiaPlatform


class Platform(PlatformInterface):
    def create_hw_accelerated_element(self, _type) -> None:
        return None

    @classmethod
    def create(cls) -> Union["GenericPlatform", "NvidiaPlatform"]:
        # Nvidia
        from deeplib.platform.nvidia import NvidiaPlatform

        nvidia = NvidiaPlatform.create()

        if nvidia:
            return nvidia

        # Xilinx
        from deeplib.platform.xilinx import XilinxPlatform

        xilinx = XilinxPlatform.create()

        if xilinx:
            return xilinx

        # Generic
        return GenericPlatform.create()
