from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from llama_client import generate_xml_from_xsd
from xsd_utils import validate_xml

app = FastAPI(title="XSD + LLaMA Sample Generator")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XSD_DIR = os.path.join(BASE_DIR, "resource", "xsd")


class GenerateRequest(BaseModel):
    xsd_name: str


@app.post("/xsd/generate")
def generate_sample(req: GenerateRequest):
    xsd_path = os.path.join(XSD_DIR, req.xsd_name)
    print("xsd_path\n" + xsd_path)
    if not os.path.exists(xsd_path):
        raise HTTPException(status_code=404, detail="XSD not found")

    with open(xsd_path, "r", encoding="utf-8") as f:
        xsd_content = f.read()

    # 1️⃣ Generate structure
    # xml_skeleton = generate_xml_skeleton(xsd_path)
    # print(xml_skeleton)
    #
    # # 2️⃣ Fill values using LLaMA
    # final_xml = fill_values_with_llama(
    #     xsd=xsd_content,
    #     xml_skeleton=xml_skeleton
    # )
    #
    # return final_xml
    xml = generate_xml_from_xsd(xsd_content)
    print("XML\n" + xml)
    validate_xml(xsd_path, xml)
    return xml
