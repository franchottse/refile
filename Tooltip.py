'''
Reference: https://www.daniweb.com/programming/software-development/code/484591/a-tooltip-class-for-tkinter, https://www.jianshu.com/p/0ae1ce88a0d5
'''
import tkinter as tk
from tkinter import ttk


class Tooltip:
    def __init__(self, root, widget, text, timeout=650, offset=(0, 20)):
        # Set variables
        self.widget = widget
        self.root = root
        self.text = text
        self.timeout = timeout
        self.offset = offset

        # Initialise the tooltip properties
        self.id_after = None
        self.tipwindow = None
        self.background = 'white'
        self.foreground = '#5E5C5B'

    # Cancel cursor timer
    def unschedule(self):
        if self.id_after:
            self.widget.after_cancel(self.id_after)
        else:
            self.id_after = None

    # Set window properties
    def tip_window(self):
        window = tk.Toplevel(self.root)

        # Hide the window title or status bar, etc.
        window.overrideredirect(True)

        # Keep the window on top
        window.attributes('-toolwindow', 1)

        # Make sure the tooltip will be created under the cursor after the timeout
        x = self.root.winfo_pointerx() + self.offset[0]
        y = self.root.winfo_pointery() + self.offset[1]
        window.wm_geometry('+%d+%d' % (x, y))

        return window

    # Create window
    def showtip(self):
        kwargs = {
            'text': self.text,
            'justify': 'left',
            'background': self.background,
            'foreground': self.foreground,
            'relief': 'solid',
            'borderwidth': 1,
            'anchor': tk.CENTER
        }

        self.tipwindow = self.tip_window()
        label = ttk.Label(self.tipwindow, **kwargs)
        label.grid(ipadx=3, ipady=3, sticky=tk.N+tk.S+tk.E+tk.W)

    # Set the timer for cursor on the widget
    def schedule(self):
        self.id_after = self.widget.after(self.timeout, self.showtip)

    # Enter event
    def enter(self):
        self.schedule()

    # Hide tip
    def hidetip(self):
        # Destroy tipwindow
        if self.tipwindow:
            self.tipwindow.destroy()
        else:
            self.tipwindow = None

    # Leave event
    def leave(self):
        self.unschedule()
        self.hidetip()

    # Debug
    def debug(self):
        print('widget:', self.widget)
        print('text:', self.text)
        print('timeout:', self.timeout)
        print('offset:', self.offset)

        print('id_after:', self.id_after)
        print('tipwindow:', self.tipwindow)
        print('background:', self.background)
        print('foreground:', self.foreground)
