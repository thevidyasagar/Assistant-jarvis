"""
file_reader.py – Reads PDF, TXT, DOCX, PPTX, EXCEL into plain text
"""

import fitz  # PyMuPDF
import docx
import pandas as pd
import os

def read_pdf(path):
    text = ""
    doc = fitz.open(path)
    for page in doc:
        text += page.get_text()
    return text

def read_docx(path):
    doc = docx.Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def read_txt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def read_excel(path):
    df = pd.read_excel(path)
    return df.to_string()

def load_file(path):
    ext = path.lower().split(".")[-1]

    if ext == "pdf":
        return read_pdf(path)
    if ext == "docx":
        return read_docx(path)
    if ext == "txt":
        return read_txt(path)
    if ext in ["xls", "xlsx"]:
        return read_excel(path)

    raise ValueError("Unsupported file type: " + ext)
