import pymupdf
import re

def extract (file_path):
    doc = pymupdf.open(file_path)
    text = ""
    lines = []

    for page in doc:
        text += page.get_text('text')
        lines = [line.strip() for line in re.split(r'[\/\n\:]', text)]
    doc.close()
    
    return lines

