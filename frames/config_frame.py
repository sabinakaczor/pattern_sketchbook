import tkinter as tk

class ConfigFrame(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)
        self.parent = parent
        self.create_widgets()

    def create_widgets(self):
        self.label1 = tk.Label(self, text='Pass the dimensions of your sample:')
        self.label1.grid(columnspan=2, pady=20)

        self.width_cm_label = tk.Label(self, text='Width [cm]', padx=10)
        self.width_cm_label.grid(row=1, sticky=tk.E)

        self.width_cm_input = tk.Entry(self, width=4)
        self.width_cm_input.grid(row=1, column=1, sticky=tk.W)

        self.height_cm_label = tk.Label(self, text='Height [cm]', padx=10)
        self.height_cm_label.grid(row=2, sticky=tk.E)

        self.height_cm_input = tk.Entry(self, width=4)
        self.height_cm_input.grid(row=2, column=1, sticky=tk.W)

        self.stitches_label = tk.Label(self, text='Number of stitches', padx=10)
        self.stitches_label.grid(row=3, sticky=tk.E)

        self.stitches_no = tk.Entry(self, width=4)
        self.stitches_no.grid(row=3, column=1, sticky=tk.W)

        self.rows_label = tk.Label(self, text='Number of rows', padx=10)
        self.rows_label.grid(row=4, sticky=tk.E)

        self.rows_no = tk.Entry(self, width=4)
        self.rows_no.grid(row=4, column=1, sticky=tk.W)

        self.label2 = tk.Label(self, text='Pass the dimensions of your sketch:')
        self.label2.grid(row=5, columnspan=2, pady=20)

        f = tk.Frame(self)
        f.grid(row=6, columnspan=2)

        self.sketch_width_input = tk.Entry(f, width=4)
        self.sketch_width_input.grid(row=0, column=0, padx=10)

        self.sketch_height_input = tk.Entry(f, width=4)
        self.sketch_height_input.grid(row=0, column=1, padx=10)

        self.sketch_width_label = tk.Label(f, text='width')
        self.sketch_width_label.grid(row=1, column=0, padx=10)

        self.sketch_height_label = tk.Label(f, text='height')
        self.sketch_height_label.grid(row=1, column=1, padx=10)

        self.cancel = tk.Button(self, text='Cancel')
        self.cancel['command'] = self.parent.hide_config
        self.cancel.grid(row=7, column=0, pady=20, sticky=tk.W)

        self.ok = tk.Button(self, text='OK', width=6)
        self.ok['command'] = self.parent.check_config
        self.ok.grid(row=7, column=1, pady=20, sticky=tk.E)

    def getValue(self, entry):
        return getattr(self, entry).get()