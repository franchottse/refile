import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk, Menu
import os
import func

class ReFile(tk.Frame):

    def __init__(self, master):
        self.xlFiles = []
        self.master = master
        #super().__init__('clam')
        tk.Frame.__init__(self, self.master)
        
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

        # App setup
        self.configureGUI()
        self.createWidgets()
        self.loadSavedList()
        self.displayFiles()

    def test_func(self):
        func.test_function()

    # TODO: Beautify the layout of the GUI
    def configureGUI(self):
        # App title & configuration
        self.master.winfo_toplevel().title('ReFile')
        self.master.geometry('{}x{}+{}+{}'.format(self.width, self.height, self.xPosition, self.yPosition))
        self.master.configure(bg='skyblue')
        self.master.minsize(690, 690)

        # Menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        self.subMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.subMenu)
        self.subMenu.add_command(label='Open File', command=self.addFile)
        self.subMenu.add_separator()
        self.subMenu.add_command(label='Exit', command=self.onClosing)

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
        self.fileListCanvas = tk.Canvas(self.fileFrame, background='white')
        self.fileListFrame = ttk.Frame(self.fileListCanvas)
        self.fileScrollBar = ttk.Scrollbar(self.fileFrame, orient=tk.HORIZONTAL, command=self.fileListCanvas.xview)
        self.fileListCanvas.configure(xscrollcommand=self.fileScrollBar.set)

        self.fileCanvasFrame = self.fileListCanvas.create_window((0, 0), window=self.fileListFrame, height=150, anchor=tk.W)
        self.fileListFrame.bind('<Configure>', lambda e: self.fileListCanvas.configure(scrollregion=self.fileListCanvas.bbox('all')))
        self.fileListCanvas.bind('<Configure>', self.onFileListFrameResizing)

        # Bind fileListCanvas with addFile function
        self.fileListFrame.bind('<Double-ButtonRelease-1>', self.addFile)
        self.fileListCanvas.bind('<Double-ButtonRelease-1>', self.addFile)

        # TODO: Add two sections for sheets and columns
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
        self.clearFile = ttk.Button(self.buttonFrame, text='Clear All Files', style='Wild.TButton', command=self.show)

        # Reference frames
        self.statusFrame = ttk.Frame(self.master)
        self.statusLabel = ttk.Label(self.statusFrame, text='Welcome to ReFile! Please double click the file area or click Select File to add files', style='Status.TLabel')

    # TODO: Fix the problem of not showing entire fileListFrame when opening window initially
    def onFileListFrameResizing(self, event=None):
        #print('self.fileListFrame.winfo_width(): ', str(self.fileListFrame.winfo_width())+', self.fileListCanvas.winfo_width(): ', self.fileListCanvas.winfo_width())
        #print('self.fileListCanvas.winfo_rootx(self.fileCanvasFrame):', str(self.fileListCanvas.coords(self.fileCanvasFrame))+', self.fileListCanvas.winfo_rooty(self.fileCanvasFrame):', self.fileListCanvas.coords(self.fileCanvasFrame))
        if event != None:
            print('event:', event)
            print('self.fileListCanvas', self.fileListCanvas)
            canvasHeight = event.height
            self.fileListCanvas.itemconfig(self.fileCanvasFrame, height=canvasHeight)

        if self.fileListFrame.winfo_width() < self.fileListCanvas.winfo_width():
            self.fileScrollBar.pack_forget()
        else:
            self.fileScrollBar.pack(padx=5, pady=(0, 5), side=tk.BOTTOM, fill=tk.X)

    # Pack everything
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
        #self.fileListCanvas.itemconfig(self.fileCanvasFrame, height=self.fileListCanvas.winfo_height())
        self.fileScrollBar.pack(padx=5, pady=(5, 0), side=tk.BOTTOM, fill=tk.X)

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

    # Demo function with clear all files ability
    def show(self):
        self.xlFiles.clear()
        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        self.master.update()
        self.fileListFrame.config(width=1)
        self.onFileListFrameResizing()

        tempList = [['Jim', '0.33', 'What', 'Hello'], ['Dave', '0.67', 'is', ''],
                    ['James', '0.67', 'Tkinter', 'World'], ['Eden', '0.5', '?', '']]
        # tempList.sort(key=lambda e: e[1], reverse=True)

        for i, (name, score, stuff, stuff1) in enumerate(tempList, start=1):
            self.dataBox.insert('', 'end', values=(
                i, name, score, stuff, stuff1), tags = 'oddrow' if i%2 == 1 else '')
    # End of demo function

    # Close window event
    def onClosing(self):
        self.statusLabel['text'] = 'Leaving ReFile'
        if messagebox.askokcancel('Quit', 'Are you sure you want to close the window?'):
            self.master.destroy()
        else:
            self.statusLabel['text'] = ''

    # Enter event for files
    def onEntering(self, event):
        #if event.widget.cget('background') == self.fileBackgroundColour:
        #print('onEntering triggered')
        event.widget.config(background=self.fileHoverColour)
    
    # Leave event for files
    def onLeaving(self, event):
        #if event.widget.cget('background') == self.fileHoverColour:
        #print('onLeaving triggered')
        event.widget.config(background=self.fileBackgroundColour)

    # Mouse hold event for files
    def onPressing(self, event):
        event.widget.config(background=self.filePressColour)

    # Mouse release event for files
    def onReleasing(self, event):
        event.widget.config(background=self.fileHoverColour)

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
        print(self.fileListCanvas.coords(self.fileCanvasFrame))
        print('File list:', self.xlFiles)
        for xlFile in self.xlFiles:
            frame = tk.Frame(self.fileListFrame, bg='skyblue', height=self.fileListFrame.winfo_height(), width=self.fileListFrame.winfo_width())
            label = ttk.Label(frame, text=xlFile, style='File.TLabel')
            #label.bind('<Button-1>', self.fileHighlighter)
            label.bind('<Enter>', self.onEntering)
            label.bind('<Leave>', self.onLeaving)
            label.bind('<ButtonPress-1>', self.onPressing)
            label.bind('<ButtonRelease-1>', self.releaseHightlight)
            frame.pack(padx=5, pady=5, side=tk.LEFT)
            label.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.BOTH)

        self.master.update()
        self.onFileListFrameResizing()

    # Call two functions when releasing mouse key
    def releaseHightlight(self, event):
        self.onReleasing(event)
        self.fileHighlighter(event)

    # TODO: Fix the problem of how to highlight only one item (on hold)
    # An event to highlight a file when clicked
    def fileHighlighter(self, event):
        '''oldHightlightLabel = ttk.Label()
        for widget in self.fileFrame.winfo_children():
            if isinstance(widget, ttk.Label) and widget.cget('text') != 'Files' and widget.cget('background') == self.fileHighlightColour:
                widget.config(background=self.fileBackgroundColour)
        print('self:', self)
        print('old label:', oldHightlightLabel)
        print('new label:', event.widget)
        #if event.widget != oldHightlightLabel:
            #oldHightlightLabel['background'] = self.fileBackgroundColour
        event.widget.config(background=self.fileHighlightColour)'''
        self.statusLabel['text'] = os.path.basename(event.widget.cget('text')) + ' selected.'

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
                messagebox.showinfo('Information', 'There is at least a file added before.')
                self.addFile()
                break

        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        self.openFile.state(['!disabled'])
        self.clearFile.state(['!disabled'])
        self.statusLabel['text'] = 'Complete!'
        self.displayFiles()

    # TODO: Solve the problem of passing arguments to other python files for Excel files


if __name__ == '__main__':
    root = tk.Tk()
    mainApp = ReFile(root)
    mainApp.test_func()
    root.protocol('WM_DELETE_WINDOW', mainApp.onClosing)
    #mainApp.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    root.mainloop()

    with open('xlList.txt', 'w') as f:
        for xlFile in mainApp.xlFiles:
            f.write(xlFile + '\n')
