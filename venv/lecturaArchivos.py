import fitz  # PyMuPDF
import docx

def read_pdf(file_path):
    text = ""
    with fitz.open(file_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def read_docx(file_path):
    doc = docx.Document(file_path)
    text = "\n".join([para.text for para in doc.paragraphs])
    return text

def classify_requirements(text, genai):
    requirements = []
    for line in text.split('\n'):
        if line.strip():
            prompt = f"Classify the following requirement by priority (low, medium, high): {line}"
            response = genai.GenerativeModel('gemini-pro').generate_content(prompt)
            priority = response._result.candidates[0].content.parts[0].text.strip()
            requirements.append((line, priority))
    return requirements
