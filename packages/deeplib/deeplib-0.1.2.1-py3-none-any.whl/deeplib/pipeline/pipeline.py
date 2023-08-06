import gi

gi.require_version("Gst", "1.0")
from gi.repository import Gst

from ..pipeline.processing import Multiplexer


class Pipeline:
    def __init__(self, gst_pipeline):
        self.pipeline = gst_pipeline
        self.elements = []
        self.elements_by_id = dict()

    def add(self, element):
        self.elements.append(element)
        self.elements_by_id[element._id] = element

    def as_gst_pipeline(self):
        # auto-generate links:
        by_id = dict()
        by_link = dict()
        last_element_id = None
        last_element_by_id = dict()
        for element in self.elements:
            if element.link_to:
                last_element_id = last_element_by_id[element.link_to.split("/")[0]]

            for sub_element in element.gst_elements:
                _id = sub_element["_id"]
                by_id[_id] = sub_element

                link_to = sub_element["link_to"]
                if not link_to and last_element_id:
                    sub_element["link_to"] = last_element_id
                    link_to = sub_element["link_to"]

                if link_to not in by_link:
                    by_link[link_to] = []

                by_link[link_to].append(_id)
                last_element_id = _id
                last_element_by_id[element._id] = _id

        # auto-generate multiplexers (for outputs linked to multiple inputs)
        multiplexers_by_id = dict()
        multiplexers_out_nr_by_id = dict()
        for _id, from_list in by_link.items():
            if len(from_list) > 1:
                print(f"multiplexer {_id}")
                multiplexers_by_id[_id] = Multiplexer(
                    len(from_list), _id="multiplexer-" + _id, link_to=_id
                )
                multiplexers_out_nr_by_id[_id] = 0
                self.elements.append(multiplexers_by_id[_id])
                for nr in range(0, len(from_list)):
                    by_id[from_list[nr]]["link_to"] = multiplexers_by_id[_id].output_id(
                        nr
                    )
                    print(
                        f"   link_multi {from_list[nr]} {by_id[from_list[nr]]['link_to']}"
                    )

        # add elements:
        for element in self.elements:
            for sub_element in element.gst_elements:
                _id = sub_element["_id"]
                by_id[_id] = sub_element
                link_to = sub_element["link_to"]
                gst_element = sub_element["gst_element"]
                print(f"add_comp {_id} linkto: {link_to}")
                self.pipeline.add(gst_element)

        # link:
        last = None
        for element in self.elements:
            for sub_element in element.gst_elements:
                _id = sub_element["gst_element"]
                gst_element = sub_element["gst_element"]
                link_to = sub_element["link_to"]

                if link_to:
                    link_to_element = by_id[link_to]
                    last = link_to_element["gst_element"]
                    print(f"link {link_to_element['_id']} -> {sub_element['_id']}")
                    # if linkTo in multiplexersById and id in byLink[linkTo]:
                    #    multiplexerOutNr = multiplexersOutNrById[linkTo]
                    #    multiplexersOutNrById[linkTo] += 1
                    #    link_to_element = byId[multiplexersById[linkTo].outputId(multiplexerOutNr)]
                    #    print(f"   link_multi {link_to_element['id']}")

                    if sub_element["gst_sink_pad"] or link_to_element["gst_source_pad"]:
                        if sub_element["gst_sink_pad"]:
                            sink_pad = gst_element.get_request_pad(
                                sub_element["gst_sink_pad"]
                            )
                        else:
                            sink_pad = gst_element.get_static_pad("sink")

                        if link_to_element["gst_source_pad"]:
                            src_pad = last.get_request_pad(
                                link_to_element["gst_source_pad"]
                            )
                        else:
                            src_pad = last.get_static_pad("src")

                        src_pad.link(sink_pad)

                    else:
                        last.link(gst_element)

            last = gst_element

        # probes
        for component in self.elements:
            for sub_element in component.gst_elements:
                gst_element = sub_element["gst_element"]
                if sub_element["gst_probes"]:
                    for pad, probe in sub_element["gst_probes"].items():
                        print("add_probe {} {}".format(pad, probe))
                        pad = gst_element.get_static_pad(pad)
                        pad.add_probe(Gst.PadProbeType.BUFFER, probe, 0)

        return self.pipeline
