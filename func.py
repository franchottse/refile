import os
import textract
import tkinter as tk
from tkinter import filedialog, Text

# This code is mainly for showing files

# TODO: Try to solve the problem of double newlines when reading word documents

# Read file


def readFile(path):
    if not os.path.exists(path):
        return ''
    _, ext = os.path.splitext(path)

    txt = ''
    if path.lower().endswith(('.doc', '.docx', '.pdf')):
        txt = textract.process(path, language=ext[1:]).replace(
            b'\n\n', b'\n').decode('utf-8')
    else:
        f = open(path, 'r', encoding='utf-8')
        txt = f.read()
    return txt

# Export file


def exportFile(text_box):
    file = filedialog.asksaveasfile(initialdir='/', initialfile='Output.docx', defaultextension='*.*', filetypes=[
        ('All Files', '.doc .docx .txt .pdf'),
        ('Word Documents', '.doc .docx'),
        ('Adobe PDF', '.pdf')])
    if file is None:
        return
    print('text_box.get(1.0, tk.END):', text_box.get(1.0, tk.END))
    print('type(text_box.get(1.0, tk.END)):', type(text_box.get(1.0, tk.END)))
    output_text = text_box.get(1.0, tk.END)

    print('file:', file)
    print('file.name:', file.name)
    with open(file.name, 'w', encoding='utf-8') as f:
        f.write(output_text)
    file.close()


def test_function():
    print("test function!!")


# TODO: Try to access files
