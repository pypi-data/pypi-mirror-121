import gi

gi.require_version("Gst", "1.0")
gi.require_version("GstRtspServer", "1.0")
from gi.repository import Gst, GstRtspServer


class RTSPPipelineFactory(GstRtspServer.RTSPMediaFactory):
    def __init__(self, udp_port: int = 12222, encoding: str = "H264") -> None:
        GstRtspServer.RTSPMediaFactory.__init__(self)
        self.udp_port = udp_port
        self.encoding = encoding

    def do_create_element(self):
        pipeline_str = f'( udpsrc name=pay0 port={self.udp_port} caps="application/x-rtp, media=video, clock-rate=90000, encoding-name={self.encoding}, payload=96" )'
        print("RTSP pipeline def: {}".format(pipeline_str))
        return Gst.parse_launch(pipeline_str)


class RTSPServer:
    def __init__(self) -> None:
        print("Creating RTSP server")
        self.server = GstRtspServer.RTSPServer()

        self.server.attach(None)
        print("Creating Rtsp server done.")

    def add_path(self, path):
        factory = RTSPPipelineFactory()
        factory.set_shared(True)

        self.server.get_mount_points().add_factory(path, factory)
