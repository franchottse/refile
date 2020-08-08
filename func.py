import os
import textract
from tkinter import filedialog
from docx import Document
from docx.shared import RGBColor, Pt
from diff_match_patch import diff_match_patch
from bs4 import BeautifulSoup
import re
from fpdf import FPDF, HTMLMixin

# This code is mainly for reading and outputing files

# TODO: Try to solve the problem of double newlines when reading word documents


class MyFPDF(FPDF, HTMLMixin):
    pass

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
        ('All Files', '.docx .pdf .txt'),
        ('Word Documents', '.docx'),
        ('Adobe PDF', '.pdf')])

    if file is None:
        return

    if file.name.lower().endswith(('.doc', '.docx')):
        document = Document()
        p = document.add_paragraph()
        for action, text in diffs:
            font = p.add_run(text).font
            font.size = Pt(14) if action == 0 else Pt(16)
            if highlightOnOff:
                if action == -1:
                    font.strike = strikethroughOnOff
                    font.color.rgb = RGBColor(255, 0, 0)
                elif action == 1:
                    font.underline = underlineOnOff
                    font.color.rgb = RGBColor(0, 0, 255)
        document.save(file.name)
    elif file.name.lower().endswith('.pdf'):
        dmp = diff_match_patch()
        diff = dmp.diff_prettyHtml(diffs)
        diff_new_html = HTMLstyle(
            diff, underlineOnOff, strikethroughOnOff, highlightOnOff, paragraphMarkOnOff)

        pdf = MyFPDF()
        pdf.add_page()
        pdf.write_html(diff_new_html)
        pdf.output(file.name, 'F')
    else:
        with open(file.name, 'w', encoding='utf-8') as f:
            f.write(''.join([word for _, word in diffs]))

    print('file:', file)
    print('file.name:', file.name)
    file.close()


# Change HTML style
def HTMLstyle(old_html, underlineOnOff, strikethroughOnOff, highlightOnOff, paragraphMarkOnOff):
    soup = BeautifulSoup(old_html, 'html.parser')
    while True:
        old_tag = soup.find('del')
        if not old_tag:
            break
        old_tag['style'] = 'background:#FFAAAA' if highlightOnOff else ''
        if not strikethroughOnOff:
            old_tag.name = 'span'

    while True:
        old_tag = soup.find('ins')
        if not old_tag:
            break
        old_tag['style'] = 'background:#AAFFAA' if highlightOnOff else ''
        if not underlineOnOff:
            old_tag.name = 'span'

    # Remove '¶' if paragraph mark is off
    while True:
        mark_span_tag = soup.find('span')
        mark_ins_tag = soup.find('ins')
        mark_del_tag = soup.find('del')
        if not mark_span_tag and not mark_ins_tag and not mark_del_tag:
            break
        if not underlineOnOff:
            if mark_span_tag:
                mark_span_tag.string = mark_span_tag.string.replace('¶', '')
            if mark_ins_tag:
                mark_ins_tag.string = mark_ins_tag.string.replace('¶', '')
            if mark_del_tag:
                mark_del_tag.string = mark_del_tag.string.replace('¶', '')

    return str(soup)


def test_function():
    print("test function!!")


# TODO: Try to access files
