from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet

def generate_pdf(commentary, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()

    content = []
    content.append(Paragraph("AI Investment Commentary Report", styles['Title']))
    content.append(Paragraph(commentary, styles['BodyText']))

    doc.build(content)
    return filename