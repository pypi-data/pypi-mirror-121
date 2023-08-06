import os
import sys
from typing import Optional

from deeplib.gst_element_factory import GstElementFactory
from deeplib.pipeline.elements import PipelineElement
from deeplib.platform.interface import PlatformInterface


# Nvidia DeepStream based platform
class NvidiaPlatform(PlatformInterface):
    DEFAULT_DEEPSTREAM_PYTHON_LIB_PATH = os.getenv(
        "DEFAULT_DEEPSTREAM_PYTHON_LIB_PATH",
        "/opt/nvidia/deepstream/deepstream-5.1/sources/python/apps/",
    )

    @classmethod
    def create(cls) -> Optional["NvidiaPlatform"]:
        try:
            sys.path.append(cls.DEFAULT_DEEPSTREAM_PYTHON_LIB_PATH)

            from common.is_aarch_64 import is_aarch64

            return cls()

        except ImportError:
            return None

    def create_hw_accelerated_element(self, _type, props=None):
        if not isinstance(props, dict):
            props = {}

        if _type == PipelineElement.ELEMENT_TYPE_H264_DECODE:
            return GstElementFactory.element("nvv4l2decoder")

        elif _type == PipelineElement.ELEMENT_TYPE_H264_ENCODE:
            return GstElementFactory.element(
                "nvv4l2h264enc",
                {
                    "bitrate": props["bit_rate"],
                    "preset-level": 1,
                    "insert-sps-pps": 1,
                    "bufapi-version": 1,
                },
            )

        elif _type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_I420_RAW:
            return GstElementFactory.caps_filter(
                "video/x-raw(memory:NVMM), format=I420"
            )

        elif _type == PipelineElement.ELEMENT_TYPE_CAPS_FILTER_NV12_720P:
            return GstElementFactory.caps_filter(
                "video/x-raw(memory:NVMM), format=NV12, width=1280 height=720 framerate=30/1"
            )

        elif _type == PipelineElement.ELEMENT_TYPE_VIDEO_CONVERT:
            return GstElementFactory.element("nvvideoconvert")

        elif _type == PipelineElement.ELEMENT_TYPE_STREAM_MUX:
            return GstElementFactory.element(
                "nvstreammux",
                {
                    "width": 1920,
                    "height": 1080,
                    "batch-size": 1,
                    "batched-push-timeout": 4000000,
                },
            )

        elif _type == PipelineElement.ELEMENT_TYPE_CAMERA_SOURCE:
            return GstElementFactory.element("nvarguscamerasrc")

        elif _type == PipelineElement.ELEMENT_TYPE_GL_SINK:
            return GstElementFactory.element("nveglglessink")

        elif _type == PipelineElement.ELEMENT_TYPE_GL_TRANSFORM:
            return GstElementFactory.element("nvegltransform")

        else:
            return None
