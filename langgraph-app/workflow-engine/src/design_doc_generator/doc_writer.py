from docx import Document
from docx.shared import Inches
import os
import time
def write_docx(title, summary, dfd, schema, image_path):
    doc = Document()
    doc.add_heading(title, 0)
    
    doc.add_heading('Design Summary', level=1)
    doc.add_paragraph(summary.content)

    if image_path:
        doc.add_heading("Data Flow Diagram", level=1)
        doc.add_picture(image_path, width=Inches(6.0))

    doc.add_heading('Data Flow Diagram (Mermaid)', level=1)
    doc.add_paragraph(dfd.content)

    doc.add_heading('Database Schema (SQL)', level=1)
    doc.add_paragraph(schema.content)

    filename = title.replace(" ", "_") + time.strftime("_%Y%m%d_%H%M%S") + ".docx"
    folder = "agent_output_design_docs"
    os.makedirs(folder, exist_ok=True)
    doc.save(os.path.join(folder, filename))
    return filename
