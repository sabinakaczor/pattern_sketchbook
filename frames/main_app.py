import tkinter as tk
from .home_page import HomePage
from .sketch_page import SketchPage

class MainApp(tk.Frame):
    def __init__(self, *args, master=None, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master
        self.pack(expand=True)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=0)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (HomePage, SketchPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            frame.grid(row=0, column=0, sticky="nsew")

        #self.show_frame("HomePage")
        self.show_frame("SketchPage")
        self.frames['SketchPage'].show_canvas(filename='files/szalik.pkl')

    def show_frame(self, page_name):
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.tkraise()
