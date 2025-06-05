from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import os
import time
import re
from markdown_it import MarkdownIt

def markdown_to_docx(doc, markdown_text):
    """Convert markdown text to properly formatted Word document."""
    if not markdown_text:
        return
    
    # Parse markdown
    md = MarkdownIt()
    tokens = md.parse(markdown_text)
    
    # Track list types and levels
    list_types = []
    list_level = 0
    
    i = 0
    while i < len(tokens):
        token = tokens[i]
        
        # Handle headings
        if token.type == 'heading_open':
            level = int(token.tag[1])  # h1, h2, etc.
            i += 1  # Move to content token
            content = tokens[i].content if i < len(tokens) else ""
            doc.add_heading(content, level=level)
            i += 2  # Skip closing tag
            continue
            
        # Handle paragraphs
        elif token.type == 'paragraph_open':
            i += 1  # Move to content token
            if i >= len(tokens):
                i += 1
                continue
                
            content = tokens[i].content
            p = doc.add_paragraph()
            
            # Process inline formatting
            parts = re.split(r'(\*\*|\*|__|_|`)', content)
            is_bold = False
            is_italic = False
            is_code = False
            
            for part in parts:
                if part == '**' or part == '__':
                    is_bold = not is_bold
                elif part == '*' or part == '_':
                    is_italic = not is_italic
                elif part == '`':
                    is_code = not is_code
                else:
                    run = p.add_run(part)
                    run.bold = is_bold
                    run.italic = is_italic
                    if is_code:
                        run.font.name = 'Courier New'
                        run.font.size = Pt(10)
            
            i += 2  # Skip closing tag
            continue
            
        # Handle lists
        elif token.type == 'bullet_list_open':
            list_types.append('bullet')
            list_level += 1
            i += 1
            continue
        elif token.type == 'ordered_list_open':
            list_types.append('ordered')
            list_level += 1
            i += 1
            continue
        elif token.type == 'bullet_list_close' or token.type == 'ordered_list_close':
            if list_types:
                list_types.pop()
            list_level = max(0, list_level - 1)
            i += 1
            continue
        elif token.type == 'list_item_open':
            i += 1
            # Find the content of this list item
            content = ""
            while i < len(tokens) and tokens[i].type != 'list_item_close':
                if tokens[i].type == 'paragraph_open':
                    i += 1
                    if i < len(tokens):
                        content = tokens[i].content
                    i += 1
                else:
                    i += 1
            
            # Add the list item with proper indentation
            p = doc.add_paragraph()
            
            # Create bullet points manually with proper indentation
            indent = list_level * 0.25
            p.paragraph_format.left_indent = Inches(indent)
            p.paragraph_format.first_line_indent = Inches(-0.25)
            
            # Add bullet character or number based on list type
            current_list_type = list_types[-1] if list_types else 'bullet'
            if current_list_type == 'bullet':
                bullet_char = '•' if list_level % 2 == 1 else '○'
                p.add_run(f"{bullet_char} ").bold = True
            else:  # ordered list
                p.add_run(f"1. ").bold = True
                
            # Add the content with any formatting
            parts = re.split(r'(\*\*|\*|__|_|`)', content)
            is_bold = False
            is_italic = False
            is_code = False
            
            for part in parts:
                if part == '**' or part == '__':
                    is_bold = not is_bold
                elif part == '*' or part == '_':
                    is_italic = not is_italic
                elif part == '`':
                    is_code = not is_code
                else:
                    run = p.add_run(part)
                    run.bold = is_bold
                    run.italic = is_italic
                    if is_code:
                        run.font.name = 'Courier New'
                        run.font.size = Pt(10)
            
            i += 1
            continue
            
        # Handle code blocks
        elif token.type == 'fence' and token.tag == 'code':
            # Add a code block with monospaced font and gray background
            p = doc.add_paragraph()
            code_text = token.content
            
            # Add light gray shading to the paragraph
            shading_elm = OxmlElement('w:shd')
            shading_elm.set(qn('w:fill'), 'F5F5F5')  # Light gray
            p._p.get_or_add_pPr().append(shading_elm)
            
            # Format code with monospaced font
            code_run = p.add_run(code_text)
            code_run.font.name = 'Courier New'
            code_run.font.size = Pt(10)
            
            i += 1
            continue
            
        # Handle horizontal rules
        elif token.type == 'hr':
            p = doc.add_paragraph()
            p.add_run('_' * 50)
            i += 1
            continue
            
        # Default: move to next token
        i += 1

def write_docx(title, summary, dfd, schema, image_path):
    """Create a Word document with proper formatting from markdown content."""
    doc = Document()
    doc.add_heading(title, 0)
    
    # Design Summary section
    doc.add_heading('Design Summary', level=1)
    markdown_to_docx(doc, summary.content)

    # Data Flow Diagram image
    if image_path:
        doc.add_heading("Data Flow Diagram", level=1)
        doc.add_picture(image_path, width=Inches(6.0))

    # Data Flow Diagram (Mermaid) section
    doc.add_heading('Data Flow Diagram (Mermaid)', level=1)
    markdown_to_docx(doc, dfd.content)

    # Database Schema section
    doc.add_heading('Database Schema (SQL)', level=1)
    markdown_to_docx(doc, schema.content)

    # Save the document
    filename = title.replace(" ", "_") + time.strftime("_%Y%m%d_%H%M%S") + ".docx"
    folder = "agent_output_design_docs"
    os.makedirs(folder, exist_ok=True)
    doc.save(os.path.join(folder, filename))
    return filename
