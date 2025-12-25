
#from vector.chroma_store import get_schema_collection
from ample_from_xsd.xsd_parser import parse_xsd
from ample_from_xsd.xsd_formatter import (
    format_element,
    format_complex_type,
    format_simple_type
)


def ingest_xsd_file(xsd_path: str):
    #collection = get_schema_collection()

    elements, complex_types, simple_types = parse_xsd(xsd_path)

    docs, ids, metas = [], [], []

    for e in elements:
        docs.append(format_element(e))
        # ids.append(f"{schema_name}:{version}:element:{e['name']}")
        # metas.append({
        #     "schema": schema_name,
        #     "version": version,
        #     "kind": "element",
        #     "name": e["name"]
        # })

    for t in complex_types:
        docs.append(format_complex_type(t))
        # ids.append(f"{schema_name}:{version}:complexType:{t['name']}")
        # metas.append({
        #     "schema": schema_name,
        #     "version": version,
        #     "kind": "complexType",
        #     "name": t["name"]
        # })

    for t in simple_types:
        docs.append(format_simple_type(t))
        # ids.append(f"{schema_name}:{version}:simpleType:{t['name']}")
        # metas.append({
        #     "schema": schema_name,
        #     "version": version,
        #     "kind": "simpleType",
        #     "name": t["name"]
        # })

    # collection.add(documents=docs, metadatas=metas, ids=ids)
    # print(f"✅ Ingested {len(docs)} schema facts for {schema_name} v{version}")
    return "".join(map(str, docs))