import tkinter as tk
from tkinter import colorchooser
from tkinter import filedialog
import pickle

NORMAL_BTN_COLOR = "#bec3ff"
DISABLED_BTN_COLOR = "#b1b1b1"

class CanvasFrame(tk.Frame):

    def __init__(self, parent, starting_func, *args, **kwargs):
        tk.Frame.__init__(self, parent)
        self.data = {}
        getattr(self, starting_func)(*args, **kwargs)
        self.eraser_radius = 6        
        self.create_canvas()
        self.create_toolkit()

    def create_new_sketch(self, rows, cols, aspect_ratio):
        self.state = 'new'
        self.data['rows'] = rows
        self.data['cols'] = cols
        self.data['aspect_ratio'] = aspect_ratio
        self.data['canvas_arr'] = {}
        self.leading_color = 'blue'
        self.secondary_color = 'gray'
        self.eraser_color = 'white'

    def load_from_file(self, filename=None):
        self.state = 'loaded'
        if filename is not None:
            self.data = pickle.load(open(filename, 'rb'))
        else:
            with filedialog.askopenfile(mode='rb', defaultextension='.pkl', filetypes=[('pickle files', '*.pkl')]) as file:
                self.data = pickle.load(file)
        self.leading_color = self.data.get('leading_color', 'blue')
        self.secondary_color = self.data.get('secondary_color', 'gray')
        self.eraser_color = self.data.get('eraser_color', 'white')

    def save_to_file(self, event):
        self.data['leading_color'] = self.leading_color
        self.data['secondary_color'] = self.secondary_color
        self.data['eraser_color'] = self.eraser_color
        with filedialog.asksaveasfile(mode='wb', defaultextension='.pkl', filetypes=[('pickle files', '*.pkl')]) as file:
            pickle.dump(self.data, file)

    def create_canvas(self):
        canvas_container = tk.Frame(self, width=800, height=500)
        canvas_container.pack(side="right")

        self.canvas = tk.Canvas(canvas_container, borderwidth=0, highlightthickness=0)
        self.canvas.config(cursor="hand1")
        self.canvas.config(bg='#FFFFFF')
        hbar = tk.Scrollbar(canvas_container, orient=tk.HORIZONTAL)
        hbar.pack(side=tk.BOTTOM, fill=tk.X)
        hbar.config(command=self.canvas.xview)
        vbar = tk.Scrollbar(canvas_container, orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT, fill=tk.Y)
        vbar.config(command=self.canvas.yview)
        self.canvas.config(width=800, height=500)

        self.canvas.config(xscrollcommand=hbar.set, yscrollcommand=vbar.set)
        self.canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

        self.canvas.bind('<Shift-Button-1>', self.erase_cell)
        self.canvas.bind('<Shift-B1-Motion>', self.erase_cell)

        self.cell_width = 20
        self.cell_height = self.cell_width / self.data['aspect_ratio']

        if len(self.data['canvas_arr']):
            canvas_arr_copy = self.data['canvas_arr']
            self.data['canvas_arr'] = {}
            for old_cell_id in canvas_arr_copy:
                row = canvas_arr_copy[old_cell_id]['row']
                column = canvas_arr_copy[old_cell_id]['column']
                color = canvas_arr_copy[old_cell_id]['color']

                self.create_canvas_cell( row, column, color)
        else:
            for row in range(self.data['rows']):
                for column in range(self.data['cols']):
                        color = self.eraser_color
                        
                        self.create_canvas_cell( row, column, color)

        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

        self.canvas.bind('<Button-4>', lambda e: self.canvas.yview_scroll(-1, 'units'))
        self.canvas.bind('<Button-5>', lambda e: self.canvas.yview_scroll(1, 'units'))

        self.canvas.bind('<Control-4>', lambda e: self.scale_canvas(1.2))
        self.canvas.bind('<Control-5>', lambda e: self.scale_canvas(0.8))

    def create_canvas_cell(self, row, column, color):
        cell_id = self.canvas.create_rectangle(row * self.cell_width, column * self.cell_height, (row + 1) * self.cell_width, (column + 1) * self.cell_height, outline="gray", fill="%s" % color)

        self.data['canvas_arr'][cell_id] = {
            'row': row,
            'column': column,
            'color': color
        }

        self.canvas.tag_bind(cell_id, '<Button-1>', self.change_cell_color)
        self.canvas.tag_bind(cell_id, '<Button-3>', self.change_cell_color)

    def change_cell_color(self, event):
        cell_id = event.widget.find_withtag('current')[0]
        color = self.leading_color if event.num == 1 else self.secondary_color
        self.canvas.itemconfig(cell_id, fill=color)
        self.data['canvas_arr'][cell_id]['color'] = color

    def create_toolkit(self):
        self.toolkit = tk.Canvas(self, borderwidth=0, highlightthickness=0, cursor="hand1", height=500)

        eraser_color_chooser = self.toolkit.create_rectangle(40, 0, 80, 40, tags="eraser_color", fill=self.eraser_color)
        self.toolkit.tag_bind(eraser_color_chooser, '<Button>', self.choose_color)

        secondary_color_chooser = self.toolkit.create_rectangle(20, 20, 60, 60, tags="secondary_color", fill=self.secondary_color)
        self.toolkit.tag_bind(secondary_color_chooser, '<Button>', self.choose_color)

        leading_color_chooser = self.toolkit.create_rectangle(0, 40, 40, 80, tags="leading_color", fill=self.leading_color)
        self.toolkit.tag_bind(leading_color_chooser, '<Button>', self.choose_color)

        self.palette_colors = []
        self.palette_y = 100
        self.palette_color_diam = 20

        if self.state == 'loaded':
            for k in self.data['canvas_arr']:
                self.add_palette_color(self.data['canvas_arr'][k]['color'])
            self.add_palette_color(self.leading_color)
            self.add_palette_color(self.secondary_color)
            self.add_palette_color(self.eraser_color)

        zoom_y = 190
        zoom_diam = 30

        self.toolkit.create_text((zoom_diam + 5, zoom_y - .5 * zoom_diam), text='Zoom')

        self.toolkit.create_rectangle(0, zoom_y, zoom_diam, zoom_y + zoom_diam, fill=NORMAL_BTN_COLOR, tags="zoom_in")
        self.toolkit.create_text((zoom_diam * .5, zoom_y + zoom_diam * .5), text='+', tags="zoom_in")
        self.toolkit.tag_bind('zoom_in', '<Button-1>', lambda e: self.scale_canvas(1.2))

        self.toolkit.create_rectangle(zoom_diam + 10, zoom_y, 2 * zoom_diam + 10, zoom_y + zoom_diam, fill=NORMAL_BTN_COLOR, tags="zoom_out")
        self.toolkit.create_text((zoom_diam + 10 + zoom_diam * .5, zoom_y + zoom_diam * .5), text='-', tags="zoom_out")
        self.toolkit.tag_bind('zoom_out', '<Button-1>', lambda e: self.scale_canvas(0.8))

        eraser_y = 265
        eraser_diam = 30

        self.toolkit.create_text((eraser_diam + 5, eraser_y - .5 * eraser_diam), text='Eraser')

        self.enlarge_eraser_btn = self.toolkit.create_rectangle(0, eraser_y, eraser_diam, eraser_y + eraser_diam, fill=NORMAL_BTN_COLOR, tags="enlarge_eraser")
        self.toolkit.create_text((eraser_diam * .5, eraser_y + eraser_diam * .5), text='+', tags="enlarge_eraser")
        self.toolkit.tag_bind('enlarge_eraser', '<Button-1>', lambda e: self.resize_eraser(mode="enlarge"))

        self.reduce_eraser_btn = self.toolkit.create_rectangle(eraser_diam + 10, eraser_y, 2 * eraser_diam + 10, eraser_y + eraser_diam, fill=NORMAL_BTN_COLOR, tags="reduce_eraser")
        self.toolkit.create_text((eraser_diam + 10 + eraser_diam * .5, eraser_y + eraser_diam * .5), text='-', tags="reduce_eraser")
        self.toolkit.tag_bind('reduce_eraser', '<Button-1>', lambda e: self.resize_eraser(mode="reduce"))

        # auxiliary lines

        aux_line_y = 340
        aux_line_diam = 30

        self.toolkit.create_text((aux_line_diam + 5, aux_line_y - .5 * aux_line_diam), text='Helpers')

        self.vertical_line_btn = self.toolkit.create_rectangle(0, aux_line_y, aux_line_diam, aux_line_y + aux_line_diam, fill=NORMAL_BTN_COLOR, tags="vertical_line")
        self.toolkit.create_line(aux_line_diam * .5, aux_line_y, aux_line_diam * .5, aux_line_y + aux_line_diam, fill='red', tags="vertical_line")
        self.toolkit.tag_bind('vertical_line', '<Button-1>', lambda e: self.resize_eraser(mode="enlarge"))

        self.horizontal_line_btn = self.toolkit.create_rectangle(aux_line_diam + 10, aux_line_y, 2 * aux_line_diam + 10, aux_line_y + aux_line_diam, fill=NORMAL_BTN_COLOR, tags="horizontal_line")
        self.toolkit.create_line(aux_line_diam + 10, aux_line_y + aux_line_diam * 0.5, 2 * aux_line_diam + 10, aux_line_y + aux_line_diam * 0.5, fill='red', tags="horizontal_line")
        self.toolkit.tag_bind('horizontal_line', '<B1-Motion>', self.add_auxiliary_line)
        #self.toolkit.tag_bind('horizontal_line', '<Button-1>', lambda e: self.toolkit.config(cursor="hand1"))

        self.toolkit.create_rectangle(0, 400, 30, 430, fill="#73d9d9", tags="save")
        self.toolkit.create_text((15, 415), text='\u2b07', tags='save')
        self.toolkit.tag_bind('save', '<Button-1>', self.save_to_file)

        self.toolkit.pack(side="left")

    def choose_color(self, event):
        widget_id = event.widget.find_withtag('current')[0]
        type = 'leading' if 'leading_color' in self.toolkit.gettags(widget_id) else 'secondary' if 'secondary_color' in self.toolkit.gettags(widget_id) else 'eraser'
        color_code = colorchooser.askcolor(title='Choose %s color' % type, initialcolor=self.__dict__['%s_color' % type])[1]
        if color_code is not None:
            self.__dict__['%s_color' % type] = color_code
            self.toolkit.itemconfig('%s_color' % type, fill=color_code)
            self.add_palette_color(color_code)

    def add_palette_color(self, color):
        if color not in self.palette_colors:
            self.palette_colors.append(color)
            x0 = (len(self.palette_colors) - 1) * self.palette_color_diam
            y0 = self.palette_y
            x1 = x0 + self.palette_color_diam
            y1 = y0 + self.palette_color_diam
            palette_cell_id = self.toolkit.create_oval(x0, y0, x1, y1, fill=color)
            self.toolkit.tag_bind(palette_cell_id, "<Shift-Button-1>", self.choose_palette_color)
            self.toolkit.tag_bind(palette_cell_id, "<Button>", self.choose_palette_color)


    def choose_palette_color(self, event):
        if event.num in (1,3):
            widget_id = event.widget.find_withtag('current')[0]
            color_code = self.toolkit.itemcget(widget_id, 'fill')
            tag = '%s_color' % ('eraser' if event.state & 1 else 'leading' if event.num == 1 else 'secondary')
            self.__dict__[tag] = color_code
            self.toolkit.itemconfig(tag, fill=color_code)

    def scale_canvas(self, scale):
        for cell_id in self.data['canvas_arr']:
            self.canvas.scale(cell_id, 0, 0, scale, scale)
        self.canvas.configure(scrollregion = self.canvas.bbox("all"))

    def resize_eraser(self, mode="enlarge"):
        min_radius = 3
        max_radius = 99
        radius_step = 3 if mode == 'enlarge' else -3

        updated_radius = self.eraser_radius + radius_step
        if updated_radius >= min_radius and updated_radius <= max_radius:
            self.eraser_radius = updated_radius

        if self.eraser_radius <= min_radius:
            self.toolkit.itemconfig(self.reduce_eraser_btn, state=tk.DISABLED, fill=DISABLED_BTN_COLOR)
        else:
            self.toolkit.itemconfig(self.reduce_eraser_btn, state=tk.NORMAL, fill=NORMAL_BTN_COLOR)

        if self.eraser_radius >= max_radius:
            self.toolkit.itemconfig(self.enlarge_eraser_btn, state=tk.DISABLED, fill=DISABLED_BTN_COLOR)
        else:
            self.toolkit.itemconfig(self.enlarge_eraser_btn, state=tk.NORMAL, fill=NORMAL_BTN_COLOR)

    def erase_cell(self, event):
        x = self.canvas.canvasx(event.x)
        y = self.canvas.canvasy(event.y)
        cells = self.canvas.find_overlapping(x - self.eraser_radius, y - self.eraser_radius, x + self.eraser_radius, y + self.eraser_radius)
        for cell_id in cells:
            self.canvas.itemconfig(cell_id, fill=self.eraser_color)
            self.data['canvas_arr'][cell_id]['color'] = self.eraser_color

    def add_auxiliary_line(self, event):
        print('a', end=' ', flush=True)
        self.toolkit.config(cursor="X_cursor red")
        self.toolkit.bind('<ButtonRelease-1>', self.cancel_auxiliary_line)
        for cell_id in self.data['canvas_arr']:
            self.canvas.tag_bind(cell_id, '<ButtonRelease-1>', lambda e: None)
            self.canvas.tag_bind(cell_id, '<B1-Motion>', lambda e: None)

    def cancel_auxiliary_line(self, event):
        print('c', end=' ', flush=True)
        self.toolkit.unbind('<ButtonRelease-1>')
        self.toolkit.config(cursor="hand1")