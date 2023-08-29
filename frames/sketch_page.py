import tkinter as tk
from .config_frame import ConfigFrame
from .canvas_frame import CanvasFrame

class SketchPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        size = {'width': int(self.winfo_screenwidth() * .9), 'height': int(self.winfo_screenheight() * .9)}
        self.controller.master.geometry('{width}x{height}'.format(**size))

    def show_config(self):
        self.config = ConfigFrame(self)
        self.config.pack()

    def show_canvas(self, filename=None):
        self.canvas = CanvasFrame(self, 'load_from_file', filename)
        self.canvas.pack()

    def check_config(self):
        stitches_per_cm = int(self.config.getValue('stitches_no')) / int(self.config.getValue('width_cm_input'))
        rows_per_cm = int(self.config.getValue('rows_no')) / int(self.config.getValue('height_cm_input'))
        aspect_ratio = rows_per_cm / stitches_per_cm
        width = int(self.config.getValue('sketch_width_input'))
        height = int(self.config.getValue('sketch_height_input'))
        self.config.pack_forget()
        self.canvas = CanvasFrame(self, 'create_new_sketch', width, height, aspect_ratio)
        self.canvas.pack()

    def hide_config(self):
        self.config.pack_forget()
        self.controller.show_frame('HomePage')