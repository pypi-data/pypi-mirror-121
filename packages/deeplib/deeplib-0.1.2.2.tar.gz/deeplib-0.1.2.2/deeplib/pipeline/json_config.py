import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..pipeline.builder import PipelineBuilder


class JsonPipelineConfigLoader:
    def __init__(self, deep_lib):
        self.deep_lib = deep_lib
        self.pipeline_builder: "PipelineBuilder" = self.deep_lib.pipeline()

    def load_from_file(self, path):
        with open(path) as json_file:
            data = json.load(json_file)
            for element in data["elements"]:
                _id = element["_id"]
                _type = element["_type"]
                properties = element.get("properties")
                links = element.get("links")
                self.parse_element(_id, _type, properties, links)

        return self.pipeline_builder.build()

    def parse_element(self, _id, _type, properties, connections):
        print(f"parse element {_id} {_type} {properties} {connections}")
        if _type == "file-input":
            self.pipeline_builder.with_file_input(_id=_id, path=properties["path"])

        elif _type == "mipi-camera-input":
            self.pipeline_builder.with_mipi_camera_input(_id=_id)

        elif _type == "usb-camera-input":
            self.pipeline_builder.with_usb_camera_input(_id=_id)

        elif _type == "nv-infer":
            self.pipeline_builder.with_nv_infer(
                _id=_id,
                config_path=properties["path"],
                link_to=self.connection_to_component_id(connections["in"]),
            )

        elif _type == "nv-tracker":
            self.pipeline_builder.with_nv_tracker(
                _id=_id,
                config_path=properties["path"],
                link_to=self.connection_to_component_id(connections["in"]),
            )

        elif _type == "nv-osd":
            self.pipeline_builder.with_nv_osd(
                _id=_id, link_to=self.connection_to_component_id(connections["in"])
            )

        elif _type == "egl-output":
            self.pipeline_builder.with_egl_output(
                _id=_id, link_to=self.connection_to_component_id(connections["in"])
            )

        elif _type == "rtsp-output":

            print(f"connections: {connections}")
            print(f"properties: {properties}")
            self.pipeline_builder.with_rtsp_output(
                _id=_id, path=properties["path"], link_to=connections["in"]
            )

        elif _type == "tcp-output":
            self.pipeline_builder.with_tcp_output(_id=_id, link_to=connections["in"])

    @staticmethod
    def connection_to_component_id(connection):
        return connection.split("/")[0]
