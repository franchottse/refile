import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os
import func


class ReFile(tk.Frame):

    def __init__(self, master):
        self.xlFiles = []
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configureGUI()
        self.createWidgets()
        self.loadSavedList()
        self.displayFiles()

    def test_func(self):
        func.test_function()

    # TODO: Fix the background colour resizing problem
    def configureGUI(self):
        # App title
        self.master.winfo_toplevel().title('ReFile')

        # Create a canvas
        self.canvas = tk.Canvas(self.master, height=700,
                                width=1200, bg='#87CEEB')
        self.canvas.grid(sticky='NSWE')
        self.canvas.place()

        # Create a frame for displaying files
        self.fileFrame = tk.Frame(self.master, bg='white')
        self.fileFrame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        self.fileLabel = tk.Label(self.fileFrame, text='Files', bg='#EBA687')
        self.fileLabel.grid(column=1, row=0, sticky='NSWE')
        self.fileLabel.pack(padx=0.5, pady=0.1)

    def createWidgets(self):
        # Create an select files button
        self.openFile = tk.Button(self.master, text='Select File', padx=10,
                                  pady=5, fg='white', bg='#263D42', bd=2, command=self.addFile)
        self.openFile.grid()
        self.openFile.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    def isFile(self):
        if os.path.isfile('xlList.txt'):
            with open('xlList.txt', 'r') as f:
                tempFiles = f.read()
                print(tempFiles)
            return True
        return False

    def loadSavedList(self):
        if os.path.isfile('xlList.txt'):
            with open('xlList.txt', 'r') as f:
                tempFiles = f.read()
                tempFiles = tempFiles.split('\n')
                self.xlFiles = [x for x in tempFiles if x.strip()]
                print('File list:', self.xlFiles)

    def displayFiles(self):
        print(self.xlFiles)
        for xlFile in self.xlFiles:
            label = tk.Label(self.fileFrame, text=xlFile, bg='#EBD987')
            # label.place(relx=0.5, rely=0.1)
            label.pack(padx=0.5, pady=0.1)

    def addFile(self):
        xlFile = filedialog.askopenfilename(initialdir='/', title='Select File',
                                            filetypes=[('Excel Files', '.xlsx')])

        if xlFile not in self.xlFiles and xlFile != '':
            self.xlFiles.append(xlFile)
            print('New file: '+xlFile)
        elif xlFile in self.xlFiles:
            messagebox.showinfo(
                'Information', 'You have added this file.')

        for widget in self.fileFrame.winfo_children():
            # print(widget.cget('text'))
            if isinstance(widget, tk.Label) and widget.cget('text') != 'Files':
                widget.destroy()

        self.displayFiles()

    # TODO: Solve the problem of passing arguments to other python files for Excel files


if __name__ == '__main__':
    root = tk.Tk()
    # xlFiles = []
    mainApp = ReFile(root)
    '''if not mainApp.isFile():
        messagebox.showinfo(
            'Information', 'You do not have the previous saved list, please select a file in order to read files')'''
    mainApp.test_func()
    root.mainloop()

    with open('xlList.txt', 'w') as f:
        for xlFile in mainApp.xlFiles:
            f.write(xlFile + '\n')
