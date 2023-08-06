from __future__ import annotations

import sys
from typing import Optional

import gi

from deeplib.pipeline.builder import PipelineBuilder
from deeplib.pipeline.json_config import JsonPipelineConfigLoader
from deeplib.platform.director import Platform
from deeplib.rtsp_utils import RTSPServer

gi.require_version("Gst", "1.0")

from gi.repository import GObject, Gst


class DeepLib:

    _instance: Optional["DeepLib"] = None
    _platform: Optional["Platform"] = None
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
    def platform(cls) -> Platform:
        return cls._instance._platform

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

    @staticmethod
    def run_on_main(pipeline):
        # create an event loop and feed gstreamer bus mesages to it
        loop = GObject.MainLoop()
        bus = pipeline.get_bus()
        bus.add_signal_watch()
        bus.connect("message", DeepLib.gstCallback, loop)

        # start play back and listen to events
        print("Starting pipeline \n")
        pipeline.set_state(Gst.State.PLAYING)
        try:
            loop.run()
        except:
            pass

        # cleanup
        pipeline.set_state(Gst.State.NULL)


class DeepError(Exception):
    def __init__(self, message):
        Exception.__init__(self, message)


def error(message):
    return DeepError(message)


H264 = "H264"
