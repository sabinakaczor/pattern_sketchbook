import tkinter as tk
from frames.main_app import MainApp

root = tk.Tk()
root.minsize(800, 500)
root.title('Welcome to the Pattern Sketchbook!')
root.attributes('-zoomed', True)
app = MainApp(master=root)
app.mainloop()