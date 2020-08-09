import os
import textract
from tkinter import filedialog
from docx import Document
from docx.shared import RGBColor, Pt
from docx.oxml.ns import qn
from docx.oxml.shared import OxmlElement
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# This code is mainly for reading and outputing files

# TODO: Try to solve the problem of double newlines when reading word documents


# Read file
def importFile(path):
    if not os.path.exists(path):
        return ''

    txt = ''
    if path.lower().endswith(('.docx', '.pdf')):
        rep = (b'\n\n', b'\n') if path.lower().endswith(
            ('.doc', '.docx')) else (b'\r\n', b'\n')
        txt = textract.process(path).replace(*rep).decode('utf-8')
    else:
        f = open(path, 'r', encoding='utf-8')
        txt = f.read()
    '''elif path.lower().endswith('.doc'):
        docx_file = path + 'x'
        if not os.path.exists(docx_file):
            os.system('antiword ' + path + ' > ' + docx_file)
            with open(docx_file) as f:
                text = f.read()
            os.remove(docx_file)  # docx_file was just to read, so deleting
        else:
            # already a file with same name as doc exists having docx extension,
            # which means it is a different file, so we cant read it
            print(
                'Info : file with same name of doc exists having docx extension, so we cant read it')
            text = ''
    '''
    return txt


# Output to a file
def exportFile(output, underlineOnOff, strikethroughOnOff, highlightOnOff, paragraphMarkOnOff):
    if not output:
        return

    diffs = [(action, word.replace('¶\n', '\n')) for action, word in output]
    print('diffs:', diffs)

    # May add HTML format
    file = filedialog.asksaveasfile(initialdir='/', initialfile='output.docx', defaultextension='*.*', filetypes=[
        ('All Files', '.doc .docx .pdf .txt'),
        ('Word Documents', '.doc .docx'),
        ('Adobe PDF', '.pdf')])

    if file is None:
        return

    if file.name.lower().endswith(('.doc', '.docx')):
        # Create a template
        document = Document()

        # Add a paragraph
        p = document.add_paragraph()

        for action, text in diffs:
            # Add text to paragraph reference
            run = p.add_run(text)
            run.font.size = Pt(14) if action == 0 else Pt(16)

            # Get the XML tag
            tag = run._r

            # Create an XML element
            shd = OxmlElement('w:shd')

            # Add attributes to the element
            shd.set(qn('w:val'), 'clear')
            shd.set(qn('w:color'), 'auto')

            run.font.strike = strikethroughOnOff and action == -1
            run.font.underline = underlineOnOff and action == 1

            # Set the shading colour
            shd.set(qn('w:fill'), 'FFAAAA' if action == -1 else 'AAFFAA')

            # Append the element under <w:rPr>
            if action != 0:
                tag.rPr.append(shd)

        document.save(file.name)
    elif file.name.lower().endswith('.pdf'):
        # Change the text for outputing a PDF
        pdf_text = ''
        rep = ('\n', '¶<br/>') if paragraphMarkOnOff else ('\n', '<br/>')
        underline_open_tag, underline_close_tag = (
            '<u>', '</u>') if underlineOnOff else ('', '')
        strike_open_tag, strike_close_tag = (
            '<strike>', '</strike>') if strikethroughOnOff else ('', '')
        for action, text in diffs:
            if action == -1:
                pdf_text += '<span backcolor="#FFAAAA" fontSize=16>' + \
                    strike_open_tag + \
                    text.replace(*rep) + strike_close_tag + '</span>'
            elif action == 1:
                pdf_text += '<span backcolor="#AAFFAA" fontSize=16>' + \
                    underline_open_tag + \
                    text.replace(*rep) + underline_close_tag + '</span>'
            else:
                pdf_text += '<span>' + text.replace(*rep) + '</span>'

        # Register a font
        pdfmetrics.registerFont(TTFont('MSJH', './msjh.ttc'))

        # Create a style
        style = ParagraphStyle(
            name='Normal',
            fontName='MSJH',
            fontSize=14,
            leading=21,
        )

        # Output PDF file
        simpledoctemplate = SimpleDocTemplate(file.name)
        simpledoctemplate.build([Paragraph(pdf_text, style)])
    else:
        with open(file.name, 'w', encoding='utf-8') as f:
            f.write(''.join([word for _, word in diffs]))

    print('Output path:', file.name)
    file.close()


def test_function():
    print("test function!!")
