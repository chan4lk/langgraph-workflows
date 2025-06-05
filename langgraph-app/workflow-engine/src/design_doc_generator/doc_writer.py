from docx import Document
import os
def write_docx(title, summary, dfd, schema):
    doc = Document()
    doc.add_heading(title, 0)
    
    doc.add_heading('Design Summary', level=1)
    doc.add_paragraph(summary.content)

    doc.add_heading('Data Flow Diagram (Mermaid)', level=1)
    doc.add_paragraph(dfd.content)

    doc.add_heading('Database Schema (SQL)', level=1)
    doc.add_paragraph(schema.content)

    filename = title.replace(" ", "_") + ".docx"
    folder = "agent_output_design_docs"
    os.makedirs(folder, exist_ok=True)
    doc.save(os.path.join(folder, filename))
    return filename
