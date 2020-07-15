import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk, Menu
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

    # TODO: Beautify the layout of the GUI
    def configureGUI(self):
        # App title
        self.master.winfo_toplevel().title('ReFile')
        self.master.minsize(640, 480)

        # Menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Open File', command=self.addFile)
        self.subMenu.add_separator()
        self.subMenu.add_command(label='Exit', command=self.master.destroy)

        # Create a canvas
        self.canvas = tk.Canvas(self.master, height=700,
                                width=1200, bg='#ACBFC9')

        # Create a frame for displaying data
        self.dataFrame = tk.Frame(self.master)
        self.dataFrame.place(relwidth=0.6, relheight=0.6, relx=0.3, rely=0.1)
        self.dataLabel = tk.Label(self.dataFrame, text='Data', bg='#18EBA0')

        # Test tree view
        cols = ('Position', 'Name', 'Score',
                'Random Stuff', 'Another Random Stuff')
        self.listBox = ttk.Treeview(
            self.dataFrame, columns=cols, show='headings', selectmode=tk.BROWSE)
        # set column headings
        for col in cols:
            self.listBox.column(col)
            self.listBox.heading(col, text=col)

        self.verticalScrollBar = ttk.Scrollbar(
            self.dataFrame, orient=tk.VERTICAL, command=self.listBox.yview)

        self.HorizontalScrollBar = ttk.Scrollbar(
            self.dataFrame, orient=tk.HORIZONTAL, command=self.listBox.xview)

        self.sizegrip = ttk.Sizegrip(self.dataFrame)

        self.listBox.configure(xscrollcommand=self.HorizontalScrollBar.set,
                               yscrollcommand=self.verticalScrollBar.set)

        # End of test tree view

        # Create a frame for displaying files
        self.fileFrame = tk.Frame(self.master, bg='#20313A')
        self.fileFrame.place(relwidth=0.8, relheight=0.2, relx=0.1, rely=0.7)
        self.fileLabel = tk.Label(self.fileFrame, text='Files', bg='#18EBA0')
        # self.fileLabel.grid(column=1, row=0, sticky='NSWE')

        # Create a frame for displaying check boxes
        self.checkBoxFrame = tk.Frame(self.master, bg='#172A33')
        self.checkBoxFrame.place(
            relwidth=0.2, relheight=0.6, relx=0.1, rely=0.1)
        self.checkBoxLabel = tk.Label(
            self.checkBoxFrame, text='Columns', bg='#18EBA0')

        # Pack everything
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.dataLabel.pack(padx=0.5, pady=0.1, fill=tk.X)
        self.HorizontalScrollBar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.verticalScrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)
        self.sizegrip.pack(in_=self.HorizontalScrollBar,
                           side=tk.BOTTOM, anchor=tk.S+tk.E)
        self.listBox.pack(fill=tk.BOTH, expand=True)
        self.fileLabel.pack(padx=0.5, pady=0.1)
        self.checkBoxLabel.pack(padx=0.1, pady=0.1)

    def createWidgets(self):
        # Create an select files button
        buttonStyle = {'padx': '10', 'pady': '5', 'fg': '#18EBA0', 'bg': '#20313A',
                       'activebackground': '#172A33', 'activeforeground': '#18EBA0', 'bd': '2'}
        self.openFile = tk.Button(
            self.master, text='Select File', **buttonStyle, command=self.addFile)
        self.openFile.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

        # Test button
        tk.Button(self.master, text="Show scores", **buttonStyle,
                  command=self.show).place(relx=0.6, rely=0.95, anchor=tk.CENTER)

    # Demo function
    def show(self):
        tempList = [['Jim', '0.33', 'What', 'Hello'], ['Dave', '0.67', 'is', ''],
                    ['James', '0.67', 'Tkinter', 'World'], ['Eden', '0.5', '?', '']]
        # tempList.sort(key=lambda e: e[1], reverse=True)

        for i, (name, score, stuff, stuff1) in enumerate(tempList, start=1):
            self.listBox.insert("", "end", values=(
                i, name, score, stuff, stuff1))
    # End of demo function

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
