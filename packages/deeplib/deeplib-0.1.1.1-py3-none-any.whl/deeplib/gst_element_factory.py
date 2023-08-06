from gi.repository import Gst

from deeplib.deeplib import error


def check_created(element, description):
    if not element:
        raise error(f"Failed to create Gst {description}")
    return element


class GstElementFactory:
    @staticmethod
    def pipeline():
        print("Creating Pipeline")
        pipeline = Gst.Pipeline()
        return check_created(pipeline, "pipeline")

    @staticmethod
    def element(_type, properties=None):
        print(f"create_elem {_type}: props={properties}")
        element = Gst.ElementFactory.make(_type)

        if properties:
            for name, value in properties.items():
                element.set_property(name, value)
        return check_created(element, _type)

    @classmethod
    def caps_filter(cls, caps):
        return cls.element("capsfilter", {"caps": Gst.caps_from_string(caps)})
