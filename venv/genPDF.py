from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def generate_pdf(requirements, output_path):
    c = canvas.Canvas(output_path, pagesize=letter)
    width, height = letter
    y = height - 40

    for req, priority in requirements:
        c.drawString(30, y, f"{req} - Prioridad: {priority}")
        y -= 20
        if y < 40:
            c.showPage()
            y = height - 40

    c.save()