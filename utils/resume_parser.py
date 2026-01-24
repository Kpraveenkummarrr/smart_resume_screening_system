import pdfplumber
import docx

def extract_text(path):
    text = ""
    if path.endswith(".pdf"):
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text()
    elif path.endswith(".docx"):
        doc = docx.Document(path)
        for p in doc.paragraphs:
            text += p.text
    return text
