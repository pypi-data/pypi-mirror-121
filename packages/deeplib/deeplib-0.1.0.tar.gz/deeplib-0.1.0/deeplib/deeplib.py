import gi
gi.require_version('Gst', '1.0')


class DeepLib:
    def __init__(self) -> None:
        # Standard GStreamer initialization
        GObject.threads_init()
        Gst.init(None)