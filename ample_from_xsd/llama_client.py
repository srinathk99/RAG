import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3"
MODEL2="qwen3:30b"



def generate_xml_from_xsd(xsd_text: str) -> str:
    prompt = f"""
You are an XML generator.

Task:
Generate a SINGLE valid XML document that STRICTLY conforms to the given XSD.

Rules (MANDATORY):
- Generate xml with dummy values but meaningful values
- Validate the generated xml
- If any error occurs, use the error info and re-generate the xml from scratch
- Repeat the process until you are generating an valid error-free xml from xsd
- For each element generate an xml with dummy value

XSD:
{xsd_text}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL2,
            "prompt": prompt,
            "stream": False
        },
        timeout=None
    )

    response.raise_for_status()

    return response.json()["response"].strip()


def fill_values_with_llama(xsd: str, xml_skeleton: str) -> str:
    prompt = f"""
You are given an XML skeleton generated strictly from an XSD.

RULES (MANDATORY):
- DO NOT add, remove, or rename any XML tags
- DO NOT change element order
- Fill only the element values
- Keep values realistic and schema-appropriate
- Return ONLY valid XML (no explanation)

XSD:
{xsd}

XML Skeleton:
{xml_skeleton}
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    return response.json()["response"].strip()
