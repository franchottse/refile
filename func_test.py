import xlwt
import csv
import os
import pandas as pd
from pandas import ExcelWriter
from openpyxl import load_workbook

file = r"C:\Users\tsezg523\Desktop\test_file.xlsx"
xls = pd.ExcelFile(file)
data1 = pd.read_excel(xls, 'Sheet1')
data2 = pd.read_excel(xls, 'Sheet2')
# df = pd.DataFrame(data, columns=['Product'])
print("First output:", data1)

# Show the column Product only for the first row
print("Second output:", data1['Price'].iloc[0])

# Modify the data from the column Product for the first row
data1.iloc[0, data1.columns.get_loc('Price')] = 500
print("Third output:", data1)


print("Forth output:", data2)

# Print sheet names
print("Sheet names:", xls.sheet_names)

# Generate a dictionary of DataFrames
dfs = {sh: xls.parse(sh) for sh in xls.sheet_names}
print("new:", dfs.keys())
# Print all sheets
for df in dfs:
    print(dfs[df])

# TODO: fix the ExcelWriter instantiate problem
# Try to write new data into the same excel file
# writer = pd.ExcelWriter(file, engine = 'xlsxwriter')
# Modify one of the data before writing back to the file
# data1.to_excel(writer, sheet_name = 'Sheet1', index = False, header = True)
# writer.save()
# writer.close()
