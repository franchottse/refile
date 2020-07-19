import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk, Menu
import os
import func


class ReFile(tk.Frame):

    def __init__(self, master):
        self.xlFiles = []
        self.master = master
        tk.Frame.__init__(self, self.master)
        
        # Style setup
        self.style = ttk.Style(self.master) 
        #self.style.theme_use('clam')
        self.style.configure('TFrame', background="#B5ACA8", padding=5)
        self.style.configure('TButton', font =('bold'), borderwidth = '5')
        #buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.style.map('TButton', foreground = [('active', '!disabled', 'black'), ('pressed', 'black')], background = [('active', 'white'), ('pressed', '!disabled', '#F5E7D7')])
        self.fileHighlightColour = 'grey'
        self.fileHoverColour = 'orange'
        self.filePressColour = '#ED5903'
        self.fileBackgroundColour = '#EBD987'
        self.labelColour = 'white'
        
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
        self.master.geometry('1200x700')
        self.master.configure(bg='skyblue')
        self.master.minsize(640, 480)

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
        tk.Grid.rowconfigure(self.master, (0, 1), weight=1)
        tk.Grid.columnconfigure(self.master, (1, 2), weight=1)
        self.master.grid_columnconfigure(0, minsize=280)

        # Create frame for displaying data
        self.dataFrame = ttk.Frame(self.master)
        #self.dataLabel = tk.Label(self.dataFrame, text='Data', bg='white')
        self.dataLabel = ttk.Label(self.dataFrame, text='Data', background=self.labelColour, relief = tk.SOLID, anchor=tk.CENTER)
        self.dataFieldLabel = ttk.Label(self.dataFrame, background='white', relief = tk.SOLID, anchor=tk.CENTER)

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

        self.HorizontalScrollBar = ttk.Scrollbar(
            self.dataFrame, orient=tk.HORIZONTAL, command=self.dataBox.xview)

        self.sizegrip = ttk.Sizegrip(self.dataFrame)

        self.dataBox.configure(xscrollcommand=self.HorizontalScrollBar.set,
                               yscrollcommand=self.verticalScrollBar.set)

        # TODO: Fix showing row colour problem
        self.dataBox.tag_configure('oddrow', background=self.fileHoverColour)

        # End of test tree view

        # Create a frame for displaying files
        self.fileFrame = ttk.Frame(self.master)
        self.fileLabel = ttk.Label(self.fileFrame, text='Files', background=self.labelColour, relief = tk.SOLID, anchor=tk.CENTER)
        self.fileList = tk.Canvas(self.fileFrame, background='white')
        self.fileScrollBar = ttk.Scrollbar(self.fileFrame, orient=tk.HORIZONTAL, command=self.fileList.xview)
        self.fileList.configure(xscrollcommand=self.fileScrollBar.set)

        # TODO: Add two sections for sheets and columns
        # Create a frame for displaying check boxes
        self.checkBoxFrame = ttk.Frame(self.master)
        self.checkBoxLabel = ttk.Label(
            self.checkBoxFrame, text='Columns', background='white', relief = tk.SOLID, anchor=tk.CENTER)
        self.checkBoxFieldLabel = ttk.Label(self.checkBoxFrame, background=self.labelColour, relief = tk.SOLID, anchor=tk.CENTER)

        # Button configuration
        buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.buttonFrame = tk.Frame(self.master, bg='#B5ACA8')

        # Reference frames
        self.statusFrame = tk.Frame(self.master, bg='#B5ACA8')
        self.statusLabel = tk.Label(self.statusFrame, text='Welcome to ReFile! Please double click the file area or click Select File to add files', relief=tk.SOLID)

        # Select File button
        self.openFile = ttk.Button(
            self.buttonFrame, text='Select File', command=self.addFile)

        # Clear File button
        self.clearFile = ttk.Button(self.buttonFrame, text="Clear All Files", command=self.show)

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
        self.fileList.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        self.fileScrollBar.pack(padx=5, pady=5, side=tk.BOTTOM, fill=tk.X, expand=False)

        # Treeview in data frame
        self.HorizontalScrollBar.pack(side=tk.BOTTOM, fill=tk.X, expand=False)
        self.verticalScrollBar.pack(side=tk.RIGHT, fill=tk.Y, expand=False)

        self.sizegrip.pack(in_=self.HorizontalScrollBar,
                           side=tk.BOTTOM, anchor=tk.S+tk.E)
        self.dataBox.pack(fill=tk.BOTH, expand=True)
        self.dataFieldLabel.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)
        

        self.checkBoxLabel.pack(padx=5, pady=5)
        self.checkBoxFieldLabel.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Button frame
        self.buttonFrame.grid(row=2, column=0, padx=10, pady=5)

        # Status bar
        self.statusFrame.grid(row=2, column=1, columnspan=2, padx=10, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.statusLabel.pack(fill=tk.BOTH, expand=True)

        
        self.openFile.grid(row=0, column=0, padx=5, pady=5)
        #self.openFile.pack(padx=5, pady=5, anchor=tk.CENTER, side=tk.LEFT)

        # Test button, Clear files button
        #tk.Button(self.buttonFrame, text="Show scores", **buttonStyle,command=self.show).grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.clearFile.grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # Bind fileFrame with addFile function
        self.fileList.bind('<Double-ButtonRelease-1>', self.addFile)

    # Demo function
    def show(self):
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

    def displayFiles(self):
        print(self.xlFiles)
        for xlFile in self.xlFiles:
            label = ttk.Label(self.fileList, text=xlFile, background=self.fileBackgroundColour)
            #label.bind('<Button-1>', self.fileHighlighter)
            label.bind('<Enter>', self.onEntering)
            label.bind('<Leave>', self.onLeaving)
            label.bind('<ButtonPress-1>', self.onPressing)
            label.bind('<ButtonRelease-1>', self.ReleaseHightlight)
            label.pack(padx=5, pady=5, side=tk.LEFT, fill=tk.BOTH, expand=True)

    # Call two functions when releasing mouse key
    def ReleaseHightlight(self, event):
        self.onReleasing(event)
        self.fileHighlighter(event)

    # TODO: Fix the problem of how to highlight only one item
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
        self.statusLabel['text'] = 'Selecting files'
        xlFile = filedialog.askopenfilename(initialdir='/', title='Select File',
                                            filetypes=[('Excel Files', '.xlsx')])

        if xlFile not in self.xlFiles and xlFile != '':
            self.xlFiles.append(xlFile)
            self.statusLabel['text'] = 'Added new file: ' + os.path.basename(xlFile)
            print('New file: '+xlFile)
        elif xlFile in self.xlFiles:
            self.statusLabel['text'] = 'You have added this file before.'
            messagebox.showinfo(
                'Information', 'You have added this file.')

        for widget in self.fileFrame.winfo_children():
            # print(widget.cget('text'))
            if isinstance(widget, ttk.Label) and widget.cget('text') != 'Files':
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
    root.protocol('WM_DELETE_WINDOW', mainApp.onClosing)
    root.mainloop()

    with open('xlList.txt', 'w') as f:
        for xlFile in mainApp.xlFiles:
            f.write(xlFile + '\n')
