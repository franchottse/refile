import tkinter as tk
from tkinter import filedialog, Text, messagebox, ttk, Menu
from PIL import Image, ImageTk
from diff_match_patch import diff_match_patch
import os
import func
import webbrowser


class ReFile(tk.Frame):

    def __init__(self, master):
        self.xlFiles = []
        self.master = master
        super().__init__()
        # tk.Frame.__init__(self, self.master)
        self.master.bind('<Delete>', self.deleteFile)
        self.master.bind('<Control-o>', self.addFile)
        self.master.bind('<Control-d>', self.clearAllFiles)

        # Style setup
        self.width = 1200
        self.height = 700
        self.xPosition = (self.master.winfo_screenwidth()//2)-(self.width//2)
        self.yPosition = (self.master.winfo_screenheight()//2)-(self.height//2)
        self.style = ttk.Style(self.master)
        # self.style.theme_use('clam')
        self.fileHighlightColour = '#B5ACA8'
        self.fileHoverColour = 'orange'
        self.fileHoverHightlightColour = 'grey'
        self.filePressColour = '#ED5903'
        self.fileBackgroundColour = 'white'
        # self.fileBackgroundColour = '#EBD987'
        self.labelColour = 'white'
        self.style.configure('TFrame', background="#B5ACA8", padding=5)
        self.style.configure('Wild.TButton', background='white',
                             foreground='black', font=('Helvetica', 13))
        # buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.style.map('Wild.TButton', foreground=[
            ('active', 'black'),
            ('pressed', 'black'),
            ('disabled', 'grey')
        ],
            background=[
            ('active', 'orange'),
            ('pressed', '!disabled', '#ED5903'),
            ('disabled', 'white')
        ])
        # self.style.configure("TEST.TLabel", foreground='white', background='black', font=(10))
        self.style.configure('Tab.TLabel', background='white', font=(
            'Helvetica', '11', 'bold'), relief=tk.SOLID, anchor=tk.CENTER)
        self.style.configure(
            'File.TLabel', background=self.fileBackgroundColour, font=('Helvetica', 10))
        self.style.configure('Status.TLabel', background='white', highlightbackground='#ED5903', font=(
            'Helvetica', 13), relief=tk.SOLID, anchor=tk.CENTER)

        # Variable to avoid packing file scrollbar repeatedly
        self.initializing = True

        # Variables to save the selected file(s) by the user
        self.selectedFile = ''
        self.selectedMultiFiles = []

        # Variable to save the file label
        self.fileLabelList = []

        # Variables to check the buttons states
        self.underlineOnOff = False
        self.strikethroughOnOff = False
        self.highlightOnOff = False
        self.paragraphMarkOnOff = False

        # Variable to store the selection of the text box
        self.selectedTextBox = 'old'

        # Variable to store the patch of two text boxes
        self.diffs = None

        # Variable to store the number of differences
        self.numDiff = 0

        # Variable to check if the word wrapping option is on
        #self.wordWrapBool = False
        self.wordWrapBool = tk.IntVar()
        print('self.wordWrapBool.get() when creating:', self.wordWrapBool.get())

        # Variable to save the current font size
        self.fontSize = 12

        # Variable to save the current option of radio buttons for font size
        self.radioFontOption = tk.StringVar()

        # Variables to save both vertical and horizontal less visible text name, it can be either 'old' or 'new'
        self.lessVerticalVisible = 'old'
        self.lessHorizontalVisible = 'old'

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
        self.master.iconbitmap('./refile-icon.ico')
        # colours = skyblue, #B7E7B0, #93E9BE, #FFEAAA <- recommend
        self.master.configure(bg='#FFEAAA')
        self.master.minsize(690, 690)

        # Attribution guide: https://wiki.creativecommons.org/wiki/Best_practices_for_attribution#This_is_a_good_attribution_for_material_you_modified_slightly

        # Word file icon
        self.wordIcon = ImageTk.PhotoImage(Image.open(
            './word.png').resize((100, 100), Image.ANTIALIAS))

        # Document file icon
        self.textIcon = ImageTk.PhotoImage(Image.open(
            './text.png').resize((100, 100), Image.ANTIALIAS))

        # PDF file icon
        self.pdfIcon = ImageTk.PhotoImage(Image.open(
            './pdf.png').resize((100, 100), Image.ANTIALIAS))

        # Unchecked radio button image
        self.uncheckedRadioImg = ImageTk.PhotoImage(
            Image.open('./unchecked-radio-button.png').resize((24, 24), Image.ANTIALIAS))

        # Checked radio button image
        self.checkedRadioImg = ImageTk.PhotoImage(
            Image.open('./checked-radio-button.png').resize((24, 24), Image.ANTIALIAS))

        # Toggle off button image
        self.toggleOffImg = ImageTk.PhotoImage(Image.open('./toggle-off.png'))

        # Toggle on button image
        self.toggleOnImg = ImageTk.PhotoImage(Image.open('./toggle-on.png'))

        # Configure grids
        tk.Grid.rowconfigure(self.master, 0, weight=1)
        tk.Grid.rowconfigure(self.master, 1, weight=1)
        tk.Grid.columnconfigure(self.master, (1, 2), weight=1)
        self.master.grid_columnconfigure(0, minsize=280)
        self.master.grid_rowconfigure(1, minsize=230)

        # Create frame for displaying data
        self.contentFrame = ttk.Frame(self.master)
        # self.contentLabel = tk.Label(self.contentFrame, text='Data', bg='white')
        self.contentLabel = ttk.Label(
            self.contentFrame, text='Contents', style='Tab.TLabel')
        self.contentFieldFrame = ttk.Frame(self.contentFrame)

        # Create text boxes
        self.createTextBoxes()

        # Create a frame for displaying files
        self.fileFrame = ttk.Frame(self.master)
        self.fileLabel = ttk.Label(
            self.fileFrame, text='Files', style='Tab.TLabel')
        self.fileListCanvas = tk.Canvas(
            self.fileFrame, height=120, highlightthickness=0, background='white')
        self.fileListFrame = tk.Frame(self.fileListCanvas, bg='white')
        self.fileScrollBar = ttk.Scrollbar(
            self.fileFrame, orient=tk.HORIZONTAL, command=self.fileListCanvas.xview)
        self.fileListCanvas.configure(xscrollcommand=self.fileScrollBar.set)

        self.fileCanvasFrame = self.fileListCanvas.create_window(
            (0, 0), window=self.fileListFrame, anchor=tk.W)
        self.fileListFrame.bind('<Configure>', self.onFileListFrameResizing)
        self.fileListCanvas.bind('<Configure>', self.onFileListCanvasResizing)

        # Bind fileListCanvas to addFile function
        self.fileListFrame.bind('<Double-ButtonRelease-1>', self.addFile)
        self.fileListCanvas.bind('<Double-ButtonRelease-1>', self.addFile)

        # Create a frame for displaying check boxes
        self.optionFrame = ttk.Frame(self.master)
        self.optionLabel = ttk.Label(
            self.optionFrame, text='Options', style='Tab.TLabel')
        self.optionFieldLabel = ttk.Label(
            self.optionFrame, background='white', style='Tab.TLabel')

        # Create option buttons
        self.createOptions()

        # Button configuration
        # buttonStyle = {'padx': '10', 'pady': '5', 'fg': 'black', 'bg': 'white', 'activebackground': '#F5E7D7', 'activeforeground': 'black', 'bd': '2'}
        self.buttonFrame = tk.Frame(self.master, bg='#FFEAAA')

        # Select File button
        self.openFile = ttk.Button(
            self.buttonFrame, text='Merge Text', style='Wild.TButton', command=self.mergePopup)
        self.openFile.bind('<Return>', self.mergePopup)

        # Clear File button
        self.clearContent = ttk.Button(
            self.buttonFrame, text='Clear Contents', style='Wild.TButton', command=self.clearAllContents)
        self.clearContent.bind('<Return>', self.clearAllContents)

        # Reference frames
        self.statusFrame = ttk.Frame(self.master)
        self.statusLabel = ttk.Label(
            self.statusFrame, text='Welcome to ReFile! Please double click the file area to add files', style='Status.TLabel')

    # Pack and grid everything
    def createWidgets(self):
        # Menu
        self.createMenu()

        # Option, data and file frames
        self.optionFrame.grid(row=0, column=0, padx=10,
                              pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.contentFrame.grid(row=0, column=1, columnspan=2, padx=10,
                               pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.fileFrame.grid(row=1, column=0, columnspan=3, padx=10,
                            pady=5, sticky=tk.N+tk.S+tk.E+tk.W)

        # Contents
        self.contentLabel.pack(padx=5, pady=5, fill=tk.X)
        self.renderTextBoxes()

        self.fileLabel.pack(padx=5, pady=(5, 0), fill=tk.X)
        self.fileListCanvas.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        self.optionLabel.pack(padx=5, pady=5, fill=tk.X)
        self.optionFieldLabel.pack(
            padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
        self.renderOptions()

        # Button frame
        self.buttonFrame.grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)

        # Status bar
        self.statusFrame.grid(row=2, column=1, columnspan=2,
                              padx=10, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.statusLabel.pack(fill=tk.BOTH, expand=True)

        # Open file button
        self.openFile.grid(row=0, column=0, padx=5, pady=5)

        # Clear files button
        # tk.Button(self.buttonFrame, text="Show scores", **buttonStyle,command=self.show).grid(row=0, column=1, padx=5, pady=5, sticky=tk.N+tk.S+tk.E+tk.W)
        self.clearContent.grid(row=0, column=1, padx=5, pady=5,
                               sticky=tk.N+tk.S+tk.E+tk.W)

        # Make sure the window is placed in the centre
        self.master.geometry(
            '{}x{}+{}+{}'.format(self.width, self.height, self.xPosition, self.yPosition))

    # Menu
    def createMenu(self):
        # Create menu
        self.menu = Menu(self.master)
        self.master.config(menu=self.menu)

        # File
        self.fileMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='File', menu=self.fileMenu)
        self.fileMenu.add_command(
            label='Open', accelerator='                    Ctrl+O', command=self.addFile)
        self.fileMenu.add_command(
            label='Delete All', accelerator='                    Ctrl+D', command=self.clearAllFiles)
        self.fileMenu.add_separator()
        self.fileMenu.add_command(label='Exit', command=self.onClosingWindow)

        # Format
        self.formatMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Format', menu=self.formatMenu)
        self.fontSubmenu = Menu(self.formatMenu, tearoff=False)
        self.formatMenu.add_checkbutton(
            label='Word Wrap', offvalue=0, onvalue=1, variable=self.wordWrapBool, command=self.wordWrap)
        self.formatMenu.add_cascade(label='Font Size', menu=self.fontSubmenu)
        for item in (12, 14, 16):
            self.fontSubmenu.add_radiobutton(label='{} points'.format(
                item), variable=self.radioFontOption, value='{} points'.format(item), command=self.changeFont)
        self.radioFontOption.set('12 points')

        self.formatMenu.add_command(
            label='Clear Style', accelerator='      ', command=self.clearStyle)

        # Help
        self.helpMenu = Menu(self.menu, tearoff=False)
        self.menu.add_cascade(label='Help', menu=self.helpMenu)
        self.helpMenu.add_command(
            label='How to Use', command=self.methodMessage)
        self.helpMenu.add_command(
            label='Release Notes', command=self.releaseNotesMessage)
        self.helpMenu.add_separator()
        self.helpMenu.add_command(
            label='About ReFile', command=self.aboutMessage)

    # Text boxes
    def createTextBoxes(self):
        # Create vertical scrollbar for both text boxes
        self.contentVerticalScrollbar = ttk.Scrollbar(
            self.contentFrame, orient=tk.VERTICAL, command=self.onContentVerticalScrolling)

        # Create horizontal scrollbar for both text boxes
        self.contentHorizontalScrollbar = ttk.Scrollbar(
            self.contentFrame, orient=tk.HORIZONTAL, command=self.onContentHorizontalScrolling)

        # Old and new text boxes
        self.oldTextBox = tk.Text(self.contentFieldFrame, height=18, width=1, font=('Helvetica', self.fontSize), selectbackground='#FFFFAA', selectforeground='black',
                                  relief=tk.SUNKEN, wrap=tk.NONE, state='disabled', xscrollcommand=self.onLeftHorizontalTextChanging, yscrollcommand=self.onLeftVerticalTextChanging)
        self.newTextBox = tk.Text(self.contentFieldFrame, height=18, width=1, font=('Helvetica', self.fontSize), selectbackground='#FFFFAA', selectforeground='black',
                                  relief=tk.SUNKEN, wrap=tk.NONE, state='disabled', xscrollcommand=self.onRightHorizontalTextChanging, yscrollcommand=self.onRightVerticalTextChanging)

        # Add tags for both boxes
        self.oldTextBox.tag_config(
            '-1', overstrike=False, background='SystemWindow')
        self.newTextBox.tag_config(
            '1', underline=False, background='SystemWindow')
        self.oldTextBox.bind('<1>', lambda event: self.oldTextBox.focus_set())
        self.newTextBox.bind('<1>', lambda event: self.newTextBox.focus_set())

        # Bind both text boxes to mouse wheel
        self.oldTextBox.bind('<MouseWheel>', self.onMouseWheeling)
        self.newTextBox.bind('<MouseWheel>', self.onMouseWheeling)

    # Pack both text boxes and vertical scrollbar
    def renderTextBoxes(self):
        self.contentHorizontalScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.contentVerticalScrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.contentFieldFrame.pack(
            padx=5, pady=(0, 5), fill=tk.BOTH, expand=True)
        self.oldTextBox.pack(padx=(0, 2.5), side=tk.LEFT,
                             fill=tk.BOTH, expand=True)
        self.newTextBox.pack(padx=(2.5, 0), side=tk.LEFT,
                             fill=tk.BOTH, expand=True)

    # Options
    def createOptions(self):
        # Text box label
        self.textBoxLabel = ttk.Label(
            self.optionFieldLabel, text='Text Box', style='Tab.TLabel')
        self.textBoxLabel.config(relief=tk.FLAT)

        # Left text box radio buttons
        self.leftRadioTextBox = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.leftRadioButton = tk.Label(
            self.leftRadioTextBox, bg='white', image=self.checkedRadioImg, cursor='hand2', padx=0, pady=0)
        self.leftRadioText = tk.Label(
            self.leftRadioTextBox, bg='white', text='Left Text Box', cursor='hand2', padx=0, pady=0)

        self.leftRadioTextBox.bind(
            '<Button-1>', lambda event, option='left': self.selectTextBox(option))
        self.leftRadioButton.bind(
            '<Button-1>', lambda event, option='left': self.selectTextBox(option))
        self.leftRadioText.bind(
            '<Button-1>', lambda event, option='left': self.selectTextBox(option))

        # Right text box radio buttons
        self.rightRadioTextBox = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.rightRadioButton = tk.Label(
            self.rightRadioTextBox, bg='white', image=self.uncheckedRadioImg, cursor='hand2', padx=0, pady=0)
        self.rightRadioText = tk.Label(
            self.rightRadioTextBox, bg='white', text='Right Text Box', cursor='hand2', padx=0, pady=0)

        self.rightRadioTextBox.bind(
            '<Button-1>', lambda event, option='right': self.selectTextBox(option))
        self.rightRadioButton.bind(
            '<Button-1>', lambda event, option='right': self.selectTextBox(option))
        self.rightRadioText.bind(
            '<Button-1>', lambda event, option='right': self.selectTextBox(option))

        # Text style label
        self.textStyleLabel = ttk.Label(
            self.optionFieldLabel, text='Text Style', style='Tab.TLabel')
        self.textStyleLabel.config(relief=tk.FLAT)

        # Underline insertion option
        self.underlineOption = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.underlineCheckBox = tk.Label(
            self.underlineOption, bg='white', image=self.toggleOffImg, cursor='hand2', padx=0, pady=0)
        self.underlineText = tk.Label(
            self.underlineOption, bg='white', text='Underline Insertion', cursor='hand2', padx=0, pady=0)

        self.underlineOption.bind('<Button-1>', self.underlineInsertion)
        self.underlineCheckBox.bind('<Button-1>', self.underlineInsertion)
        self.underlineText.bind('<Button-1>', self.underlineInsertion)

        # Strikethrough deletion option
        self.strikethroughOption = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.strikethroughCheckBox = tk.Label(
            self.strikethroughOption, bg='white', image=self.toggleOffImg, cursor='hand2', padx=0, pady=0)
        self.strikethroughText = tk.Label(
            self.strikethroughOption, bg='white', text='Strikethrough Deletion', cursor='hand2', padx=0, pady=0)

        self.strikethroughOption.bind(
            '<Button-1>', self.strikethroughDeleteion)
        self.strikethroughCheckBox.bind(
            '<Button-1>', self.strikethroughDeleteion)
        self.strikethroughText.bind('<Button-1>', self.strikethroughDeleteion)

        # Highlight insertion/deletion option
        self.highlightOption = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.highlightCheckBox = tk.Label(
            self.highlightOption, bg='white', image=self.toggleOffImg, cursor='hand2', padx=0, pady=0)
        self.highlightText = tk.Label(
            self.highlightOption, bg='white', text='Highlight Insertion/Deletion', cursor='hand2', padx=0, pady=0)

        self.highlightOption.bind('<Button-1>', self.highlightDifferece)
        self.highlightCheckBox.bind('<Button-1>', self.highlightDifferece)
        self.highlightText.bind('<Button-1>', self.highlightDifferece)

        # Show/Hide ¶ option
        self.paragraphMarkOption = tk.Label(
            self.optionFieldLabel, bg='white', cursor='hand2', padx=0, pady=0)
        self.paragraphMarkCheckBox = tk.Label(
            self.paragraphMarkOption, bg='white', image=self.toggleOffImg, cursor='hand2', padx=0, pady=0)
        self.paragraphMarkText = tk.Label(
            self.paragraphMarkOption, bg='white', text='Show/Hide ¶', cursor='hand2', padx=0, pady=0)

        self.paragraphMarkOption.bind('<Button-1>', self.paragraphMark)
        self.paragraphMarkCheckBox.bind('<Button-1>', self.paragraphMark)
        self.paragraphMarkText.bind('<Button-1>', self.paragraphMark)

    # Pack options
    def renderOptions(self):
        # Text box
        self.textBoxLabel.grid(row=0, column=0, columnspan=2,
                               padx=5, pady=(12, 10), sticky=tk.W)

        self.leftRadioTextBox.grid(row=1, column=0, padx=(11, 6), pady=0)
        self.leftRadioButton.pack(side=tk.LEFT)
        self.leftRadioText.pack(side=tk.LEFT)

        self.rightRadioTextBox.grid(row=1, column=1, padx=(6, 11), pady=0)
        self.rightRadioButton.pack(side=tk.LEFT)
        self.rightRadioText.pack(side=tk.LEFT)

        # Text style
        self.textStyleLabel.grid(
            row=2, column=0, columnspan=2, padx=5, pady=(35, 10), sticky=tk.W)

        # Underline insertion
        self.underlineOption.grid(
            row=3, column=0, padx=(30, 5), pady=(0, 5), columnspan=2, sticky=tk.W)
        self.underlineCheckBox.pack(side=tk.LEFT)
        self.underlineText.pack(padx=(3, 0), side=tk.LEFT)

        # Strikethrough deletion
        self.strikethroughOption.grid(
            row=4, column=0, padx=(30, 5), pady=(0, 5), columnspan=2, sticky=tk.W)
        self.strikethroughCheckBox.pack(side=tk.LEFT)
        self.strikethroughText.pack(padx=(3, 0), side=tk.LEFT)

        # Highlight Insertion/Deletion
        self.highlightOption.grid(
            row=5, column=0, padx=(30, 5), pady=(0, 5), columnspan=2, sticky=tk.W)
        self.highlightCheckBox.pack(side=tk.LEFT)
        self.highlightText.pack(padx=(3, 0), side=tk.LEFT)

        # Show/Hide ¶
        self.paragraphMarkOption.grid(
            row=6, column=0, padx=(30, 5), pady=0, columnspan=2, sticky=tk.W)
        self.paragraphMarkCheckBox.pack(side=tk.LEFT)
        self.paragraphMarkText.pack(padx=(3, 0), side=tk.LEFT)

    # Text box selection
    def selectTextBox(self, option):
        if option == 'left' and self.selectedTextBox != 'old':
            self.selectedTextBox = 'old'
            self.leftRadioButton.config(image=self.checkedRadioImg)
            self.rightRadioButton.config(image=self.uncheckedRadioImg)
            self.statusLabel['text'] = 'Left text box selected.'
        elif option == 'right' and self.selectedTextBox != 'new':
            self.selectedTextBox = 'new'
            self.leftRadioButton.config(image=self.uncheckedRadioImg)
            self.rightRadioButton.config(image=self.checkedRadioImg)
            self.statusLabel['text'] = 'Right text box selected.'

    # Underline insertion
    def underlineInsertion(self, event):
        self.underlineOnOff = not self.underlineOnOff
        self.underlineCheckBox.config(
            image=self.toggleOnImg) if self.underlineOnOff else self.underlineCheckBox.config(image=self.toggleOffImg)
        self.newTextBox.tag_config('1', underline=self.underlineOnOff)

        on_off = 'on' if self.underlineOnOff else 'off'
        self.statusLabel['text'] = 'Underline insertion ' + on_off + '.'

    # Strikethrough deletion
    def strikethroughDeleteion(self, event):
        self.strikethroughOnOff = not self.strikethroughOnOff
        self.strikethroughCheckBox.config(
            image=self.toggleOnImg) if self.strikethroughOnOff else self.strikethroughCheckBox.config(image=self.toggleOffImg)
        self.oldTextBox.tag_config('-1', overstrike=self.strikethroughOnOff)

        on_off = 'on' if self.strikethroughOnOff else 'off'
        self.statusLabel['text'] = 'Strikethrough deletion ' + on_off + '.'

    # Highlight insertion/deletion
    def highlightDifferece(self, event):
        self.highlightOnOff = not self.highlightOnOff
        self.highlightCheckBox.config(
            image=self.toggleOnImg) if self.highlightOnOff else self.highlightCheckBox.config(image=self.toggleOffImg)
        self.oldTextBox.tag_config('-1', background='#FFAAAA' if self.highlightOnOff else 'SystemWindow',
                                   selectbackground='#FFAAAA' if self.highlightOnOff else '#FFFFAA')
        self.newTextBox.tag_config('1', background='#AAFFAA' if self.highlightOnOff else 'SystemWindow',
                                   selectbackground='#AAFFAA' if self.highlightOnOff else '#FFFFAA')

        on_off = 'on' if self.highlightOnOff else 'off'
        self.statusLabel['text'] = 'Highlight insertion/deletion ' + on_off + '.'

    # Show/Hide ¶
    def paragraphMark(self, event):
        self.paragraphMarkOnOff = not self.paragraphMarkOnOff
        self.paragraphMarkCheckBox.config(
            image=self.toggleOnImg) if self.paragraphMarkOnOff else self.paragraphMarkCheckBox.config(image=self.toggleOffImg)

        on_off = 'on' if self.paragraphMarkOnOff else 'off'
        self.statusLabel['text'] = 'Paragraph mark ' + on_off + '.'

        if self.diffs == None:
            return

        rep = ('\n', '¶\n') if self.paragraphMarkOnOff else ('¶\n', '\n')
        self.diffs = [(action, text.replace(*rep))
                      for action, text in self.diffs]

        self.modifyTextBoxes()

    # Update vertical scrollbar only when left box has less vertical visibility than right box
    def onLeftVerticalTextChanging(self, *args):
        if self.lessVerticalVisible == 'old':
            self.contentVerticalScrollbar.set(*args)

    # Update vertical scrollbar only when right box has less vertical visibility than left box
    def onRightVerticalTextChanging(self, *args):
        if self.lessVerticalVisible == 'new':
            self.contentVerticalScrollbar.set(*args)

    # Update horizontal scrollbar only when left box has less horizontal visibility than right box
    def onLeftHorizontalTextChanging(self, *args):
        if self.lessHorizontalVisible == 'old':
            self.contentHorizontalScrollbar.set(*args)

    # Update horizontal scrollbar only when right box has less horizontal visibility than left box
    def onRightHorizontalTextChanging(self, *args):
        if self.lessHorizontalVisible == 'new':
            self.contentHorizontalScrollbar.set(*args)

    # Contents vertical scrollbar function
    def onContentVerticalScrolling(self, *args):
        self.oldTextBox.yview(*args)
        self.newTextBox.yview(*args)

    # Mouse wheel event for vertical scrolling
    def onMouseWheeling(self, event):
        self.oldTextBox.yview_scroll(-1*(event.delta//120), tk.UNITS)
        self.newTextBox.yview_scroll(-1*(event.delta//120), tk.UNITS)
        return 'break'

    # Contents horizontal scrollbar function
    def onContentHorizontalScrolling(self, *args):
        self.oldTextBox.xview(*args)
        self.newTextBox.xview(*args)

    # Word wrapping
    def wordWrap(self):
        print('self.wordWrapBool.get():', self.wordWrapBool.get())
        #self.wordWrapBool.set(1 if self.wordWrapBool.get() == 0 else 0)
        if self.wordWrapBool.get() == 1 and self.contentHorizontalScrollbar.winfo_ismapped():
            self.oldTextBox.config(wrap=tk.WORD)
            self.newTextBox.config(wrap=tk.WORD)
            self.contentHorizontalScrollbar.pack_forget()
            print('contentHorizontalScrollbar pack_forget')
        elif self.wordWrapBool.get() == 0 and not self.contentHorizontalScrollbar.winfo_ismapped():
            self.oldTextBox.config(wrap=tk.NONE)
            self.newTextBox.config(wrap=tk.NONE)
            self.contentHorizontalScrollbar.pack(side=tk.BOTTOM, fill=tk.X)
            print('contentHorizontalScrollbar pack')
        self.master.update_idletasks()
        self.updateViewVisibility()

    # Change font size
    def changeFont(self):
        size = 12
        if self.radioFontOption.get() == '14 points':
            size = 14
        elif self.radioFontOption.get() == '16 points':
            size = 16
        self.oldTextBox.config(font=('Helvetica', size))
        self.newTextBox.config(font=('Helvetica', size))
        self.fontSize = size

    # Clear all styles
    def clearStyle(self, event=None):
        # Turn every thing off
        self.underlineOnOff = False
        self.strikethroughOnOff = False
        self.highlightOnOff = False
        self.paragraphMarkOnOff = False

        # Change the check box image for all options
        self.underlineCheckBox.config(image=self.toggleOffImg)
        self.strikethroughCheckBox.config(image=self.toggleOffImg)
        self.highlightCheckBox.config(image=self.toggleOffImg)
        self.paragraphMarkCheckBox.config(image=self.toggleOffImg)

        # Implement "Clear Style"
        self.oldTextBox.tag_config(
            '-1', overstrike=False, background='SystemWindow', selectbackground='#FFFFAA')
        self.newTextBox.tag_config(
            '1', underline=False, background='SystemWindow', selectbackground='#FFFFAA')

        if self.diffs:
            self.diffs = [(action, text.replace('¶\n', '\n'))
                          for action, text in self.diffs]
            self.modifyTextBoxes()

        # Show status
        self.statusLabel['text'] = 'All styles are cleared.'

    # How to use message
    def methodMessage(self):
        title = 'ReFile'
        message = 'If you want to know more information about how to use it, please press OK to open the GitHub repository.'
        if messagebox.askokcancel(title, message):
            # TODO: Change the link
            webbrowser.open('https://github.com/franchottse')

    # Release not message
    def releaseNotesMessage(self):
        title = 'Release Notes'
        message = 'Version 1.0'
        messagebox.showinfo(title, message)

    # About message
    def aboutMessage(self):
        title = 'About ReFile'
        message = 'ReFile is a Python GUI app which compares two inputs of text, and can output the difference between them with different formats.'
        messagebox.showinfo(title, message)

    # Make sure the scrollbar works for the file list frame
    def onFileListFrameResizing(self, event=None):
        self.fileListCanvas.configure(
            scrollregion=self.fileListCanvas.bbox(tk.ALL))
        self.checkFilelistCanvasFrame()

    # Keep file list frame remaining the same size
    def onFileListCanvasResizing(self, event=None):
        if event != None:
            self.fileListCanvas.itemconfig(
                self.fileCanvasFrame, height=event.height)
        self.checkFilelistCanvasFrame()

    # Make the file scrollbar visible depending on file list frame size and file list canvas size
    def checkFilelistCanvasFrame(self):
        if not self.initializing:
            if self.fileScrollBar.winfo_ismapped() and self.fileListFrame.winfo_width() <= self.fileListCanvas.winfo_width():
                self.fileScrollBar.pack_forget()
            if not self.fileScrollBar.winfo_ismapped() and self.fileListFrame.winfo_width() > self.fileListCanvas.winfo_width():
                self.fileScrollBar.pack(padx=5, pady=(
                    0, 5), side=tk.BOTTOM, fill=tk.X)

    # Enter event for files
    def onEntering(self, event):
        colour = self.fileHoverColour if event.widget.cget(
            'state') != 'DISABLED' else self.fileHoverHightlightColour
        event.widget.config(background=colour)
        for child in event.widget.winfo_children():
            child.config(background=colour)

    # Leave event for files
    def onLeaving(self, event):
        colour = self.fileBackgroundColour if event.widget.cget(
            'state') != 'DISABLED' else self.fileHighlightColour
        event.widget.config(background=colour)
        for child in event.widget.winfo_children():
            child.config(background=colour)

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
                    widget.config(
                        background=self.fileBackgroundColour, state='NORMAL')
                    for child in widget.winfo_children():
                        child.config(background=self.fileBackgroundColour)

            self.selectedFile = filename
            self.statusLabel['text'] = os.path.basename(
                filename) + ' selected.'
            outLabel.config(
                background=self.fileHoverHightlightColour, state='DISABLED')
            for child in outLabel.winfo_children():
                child.config(background=self.fileHoverHightlightColour)

        self.displayContents()

    # Mouse double click event for opening a file
    def onDoubleClicking(self, event, filename):
        try:
            self.statusLabel['text'] = 'Opening file: ' + \
                os.path.basename(filename) + '.'
            os.startfile(filename)
            self.statusLabel['text'] = os.path.basename(filename) + ' opened.'
        except:
            print('Some error.')
            tk.messagebox.showerror(
                title='ReFile', message='Error: the file you are opening may be deleted, unknown or corrupted.')
            self.statusLabel['text'] = 'Error: the file you are opening may be deleted, unknown or corrupted.'

    # Close window event
    def onClosingWindow(self):
        self.statusLabel['text'] = 'Leaving ReFile'
        if messagebox.askokcancel('ReFile', 'Are you sure you want to close the window?'):
            self.master.destroy()
        else:
            self.statusLabel['text'] = ''

    # Test function for selecting some files to delete
    def selectMultiFiles(self, event=None):
        if not event.widget.cget('text') in self.selectedMultiFiles:
            self.selectedMultiFiles.append(event.widget.cget('text'))
            self.statusLabel['text'] = str(
                len(self.selectedMultiFiles)) + ' file(s) selected.'

    # File name wrapper
    def filenameWrapper(self, filename):
        # File name must be in full path
        return os.path.basename(filename) if len(os.path.basename(filename)) < 21 else os.path.basename(filename)[:20]+'...'

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
            with open('xlList.txt', 'r', encoding='utf-8') as f:
                tempFiles = f.read()
                tempFiles = tempFiles.split('\n')
                self.xlFiles = [x for x in tempFiles if x.strip()]
                print('File list:', self.xlFiles)
        self.statusLabel['text'] = 'Welcome to ReFile! Please double click the file area to add files.'

    # Display contents
    def displayContents(self):
        if self.selectedFile == '':
            return

        txt = func.importFile(self.selectedFile)
        if txt == '':
            tk.messagebox.showwarning(
                title='Error', message='The selected file is empty or does not exist.')
            return

        oldText = txt if self.selectedTextBox == 'old' else self.oldTextBox.get(1.0, tk.END)[
            :-1].replace('¶', '')
        newText = txt if self.selectedTextBox == 'new' else self.newTextBox.get(1.0, tk.END)[
            :-1].replace('¶', '')

        dmp = diff_match_patch()
        self.diffs = dmp.diff_main(oldText, newText)
        dmp.diff_cleanupSemantic(self.diffs)

        # Keep or remove underline insertion
        self.newTextBox.tag_config('1', underline=self.underlineOnOff)

        # Keep or remove strikethrough deletion
        self.oldTextBox.tag_config('-1', overstrike=self.strikethroughOnOff)

        # Keep or remove highlight difference
        self.oldTextBox.tag_config('-1', background='#FFAAAA' if self.highlightOnOff else 'SystemWindow',
                                   selectbackground='#FFAAAA' if self.highlightOnOff else '#FFFFAA')
        self.newTextBox.tag_config('1', background='#AAFFAA' if self.highlightOnOff else 'SystemWindow',
                                   selectbackground='#AAFFAA' if self.highlightOnOff else '#FFFFAA')

        # Keep or remove paragraph mark
        rep = ('\n', '¶\n') if self.paragraphMarkOnOff else ('¶\n', '\n')
        self.diffs = [(action, text.replace(*rep))
                      for action, text in self.diffs]

        self.modifyTextBoxes()
        self.numHighlight()

    # Clear all contents
    def clearAllContents(self):
        self.oldTextBox.config(state=tk.NORMAL)
        self.newTextBox.config(state=tk.NORMAL)
        self.oldTextBox.delete(1.0, tk.END)
        self.newTextBox.delete(1.0, tk.END)
        self.oldTextBox.config(state=tk.DISABLED)
        self.newTextBox.config(state=tk.DISABLED)
        self.diffs = None
        self.numDiff = 0

    # Merge result pop-up window
    def mergePopup(self, event=None):
        self.mergeWindow = tk.Toplevel(self.master)
        self.mergeWindow.protocol(
            "WM_DELETE_WINDOW", self.onMergeWindowDestroying)
        self.mergeWindow.bind('<Escape>', self.onMergeWindowDestroying)

        self.openFile.state(['disabled'])
        self.clearContent.state(['disabled'])

        mergeWidth = 680
        if self.fontSize == 14:
            mergeWidth = 820
        elif self.fontSize == 16:
            mergeWidth = 890
        mergeHeight = 380
        xMergePosition = (
            self.mergeWindow.winfo_screenwidth()//2)-(mergeWidth//2)
        yMergePosition = (
            self.mergeWindow.winfo_screenheight()//2)-(mergeHeight//2)
        self.mergeWindow.iconbitmap('./refile-icon.ico')
        self.mergeWindow.geometry(
            '{}x{}+{}+{}'.format(mergeWidth, mergeHeight, xMergePosition, yMergePosition))
        self.mergeWindow.configure(bg='#FFEAAA')
        self.mergeWindow.minsize(mergeWidth, mergeHeight)

        self.mergeFrame = ttk.Frame(self.mergeWindow)
        self.mergeFrame.pack(padx=5, pady=5, fill=tk.BOTH, expand=True)

        # Prevent interacting with root window
        self.mergeWindow.grab_set()

        # Get the focus on merge window
        self.mergeWindow.focus_set()

        # Merge text box
        self.mergeTextBox = tk.Text(self.mergeFrame, width=70, height=12, font=(
            'Helvetica', self.fontSize), selectbackground='#FFFFAA', selectforeground='black', relief=tk.SUNKEN, wrap=tk.WORD)
        self.mergeTextBox.tag_config('-1', overstrike=self.strikethroughOnOff, background='#FFAAAA' if self.highlightOnOff else 'SystemWindow',
                                     selectbackground='#FFAAAA' if self.highlightOnOff else '#FFFFAA')
        self.mergeTextBox.tag_config('1', underline=self.underlineOnOff, background='#AAFFAA' if self.highlightOnOff else 'SystemWindow',
                                     selectbackground='#AAFFAA' if self.highlightOnOff else '#FFFFAA')
        self.mergeText()
        self.mergeTextBox.pack(padx=(5, 0), pady=5,
                               side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Vertical scrollbar
        self.mergeVerticalScrollBar = ttk.Scrollbar(
            self.mergeFrame, orient=tk.VERTICAL, command=self.mergeTextBox.yview)
        self.mergeTextBox.configure(
            yscrollcommand=self.mergeVerticalScrollBar.set)
        self.mergeVerticalScrollBar.pack(
            padx=(0, 5), side=tk.RIGHT, pady=5, fill=tk.Y)

        self.mergeResultButtonFrame = tk.Frame(self.mergeWindow, bg='#FFEAAA')
        self.mergeResultButtonFrame.pack(
            padx=5, pady=(0, 5), fill=tk.X)

        # Result label
        self.mergeResult = ttk.Label(
            self.mergeResultButtonFrame, text='No. of Highlights: '+str(self.numDiff), style='Tab.TLabel')
        self.mergeResult.pack(padx=5, pady=5, side=tk.LEFT)

        # Cancel button
        self.cancelButton = ttk.Button(
            self.mergeResultButtonFrame, text='Cancel', style='Wild.TButton', command=self.onMergeWindowDestroying)
        self.cancelButton.pack(padx=(0, 5), pady=5, side=tk.RIGHT)

        # Save output button
        self.saveButton = ttk.Button(
            self.mergeResultButtonFrame, text='Save Output', style='Wild.TButton', command=self.exportFile)
        self.saveButton.pack(padx=5, pady=5, side=tk.RIGHT)

    # Merge text
    def mergeText(self):
        if not self.diffs:
            return

        self.mergeTextBox.config(state=tk.NORMAL)
        self.mergeTextBox.delete(1.0, tk.END)

        for action, text in self.diffs:
            for char in text:
                self.mergeTextBox.insert(tk.END, char, str(
                    action) if char != '\n' else '0')

        self.mergeTextBox.config(state=tk.DISABLED)

    # Export file
    def exportFile(self, event=None):
        # Disable the merge window
        self.mergeWindow.withdraw()

        # Save output
        func.exportFile(self.diffs, self.underlineOnOff,
                        self.strikethroughOnOff, self.highlightOnOff)

        # Enable merge window
        self.mergeWindow.deiconify()

    # Enable buttons from root when closing merge window
    def onMergeWindowDestroying(self, event=None):
        self.mergeWindow.destroy()
        self.openFile.state(['!disabled'])
        self.clearContent.state(['!disabled'])

    # Modify both text boxes
    def modifyTextBoxes(self):
        # Change both text boxes state to normal
        self.oldTextBox.config(state=tk.NORMAL)
        self.newTextBox.config(state=tk.NORMAL)

        # Clear the contents for both boxes
        self.oldTextBox.delete(1.0, tk.END)
        self.newTextBox.delete(1.0, tk.END)

        # Insert the text to both boxes
        for action, text in self.diffs:
            for char in text:
                if action == -1:
                    self.oldTextBox.insert(
                        tk.END, char, '-1' if char != '\n' else '0')
                elif action == 1:
                    self.newTextBox.insert(
                        tk.END, char, '1' if char != '\n' else '0')
                else:
                    self.oldTextBox.insert(tk.END, char)
                    self.newTextBox.insert(tk.END, char)

        self.updateViewVisibility()

        # Make the state back to disabled
        self.oldTextBox.config(state=tk.DISABLED)
        self.newTextBox.config(state=tk.DISABLED)

    def updateViewVisibility(self):
        # Update whole app before getting yview and xview
        self.master.update()

        print('self.oldTextBox.yview()[1]:', self.oldTextBox.yview()[1])
        print('self.newTextBox.yview()[1]:', self.newTextBox.yview()[1])
        print('self.oldTextBox.xview()[1]:', self.oldTextBox.xview()[1])
        print('self.newTextBox.xview()[1]:', self.newTextBox.xview()[1])
        # Update vertical scrollbar depending on less vertically visible text box
        self.lessVerticalVisible = 'old' if self.oldTextBox.yview(
        )[1] <= self.newTextBox.yview()[1] else 'new'

        # Update horizontal scrollbar depending on less horizontally visible text box
        self.lessHorizontalVisible = 'old' if self.oldTextBox.xview(
        )[1] <= self.newTextBox.xview()[1] else 'new'

    def numHighlight(self):
        # Reset the number of hightlights to avoid the miscalculation
        self.numDiff = 0
        for action, _ in self.diffs:
            self.numDiff += 1 if action != 0 else 0

    def displayFiles(self):
        print('File list:', self.xlFiles)
        for xlFile in self.xlFiles:
            label = ttk.Label(self.fileListFrame,
                              style='File.TLabel', takefocus=True)
            imageCanvas = tk.Canvas(
                label, width=100, height=100, highlightthickness=0)
            textLabel = ttk.Label(label, text=self.filenameWrapper(
                xlFile), style='File.TLabel', anchor=tk.CENTER, wraplength=140)
            self.fileLabelList.append(label)

            # Highlight the selected file again after adding files
            if xlFile == self.selectedFile:
                label.config(background=self.fileHighlightColour,
                             state='DISABLED')
                for child in label.winfo_children():
                    child.config(background=self.fileHighlightColour)

            # Bind label to onEntering
            label.bind('<Enter>', self.onEntering)
            label.bind('<FocusIn>', self.onEntering)

            # Bind label to onLeaving
            label.bind('<Leave>', self.onLeaving)
            label.bind('<FocusOut>', self.onLeaving)

            # Bind label, imageCanvas and textLabel to onPressing
            label.bind('<ButtonPress-1>', lambda event,
                       outLabel=label: self.onPressing(event, outLabel))
            imageCanvas.bind('<ButtonPress-1>', lambda event,
                             outLabel=label: self.onPressing(event, outLabel))
            textLabel.bind('<ButtonPress-1>', lambda event,
                           outLabel=label: self.onPressing(event, outLabel))

            # Bind label, imageCanvas and textLabel to onReleasing
            label.bind('<ButtonRelease-1>', lambda event, outLabel=label,
                       filename=xlFile: self.onReleasing(event, outLabel, filename))
            label.bind('<Return>', lambda event, outLabel=label,
                       filename=xlFile: self.onReleasing(event, outLabel, filename))
            imageCanvas.bind('<ButtonRelease-1>', lambda event, outLabel=label,
                             filename=xlFile: self.onReleasing(event, outLabel, filename))
            textLabel.bind('<ButtonRelease-1>', lambda event, outLabel=label,
                           filename=xlFile: self.onReleasing(event, outLabel, filename))

            # Bind label, imageCanvas and textLabel to onDoubleClicking
            label.bind('<Double-Button-1>', lambda event,
                       filename=xlFile: self.onDoubleClicking(event, filename))
            label.bind('<Control-Return>', lambda event,
                       filename=xlFile: self.onDoubleClicking(event, filename))
            imageCanvas.bind('<Double-Button-1>', lambda event,
                             filename=xlFile: self.onDoubleClicking(event, filename))
            textLabel.bind('<Double-Button-1>', lambda event,
                           filename=xlFile: self.onDoubleClicking(event, filename))

            # label.bind('<Control-ButtonRelease-1>', self.selectMultiFiles)

            img = ''
            if xlFile.lower().endswith(('.doc', '.docx')):
                img = self.wordIcon
            elif xlFile.lower().endswith('.pdf'):
                img = self.pdfIcon
            else:
                img = self.textIcon

            label.pack(padx=30, side=tk.LEFT)
            imageCanvas.pack(padx=25, pady=(10, 5))
            imageCanvas.create_image((0, 0), anchor=tk.N+tk.W, image=img)
            textLabel.pack(padx=5, pady=5)

        # Make sure the widgets in file list frame are center
        self.master.update()
        self.onFileListFrameResizing()

    # Delete file
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
                if isinstance(widget, ttk.Label) and outLabel.cget('state') == 'DISABLED' and widget.cget('text') == self.filenameWrapper(self.selectedFile):
                    outLabel.destroy()
                    print('Deleted file:', self.selectedFile)
                    self.statusLabel['text'] = os.path.basename(
                        self.selectedFile) + ' deleted.'
                    self.selectedFile = ''
                    if not self.fileListFrame.winfo_children():
                        self.master.update()
                        self.fileListFrame.config(width=1)

    def addFile(self, event=None):
        self.openFile.state(['disabled'])
        self.clearContent.state(['disabled'])
        self.statusLabel['text'] = 'Selecting files'
        files = filedialog.askopenfilenames(initialdir='/', title='Select File',
                                            filetypes=[
                                                ('All Files', '.doc .docx .txt .pdf'),
                                                ('Word Documents', '.doc .docx'),
                                                ('Text Documents', '.txt'),
                                                ('Adobe PDF', '.pdf')])

        for file in files:
            if file not in self.xlFiles and file != '':
                self.xlFiles.append(file)
                print('New file: ' + file)
            '''elif file in self.xlFiles:
                self.statusLabel['text'] = 'There is at least a file added before.'
                messagebox.showinfo(
                    'ReFile', 'There is at least a file added before.')
                self.addFile()
                break'''
        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        self.fileLabelList.clear()
        self.openFile.state(['!disabled'])
        self.clearContent.state(['!disabled'])
        self.statusLabel['text'] = 'Complete!'
        self.displayFiles()

    # Clear all files
    def clearAllFiles(self, event=None):
        if self.xlFiles and not messagebox.askyesno('ReFile', 'Do you really want to delete all files?'):
            return

        self.xlFiles.clear()
        self.fileLabelList.clear()
        for widget in self.fileListFrame.winfo_children():
            widget.destroy()

        self.master.update()
        self.fileListFrame.config(width=1)

    # TODO: Solve the problem of passing arguments to other python files for text files


if __name__ == '__main__':
    root = tk.Tk()
    mainApp = ReFile(root)
    root.protocol('WM_DELETE_WINDOW', mainApp.onClosingWindow)
    root.mainloop()

    with open('xlList.txt', 'w', encoding='utf-8') as f:
        for xlFile in mainApp.xlFiles:
            f.write(xlFile + '\n')
