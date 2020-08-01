import os
import textract

# This code is mainly for showing files

# TODO: Try to solve the problem of double newlines when reading word documents


def readFile(path):
    _, ext = os.path.splitext(path)

    txt = ''
    if path.lower().endswith(('.doc', '.docx', '.pdf')):
        txt = textract.process(path, language=ext[1:]).replace(
            b'\n\n', b'\n').decode('utf-8').replace('\n', '¶\n')
    else:
        f = open(path, 'r', encoding='utf-8')
        txt = f.read()
    print('type(txt):', type(txt))
    print(txt)


def test_function():
    print("test function!!")


if __name__ == '__main__':
    readFile('C:/Users/tsezg523/Desktop/ReFile_test_files/化妝用品.pdf')

# TODO: Try to access files
