def format_element(e):
    return (
        f'Element "{e["name"]}" is defined in the schema.\n'
        f'Its type is "{e["type"]}".\n'
        f'Namespace: {e["namespace"]}.\n'
        f'Description: {e["doc"] or "No documentation provided."}'
    )


def format_complex_type(t):
    lines = [f'Complex type "{t["name"]}" consists of:']

    for c in t["children"]:
        occ = "required" if c["min"] > 0 else "optional"
        max_occ = "unbounded" if c["max"] is None else c["max"]

        lines.append(
            f'- {c["name"]}: type {c["type"]} '
            f'({occ}, max {max_occ})'
        )

    return "\n".join(lines)


def format_simple_type(t):
    return (
        f'Simple type "{t["name"]}" is based on "{t["base"]}".\n'
        f'Constraints: {", ".join(t["facets"]) or "none"}'
    )
