from flask import Flask, request, render_template,jsonify
import google.generativeai as genai
from lecturaArchivos import read_pdf, read_docx, classify_requirements
from genPDF import generate_pdf

app = Flask(__name__)


genai.configure(api_key="API-KEY")
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and file.filename.endswith('.pdf'):
        text = read_pdf(file)
    elif file and file.filename.endswith('.docx'):
        text = read_docx(file)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    requirements = classify_requirements(text)
    
    output_path = "processed_requirements.pdf"
    generate_pdf(requirements, output_path)

    return jsonify({"message": "File processed successfully", "output_path": output_path})


@app.route('/generate-questions', methods=['POST'])
def generate_questions():
    context = request.form['context']
    try:
        generated_text = generate_text(f"What kind of questions can I ask my client to better understand their needs? Context: {context}")
        questions = generated_text.split('\n')  
        print("Preguntas Generadas para Entender las Necesidades del Cliente:")  
        for question in questions:
            print(question)
        return render_template('questions.html', questions=questions)
    except Exception as e:
        error_message = f"Error durante la solicitud: {e}"
        return render_template('error.html', error=error_message)

def generate_text(prompt):
    response = model.generate_content(prompt)
    # Extraer el texto generado de la respuesta
    generated_text = response._result.candidates[0].content.parts[0].text
    return generated_text

if __name__ == '__main__':
    app.run(debug=True)
