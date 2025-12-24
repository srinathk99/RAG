import os
import xmlschema
import xml.etree.ElementTree as ET
from lxml import etree

def validate_xml(xsd_path: str, xml_text: str) -> None:
    schema = xmlschema.XMLSchema(xsd_path)
    schema.validate(xml_text)

def generate_xml_skeleton(xsd_path: str) -> str:
    schema = xmlschema.XMLSchema(
        xsd_path,
        base_url=os.path.dirname(xsd_path)
    )

    # Pick the first non-abstract global root
    root_elem = next(
        e for e in schema.root_elements
        if not e.abstract
    )

    # Generate skeleton using xmlschema (stdlib Element)
    xml_elem_std = schema.encode(
        {},
        path=root_elem.name,
        validation="skip",
        fill_missing=True
    )

    # 🔁 CORRECT conversion: stdlib → bytes → lxml
    xml_bytes = ET.tostring(
        xml_elem_std,
        encoding="utf-8",
        xml_declaration=True
    )

    xml_elem_lxml = etree.fromstring(xml_bytes)

    # Serialize with lxml
    return etree.tostring(
        xml_elem_lxml,
        encoding="UTF-8",
        xml_declaration=True
    ).decode("utf-8")
