#!/usr/bin/env python3
# List files containg JavaScript code and print this code
# USAGE: ./get_js_from_pdf_files.py $files
# Script Dependencies:
#    pypdf
import sys
from pypdf import PdfReader
from pypdf.generic import IndirectObject

def resolve(obj):
    if isinstance(obj, IndirectObject):
        obj = obj.get_object()
    return obj

for filepath in sys.argv[1:]:
    reader = PdfReader(filepath)
    if reader.is_encrypted:
        reader.decrypt("fpdf2")
    names = resolve(reader.root_object["/Names"]) if "/Names" in reader.root_object else ()
    if "/JavaScript" in names:
        print(filepath, "contains JavaScript")
        for name in resolve(names["/JavaScript"])["/Names"]:
            action = resolve(name)
            if "/JS" in action:
                print("   ", action["/JS"])
