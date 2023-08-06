from typing import Any

from ..platform.interface import PlatformInterface

from ..gst_element_factory import GstElementFactory
from ..pipeline.elements import PipelineElement


# Generic Gstreamer platform
class GenericPlatform(PlatformInterface):
    @classmethod
    def create(cls) -> "GenericPlatform":
        return cls()

    def create_hw_accelerated_element(self, _type, props=None) -> Any:
        if not isinstance(props, dict):
            props = {}

        if _type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("avdec_h264")

        elif _type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element(
                "x264enc",
                {
                    "bitrate": props["bit_rate"],
                    "speed-preset": "ultrafast",
                    "tune": "zerolatency",
                },
            )

        elif _type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW:
            return GstElementFactory.caps_filter("video/x-raw, format=I420")

        elif _type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720P:
            return GstElementFactory.caps_filter(
                "video/x-raw, format=NV12, width=1280 height=720 framerate=30/1"
            )

        elif _type == PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT:
            return GstElementFactory.element("videoconvert")

        elif _type == PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE:
            return GstElementFactory.element("v4l2src")

        elif _type == PipelineElement.ELEMENT_TYPE_GL_SINK:
            return GstElementFactory.element("glimagesink")

        else:
            return None
