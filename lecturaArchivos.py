import fitz  # PyMuPDF
import io
import docx

def read_pdf(file):
    text = ""
    file_bytes = file.read()  # Leer el archivo en bytes
    doc = fitz.open(stream=file_bytes, filetype="pdf")
    for page in doc:
        text += page.get_text()
    return text

def read_docx(file):
    file_bytes = io.BytesIO(file.read())  # Convertir el archivo a BytesIO
    doc = docx.Document(file_bytes)
    text = "\n".join([para.text for para in doc.paragraphs if para.text.strip()])
    return text

def classify_requirements(text, genai):
    paragraphs = [para.strip() for para in text.split('\n\n') if para.strip()]

    if not paragraphs:
        return []

    requirements = []
    model = genai.GenerativeModel('gemini-pro')  # Asegúrate de tener esta instancia configurada correctamente

    for paragraph in paragraphs:
        prompt = f"Classify the following requirements by priority (low, medium, high):\n\n{paragraph}"
        response = model.generate_content(prompt)
        print(response)
        classified_text = response._result.candidates[0].content
        print(classified_text._result.candidates[0].content)
        # Evitar la repetición de la palabra "Prioridad:" en cada línea
        clean_text = classified_text.replace("Prioridad: ", "")
        requirements.append((paragraph, clean_text))

    return requirements

"""
def classify_requirements(text, genai):
    lines = text.split('\n')
    requirements = [line for line in lines if line.strip() and "Prioridad:" not in line]
    
    if not requirements:
        return []

    prompt = "Classify the following requirements into functional and non-functional:\n"
    prompt += "\n".join(requirements)
    
    model = genai.GenerativeModel('gemini-pro')  # Asegúrate de tener esta instancia configurada correctamente
    response = model.generate_content(prompt)
    classified_text = response._result.candidates[0].content.parts[0].text.strip()
    
    classified_lines = classified_text.split('\n')
    classified_requirements = [(req, cls) for req, cls in zip(requirements, classified_lines) if req.strip()]

    return classified_requirements
"""