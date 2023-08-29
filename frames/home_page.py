import tkinter as tk

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.create_widgets()

    def create_widgets(self):
        self.new = tk.Button(self, width=30)
        self.new['text'] = '\u2295 New sketch'
        self.new['command'] = self.show_config
        self.new.pack()

        self.load = tk.Button(self, width=30)
        self.load['text'] = '\u270E Edit sketch'
        self.load['command'] = self.show_sketch
        self.load.pack()

    def show_config(self):
        self.controller.show_frame('SketchPage')
        self.controller.frames['SketchPage'].show_config()

    def show_sketch(self):
        self.controller.show_frame('SketchPage')
        self.controller.frames['SketchPage'].show_canvas()