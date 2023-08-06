from deeplib.gst_element_factory import GstElementFactory
from deeplib.pipeline.processing import ProcessingElement


class XilinxFaceDetect(ProcessingElement):
    def __init__(self, _id=None, link_to=None):
        ProcessingElement.__init__(self, _id, link_to)

        videoconvert = GstElementFactory.element("videoconvert")
        facedetect = GstElementFactory.element("vaifacedetect")

        self.add_multiple(videoconvert, facedetect)


class XilinxPersonDetect(ProcessingElement):
    def __init__(self, _id=None, link_to=None):
        ProcessingElement.__init__(self, _id, link_to)

        persondetect = GstElementFactory.element("vaipersondetect")
        videoconvert = GstElementFactory.element("videoconvert")

        self.add_multiple(videoconvert, persondetect)


class XilinxSingleShotDetector(ProcessingElement):
    def __init__(self, model, _id=None, link_to=None):
        ProcessingElement.__init__(self, _id, link_to)

        vaissd = GstElementFactory.element("vaissd", {"model": model})
        videoconvert = GstElementFactory.element("videoconvert")

        self.add_multiple(videoconvert, vaissd)
