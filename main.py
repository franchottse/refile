import tkinter as tk
from tkinter import filedialog, Text, messagebox
import os
import func


class ReFile(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

    def test_func(self):
        func.test_function()

    def configure_gui(self):
        # App title
        self.master.winfo_toplevel().title('ReFile')

        # Create a canvas
        canvas = tk.Canvas(self.master, height=700, width=1200, bg="#87CEEB")
        canvas.grid(sticky='NSWE')

        # Create a frame for displaying files
        fileFrame = tk.Frame(self.master, bg="white")
        fileFrame.place(relwidth=0.8, relheight=0.8, relx=0.1, rely=0.1)
        fileLabel = tk.Label(fileFrame, text="Files", bg="#EBA687")
        fileLabel.grid(column=1, row=0, sticky='NSWE')
        fileLabel.place(relx=0.5)

    # TODO: Solve the problem of passing arguments to other python files
    def create_widgets(self):
        '''openFile = tk.Button(self.master, text="Open File", padx=10,
                             pady=5, fg="white", bg="#263D42", bd=2, command=addFile)
        openFile.grid()
        openFile.place(relx=0.43, rely=0.9)'''
        return

    def isFile(self):
        if os.path.isfile('xlList.txt'):
            with open('xlList.txt', 'r') as f:
                tempFiles = f.read()
                print(tempFiles)
            return True
        return False


if __name__ == '__main__':
    root = tk.Tk()
    xlFlies = []
    mainApp = ReFile(root)
    if not mainApp.isFile():
        messagebox.showinfo(
            'Information', 'You do not have the previous saved list, please select a file in order to read files')
    mainApp.test_func()
    root.mainloop()
