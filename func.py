import openpyxl
import tkinter as tk
from openpyxl import load_workbook
from openpyxl.utils.exceptions import ReadOnlyWorkbookException
from tkinter import filedialog, Text, scrolledtext, messagebox

# This code is mainly for modifying or showing Excel files

# file = r"C:\Users\tsezg523\Desktop\testfile.xlsx"

# wbs = load_workbook(file, read_only=False)
# ws1 = wbs["Sheet1"]


def test_function():
    print("test function!!")


# Print cells in the terminal
def printCell(sheet):
    max_row = sheet.max_row
    max_col = sheet.max_column
    for i in range(1, max_row+1):
        # iterate over all columns
        for j in range(1, max_col+1):
            # get particular cell value
            cell_obj = sheet.cell(row=i, column=j)
            # print cell value
            print(cell_obj.value, end='')
            if j != max_col:
                print(' | ', end='')
        # print new line
        print('\n')

# TODO: Try to access Excel files
