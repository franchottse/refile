import tkinter as tk
import func


class MainApplication(tk.Frame):

    def __init__(self, master):
        self.master = master
        tk.Frame.__init__(self, self.master)
        self.configure_gui()
        self.create_widgets()

    def test_func(self):
        func.test_function()

    def configure_gui(self):
        # ...
        return

    def create_widgets(self):
        # ...
        return


if __name__ == '__main__':
    root = tk.Tk()
    main_app = MainApplication(root)
    main_app.test_func()
    root.mainloop()
