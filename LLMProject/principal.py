from flask import Flask
import google.generativeai as genai


app = Flask(__name__)

@app.route('/')

def index():
    generated_text = generate_text("What kind of questions can i ask to my client to know more about their business?") 
    return generated_text



genai.configure(api_key="AIzaSyDrgS_nkCcezHkVGD2PeOAet-Ut9fPOuAc")
model = genai.GenerativeModel('gemini-pro')

def generate_text(prompt):
    response = model.generate_content(prompt)
    return response._result.candidates[0].content.parts[0].text