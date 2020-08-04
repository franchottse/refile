import os
import textract

# This code is mainly for showing files

# TODO: Try to solve the problem of double newlines when reading word documents


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


def test_function():
    print("test function!!")


# TODO: Try to access files
