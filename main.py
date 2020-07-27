import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk, Menu
from PIL import Image, ImageTk
import os
import func

class ReFile(tk.Frame):

    def __init__(self, master):
        self.xlFiles = []
        self.master = master
        super().__init__()
        #tk.Frame.__init__(self, self.master)
        self.master.bind('<Delete>', self.deleteFile)

        # Style setup
        self.width = 1200
        self.height = 700
        self.xPosition = (self.master.winfo_screenwidth() // 2) - (self.width // 2)
        self.yPosition = (self.master.winfo_screenheight() // 2) - (self.height // 2)
        self.style = ttk.Style(self.master) 
        #self.style.theme_use('clam')
        self.fileHighlightColour = 'grey'
        self.fileHoverColour = 'orange'
        self.filePressColour = '#ED5903'
        self.fileBackgroundColour = '#EBD987'
        self.labelColour = 'white'
        self.style.configure('TFrame', background="#B5ACA8", padding=5)
        self.style.configure('Wild.TButton', background='white', foreground='black', font=('Helvetica', 13))
        #buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.style.map('Wild.TButton', foreground = [('active', 'black'),
                                                     ('pressed', 'black'),
                                                     ('disabled', 'grey')],
                                       background = [('active', 'orange'),
                                                     ('pressed', '!disabled', '#ED5903'),
                                                     ('disabled', 'white')])
        #self.style.configure("TEST.TLabel", foreground='white', background='black', font=(10))
        self.style.configure('Tab.TLabel', background='white', font=('Helvetica', '11', 'bold'), relief=tk.SOLID, anchor=tk.CENTER)
        self.style.configure('File.TLabel', background=self.fileBackgroundColour, font=('Helvetica', 10))
        self.style.configure('Status.TLabel', background='white', highlightbackground='#ED5903', font=('Helvetica', 13), relief=tk.SOLID, anchor=tk.CENTER)

        # Variable to avoid packing file scrollbar repeatedly
        self.initializing = True

        # Variables to save the selected file(s) by the user
        self.selectedFile = ''
        self.selectedMultiFiles = []

        # Test variable to save the file label
        self.fileLabelList = []

        # App setup
        self.configureGUI()
        self.createWidgets()
        self.loadSavedList()
        self.displayFiles()
        self.initializing = False
        self.onFileListFrameResizing()

    # TODO: Beautify the layout of the GUI
    def configureGUI(self):
        # App title & configuration
        self.master.winfo_toplevel().title('ReFile')
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.xPosition, self.yPosition))
        self.master.configure(bg='skyblue')
        self.master.minsize(690, 690)

        # Excel file icon
        self.xlsIcon = ImageTk.PhotoImage(Image.open('./excel.png').resize((100, 100), Image.ANTIALIAS))

        # Menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Open File', command=self.addFile)
        self.subMenu.add_separator()
        self.subMenu.add_command(label='Exit', command=self.onClosingWindow)

        self.helpMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(label='About')

        # Configure grids
        tk.Grid.rowconfigure(self.master, 0, weight=2)
        tk.Grid.rowconfigure(self.master, 1, weight=1)
        tk.Grid.columnconfigure(self.master, (1, 2), weight=1)
        self.master.grid_columnconfigure(0, minsize=280)
        self.master.grid_rowconfigure(1, minsize=200)

        # Create frame for displaying data
        self.dataFrame = ttk.Frame(self.master)
        #self.dataLabel = tk.Label(self.dataFrame, text='Data', bg='white')
        self.dataLabel = ttk.Label(self.dataFrame, text='Data', style='Tab.TLabel')
        self.dataFieldLabel = ttk.Label(self.dataFrame, style='Tab.TLabel')

        # Test tree view
        cols = ('Position', 'Name', 'Score',
                'Random Stuff', 'Another Random Stuff')
        self.dataBox = ttk.Treeview(
            self.dataFieldLabel, columns=cols, show='headings', selectmode=tk.BROWSE)
        # set column headings
        for col in cols:
            self.dataBox.column(col)
            self.dataBox.heading(col, text=col)

        self.verticalScrollBar = ttk.Scrollbar(
            self.dataFrame, orient=tk.VERTICAL, command=self.dataBox.yview)

        self.horizontalScrollBar = ttk.Scrollbar(
            self.dataFrame, orient=tk.HORIZONTAL, command=self.dataBox.xview)

        self.sizegrip = ttk.Sizegrip(self.dataFrame)

        self.dataBox.configure(xscrollcommand=self.horizontalScrollBar.set,
                               yscrollcommand=self.verticalScrollBar.set)

        # TODO: Fix showing row colour problem
        self.dataBox.tag_configure('oddrow', background=self.fileHoverColour)

        # End of test tree view

        # Create a frame for displaying files
        self.fileFrame = ttk.Frame(self.master)
        self.fileLabel = ttk.Label(self.fileFrame, text='Files', style='Tab.TLabel')
        self.fileListCanvas = tk.Canvas(self.fileFrame, highlightthickness=0, background='white')
        self.fileListFrame = ttk.Frame(self.fileListCanvas)
        self.fileScrollBar = ttk.Scrollbar(self.fileFrame, orient=tk.HORIZONTAL, command=self.fileListCanvas.xview)
        self.fileListCanvas.configure(xscrollcommand=self.fileScrollBar.set)

        self.fileCanvasFrame = self.fileListCanvas.create_window((0, 0), window=self.fileListFrame, anchor=tk.W)
        self.fileListFrame.bind('<Configure>', self.onFileListFrameResizing)
        self.fileListCanvas.bind('<Configure>', self.onFileListCanvasResizing)

        # Bind fileListCanvas with addFile function
        self.fileListFrame.bind('<Double-ButtonRelease-1>', self.addFile)
        self.fileListCanvas.bind('<Double-ButtonRelease-1>', self.addFile)

        # TODO: Add three sections for sheets, columns and showing selected columns only
        # Create a frame for displaying check boxes
        self.checkBoxFrame = ttk.Frame(self.master)
        self.checkBoxLabel = ttk.Label(self.checkBoxFrame, text='Columns', style='Tab.TLabel')
        self.checkBoxFieldLabel = ttk.Label(self.checkBoxFrame, background='white', style='Tab.TLabel')

        # Button configuration
        #buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.buttonFrame = tk.Frame(self.master, bg='#B5ACA8')

        # Select File button
        self.openFile = ttk.Button(
            self.buttonFrame, text='Select File', style='Wild.TButton', command=self.addFile)

        # Clear File button
        self.clearFile = ttk.Button(self.buttonFrame, text='Clear All Files', style='Wild.TButton', command=self.clearAllFiles)

        # Reference frames
        self.statusFrame = ttk.Frame(self.master)
        self.statusLabel = ttk.Label(self.statusFrame, text='Welcome to ReFile! Please double click the file area or click Select File to add files', style='Status.TLabel')

    # Pack and grid everything
    def createWidgets(self):
        # Check box, data and file frames
        self.checkBoxFrame.grid(row=0, column=0, padx=10,
                                pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.dataFrame.grid(row=0, column=1, columnspan=2, padx=10,
                            pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.fileFrame.grid(row=1, column=0, columnspan=3, padx=10,
                            pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        self.dataLabel.pack(padx=5, pady=5, fill=tk.X)
        self.fileLabel.pack(padx=5, pady=5, fill=tk.X)
        self.fileListCanvas.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        #self.fileScrollBar.pack(padx=5, pady=(0, 5), side=tk.BOTTOM, fill=tk.X)

        # Treeview in data frame
        self.horizontalScrollBar.pack(side=tk.BOTTOM, fill=tk.X, padx=(0, 17))
        self.verticalScrollBar.pack(side=tk.RIGHT, fill=tk.Y)

        #self.sizegrip.pack(in_=self.horizontalScrollBar, anchor=tk.S+tk.E)
        self.dataFieldLabel.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
        self.dataBox.pack(fill=tk.BOTH, expand=True)

        self.checkBoxLabel.pack(padx=5, pady=5, fill=tk.X)
        self.checkBoxFieldLabel.pack(padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)

        # Button frame
        self.buttonFrame.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # Status bar
        self.statusFrame.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.statusLabel.pack(fill=tk.BOTH, expand=True)

        
        self.openFile.grid(row=0, column=0, padx=5, pady=5)
        #self.openFile.pack(padx=5, pady=5, anchor=tk.CENTER, side=tk.LEFT)

        # Test button, Clear files button
        #tk.Button(self.buttonFrame, text="Show scores", **buttonStyle,command=self.show).grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.clearFile.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

    def test_func(self):
        func.test_function()

    # Make sure the scrollbar works for the file list frame
    def onFileListFrameResizing(self, event=None):
        self.fileListCanvas.configure(scrollregion=self.fileListCanvas.bbox(tk.ALL))
        self.checkFilelistCanvasFrame()

    # Keep file list frame remaining the same size
    def onFileListCanvasResizing(self, event=None):
        if event != None:
            self.fileListCanvas.itemconfig(self.fileCanvasFrame, height=event.height)
        self.checkFilelistCanvasFrame()

    # Make the file scrollbar visible depending on file list frame size and file list canvas size
    def checkFilelistCanvasFrame(self):
        if not self.initializing:
            if self.fileScrollBar.winfo_ismapped() and self.fileListFrame.winfo_width() <= self.fileListCanvas.winfo_width():
                self.fileScrollBar.pack_forget()
            if not self.fileScrollBar.winfo_ismapped() and self.fileListFrame.winfo_width() > self.fileListCanvas.winfo_width():
                self.fileScrollBar.pack(padx=5, pady=(0, 5), side=tk.BOTTOM, fill=tk.X)

    # Enter event for files
    def onEntering(self, event):
        if event.widget.cget('state') != 'DISABLED':
            event.widget.config(background=self.fileHoverColour)
            for child in event.widget.winfo_children():
                child.config(background=self.fileHoverColour)

    # Leave event for files
    def onLeaving(self, event):
        if event.widget.cget('state') != 'DISABLED':
            event.widget.config(background=self.fileBackgroundColour)
            for child in event.widget.winfo_children():
                child.config(background=self.fileBackgroundColour)

    # Mouse hold event for files
    def onPressing(self, event, outLabel):
        if outLabel.cget('state') != 'DISABLED':
            outLabel.config(background=self.filePressColour)
            for child in outLabel.winfo_children():
                child.config(background=self.filePressColour)

    # Mouse release event for highlighting a file when clicked
    def onReleasing(self, event, outLabel, filename):
        if outLabel.cget('state') != 'DISABLED':
            for widget in self.fileLabelList:
                if widget.cget('state') == 'DISABLED':
                    widget.config(background=self.fileBackgroundColour, state='NORMAL')
                    for child in widget.winfo_children():
                        child.config(background=self.fileBackgroundColour)

            print('filename:', filename)
            self.selectedFile = filename
            self.statusLabel['text'] = os.path.basename(filename) + ' selected.'
            outLabel.config(background='grey', state='DISABLED')
            for child in outLabel.winfo_children():
                child.config(background='grey')

    # Mouse double click event for opening a file
    def onDoubleClicking(self, event, filename):
        try:
            self.statusLabel['text'] = 'Opening file: ' + os.path.basename(filename) + '.'
            os.startfile(filename)
        except:
            print('Some error.')
            tk.messagebox.showerror(title='ReFile', message='Error: the file you are opening may be deleted, unknown or corrupted.')
            self.statusLabel['text'] = 'Error: the file you are opening may be deleted, unknown or corrupted.'

    # Close window event
    def onClosingWindow(self):
        self.statusLabel['text'] = 'Leaving ReFile'
        if messagebox.askokcancel('ReFile', 'Are you sure you want to close the window?'):
            self.master.destroy()
        else:
            self.statusLabel['text'] = ''

    def deleteFile(self, event=None):
        if self.selectedFile == '':
            return

        # Find target widget and file name to remove from file label list and xlFiles
        for label in self.fileLabelList:
            if label.cget('state') == 'DISABLED':
                self.fileLabelList.remove(label)
                self.xlFiles.remove(self.selectedFile)

        # Destroy widget from GUI
        for outLabel in self.fileListFrame.winfo_children():
            for widget in outLabel.winfo_children():
                if isinstance(widget, ttk.Label) and widget.cget('text') == self.selectedFile:
                    outLabel.destroy()
                    self.statusLabel['text'] = os.path.basename(self.selectedFile) + ' deleted.'
                    self.selectedFile = ''
                    if not self.fileListFrame.winfo_children():
                        self.master.update()
                        self.fileListFrame.config(width=1)

    # Test function for selecting some files to delete
    def selectMultiFiles(self, event=None):
        if not event.widget.cget('text') in self.selectedMultiFiles:
            self.selectedMultiFiles.append(event.widget.cget('text'))
            self.statusLabel['text'] = str(len(self.selectedMultiFiles)) + ' file(s) selected.'

    # Demo function with clear all files ability
    def clearAllFiles(self):
        if self.xlFiles and not messagebox.askyesno('ReFile', 'Do you really want to delete all files?'):
            return
        self.xlFiles.clear()
        print('Before clearing in clearAllFiles:', self.fileLabelList)
        self.fileLabelList.clear()
        print('After clearing in clearAllFiles:', self.fileLabelList)
        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        # Make the file list frame resize when deleting files
        self.master.update()
        self.fileListFrame.config(width=1)

        tempList = [
            ['Jim', '0.33', 'What', 'Hello'],
            ['Dave', '0.67', 'is', ''],
            ['James', '0.67', 'Tkinter', 'World'],
            ['Eden', '0.5', '?', '']
            ]
        # tempList.sort(key=lambda e: e[1], reverse=True)

        for i, (name, score, stuff, stuff1) in enumerate(tempList, start=1):
            self.dataBox.insert('', 'end', values=(
                i, name, score, stuff, stuff1), tags = 'oddrow' if i%2 == 1 else '')
    # End of demo function

    def isFile(self):
        if os.path.isfile('xlList.txt'):
            with open('xlList.txt', 'r') as f:
                tempFiles = f.read()
                print(tempFiles)
            return True
        return False

    def loadSavedList(self):
        self.statusLabel['text'] = 'Loading previous saved list'
        if os.path.isfile('xlList.txt'):
            with open('xlList.txt', 'r') as f:
                tempFiles = f.read()
                tempFiles = tempFiles.split('\n')
                self.xlFiles = [x for x in tempFiles if x.strip()]
                print('File list:', self.xlFiles)
        self.statusLabel['text'] = 'Welcome to ReFile! Please double click the file area or click Select File to add files.'

    # TODO: Display data from a file when clicked
    def displayData(self):
        pass

    # TODO: Display check boxes from a file when clicked
    def displayCheckBoxes(self):
        pass

    def displayFiles(self):
        print('File list:', self.xlFiles)
        for xlFile in self.xlFiles:
            label = ttk.Label(self.fileListFrame, style='File.TLabel')
            # don't forget to add "Icon made by Pixel perfect from www.flaticon.com" for this project
            imageCanvas = tk.Canvas(label, width=100, height=100, highlightthickness=0)
            textLabel = ttk.Label(label, text=xlFile, style='File.TLabel')
            self.fileLabelList.append(label)

            if xlFile == self.selectedFile:
                label.config(background='grey', state='DISABLED')
                for child in label.winfo_children():
                    child.config(background='grey')

            # Bind label with onEntering
            label.bind('<Enter>', self.onEntering)

            # Bind label with onLeaving
            label.bind('<Leave>', self.onLeaving)

            # Bind label, imageCanvas and textLabel with onPressing
            label.bind('<ButtonPress-1>', lambda event, outLabel=label: self.onPressing(event, outLabel))
            imageCanvas.bind('<ButtonPress-1>', lambda event, outLabel=label: self.onPressing(event, outLabel))
            textLabel.bind('<ButtonPress-1>', lambda event, outLabel=label: self.onPressing(event, outLabel))

            # Bind label, imageCanvas and textLabel with onReleasing
            label.bind('<ButtonRelease-1>', lambda event, outLabel=label, filename=xlFile: self.onReleasing(event, outLabel, filename))
            imageCanvas.bind('<ButtonRelease-1>', lambda event, outLabel=label, filename=xlFile: self.onReleasing(event, outLabel, filename))
            textLabel.bind('<ButtonRelease-1>', lambda event, outLabel=label, filename=xlFile: self.onReleasing(event, outLabel, filename))

            # Bind label, imageCanvas and textLabel with onDoubleClicking
            label.bind('<Double-Button-1>', lambda event, filename=xlFile: self.onDoubleClicking(event, filename))
            imageCanvas.bind('<Double-Button-1>', lambda event, filename=xlFile: self.onDoubleClicking(event, filename))
            textLabel.bind('<Double-Button-1>', lambda event, filename=xlFile: self.onDoubleClicking(event, filename))

            #label.bind('<Control-ButtonRelease-1>', self.selectMultiFiles)
            label.pack(padx=5, pady=5, side=tk.LEFT)
            imageCanvas.pack(padx=5, pady=5)
            imageCanvas.create_image((0, 0), anchor=tk.N+tk.W, image=self.xlsIcon)
            textLabel.pack(padx=5, pady=5, fill=tk.BOTH)

        self.master.update()
        self.onFileListFrameResizing()

    def addFile(self, event=None):
        self.openFile.state(['disabled'])
        self.clearFile.state(['disabled'])
        self.statusLabel['text'] = 'Selecting files'
        files = filedialog.askopenfilenames(initialdir='/', title='Select File',
                                            filetypes=[('Excel Files', '.xlsx')])

        for file in files:
            if file not in self.xlFiles and file != '':
                self.xlFiles.append(file)
                #self.statusLabel['text'] = 'Added new file: ' + os.path.basename(file)
                print('New file: ' + file)
            elif file in self.xlFiles:
                #self.statusLabel['text'] = 'There is at least a file added before.'
                self.statusLabel['text'] = 'There is at least a file added before.'
                messagebox.showinfo('ReFile', 'There is at least a file added before.')
                self.addFile()
                break

        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        self.fileLabelList.clear()
        self.openFile.state(['!disabled'])
        self.clearFile.state(['!disabled'])
        self.statusLabel['text'] = 'Complete!'
        self.displayFiles()

    # TODO: Solve the problem of passing arguments to other python files for Excel files


if __name__ == '__main__':
    root = tk.Tk()
    mainApp = ReFile(root)
    mainApp.test_func()
    root.protocol('WM_DELETE_WINDOW', mainApp.onClosingWindow)
    #mainApp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

    with open('xlList.txt', 'w') as f:
        for xlFile in mainApp.xlFiles:
            f.write(xlFile + '\n')
