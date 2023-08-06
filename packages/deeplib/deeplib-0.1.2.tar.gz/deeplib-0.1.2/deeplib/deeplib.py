import sys
from typing import TYPE_CHECKING, Optional, Union

import gi

from .pipeline.builder import PipelineBuilder
from .pipeline.json_config import JsonPipelineConfigLoader
from .platform.director import Platform
from .rtsp_utils import RTSPServer

if TYPE_CHECKING:
    from .platform.generic import GenericPlatform
    from .platform.nvidia import NvidiaPlatform

gi.require_version("Gst", "1.0")

from gi.repository import GObject, Gst


class DeepLib:

    _instance: Optional["DeepLib"] = None
    _platform: Optional[Union["GenericPlatform", "NvidiaPlatform", "Platform"]] = None
    rtsp_server: Optional["RTSPServer"] = None

    def __init__(self) -> None:
        # Standard GStreamer initialization
        GObject.threads_init()
        Gst.init(None)

    @classmethod
    def init(cls) -> None:
        cls._instance = cls()
        cls._instance._platform = Platform.create()
        print("Platform: " + str(cls._instance._platform))

    @classmethod
    def platform(
        cls,
    ) -> Optional[Union["GenericPlatform", "NvidiaPlatform", "Platform"]]:
        return getattr(cls._instance, "_platform", None)

    @classmethod
    def pipeline(cls):
        return PipelineBuilder(cls._instance)

    @classmethod
    def pipeline_from_json_config(cls, path):
        return JsonPipelineConfigLoader(cls._instance).load_from_file(path)

    @staticmethod
    def gst_callback(bus, message, loop):
        t = message.type
        if t == Gst.MessageType.EOS:
            sys.stdout.write("End-of-stream\n")
            loop.quit()
        elif t == Gst.MessageType.WARNING:
            err, debug = message.parse_warning()
            sys.stderr.write("Warning: %s: %s\n" % (err, debug))
        elif t == Gst.MessageType.ERROR:
            err, debug = message.parse_error()
            sys.stderr.write("Error: %s: %s\n" % (err, debug))
            loop.quit()
        return True

    @classmethod
    def run_on_main(cls, pipeline):
        # create an event loop and feed gstreamer bus mesages to it
        loop = GObject.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", cls.gst_callback, loop)

        # start play back and listen to events
        print("Starting pipeline \n")
        pipeline.set_state(Gst.State.PLAYING)
        try:
            loop.run()
        except:
            pass

        # cleanup
        pipeline.set_state(Gst.State.NULL)


H264 = "H264"
