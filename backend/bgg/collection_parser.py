import xml.etree.ElementTree as ET


def parse_collection_ids(xml: str) -> list[int]:
    root = ET.fromstring(xml)

    return [
        int(item.attrib["objectid"])
        for item in root.findall("item")
    ]