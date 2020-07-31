import os
import textract

# This code is mainly for showing files

# TODO: Try to solve the problem of double newlines when reading word documents
def readFile(path):
    _, ext = os.path.splitext(path)

    txt = ''
    if path.lower().endswith(('.doc', '.docx', '.pdf')):
        txt = textract.process(path, language=ext[1:]).decode('utf-8')
    else:
        f = open(path, 'r', encoding='utf-8')
        txt = f.read()
    print('type(txt):', type(txt))
    print(txt)

def test_function():
    print("test function!!")

if __name__ == '__main__':
    print('testwordfile1.pdf:')
    readFile('C:/Users/tsezg523/Desktop/testwordfile1.pdf')
    print('testwordfile2.pdf:')
    readFile('C:/Users/tsezg523/Desktop/testwordfile2.pdf')
    print('testwordengfile1.pdf:')
    readFile('C:/Users/tsezg523/Desktop/testwordengfile1.pdf')
    print('testwordengfile2.pdf:')
    readFile('C:/Users/tsezg523/Desktop/testwordengfile2.pdf')

# TODO: Try to access files
