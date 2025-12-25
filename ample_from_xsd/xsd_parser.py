from xmlschema import XMLSchema


def clean_xsd_name(name):
    if not name:
        return ""
    name = str(name)
    if "}" in name:
        name = name.split("}", 1)[1]
    if "__" in name:
        name = name.split("__", 1)[0]
    return name


def parse_xsd(xsd_path: str):
    schema = XMLSchema(xsd_path)

    elements = []
    complex_types = []
    simple_types = []

    # Global elements
    for e in schema.elements.values():
        print("\nelement :\n"+e.tostring())
        elements.append({
            "kind": "element",
            "name": clean_xsd_name(e.name),
            "type": clean_xsd_name(e.type.name),
            "namespace": e.target_namespace,
            "doc": e.annotation.documentation if e.annotation else ""
        })

    for t in schema.types.values():
        print("\n Compplex or simple \n"+t.tostring())
        if t.is_complex() and t.content and hasattr(t.content, "iter_elements"):
            children = []
            for c in t.content.iter_elements():
                children.append({
                    "name": clean_xsd_name(c.name),
                    "type": clean_xsd_name(c.type.name),
                    "min": c.min_occurs,
                    "max": c.max_occurs
                })
            print("\nChildren\n"+children.__str__())
            complex_types.append({
                "kind": "complexType",
                "name": clean_xsd_name(t.name),
                "children": children
            })

        else:
            print("\nSimple Type\n")
            simple_types.append({
                "kind": "simpleType",
                "name": clean_xsd_name(t.name),
                "base": clean_xsd_name(t.base_type.name)
                if t.base_type else None,
                "facets": list(t.facets.keys()) if hasattr(t, "facets") else []
            })

    return elements, complex_types, simple_types
