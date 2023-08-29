from tkinter import *
import tkinter

top = tkinter.Tk()

def helloCallBack():
   print( "Hello Python", "Hello World")

B = tkinter.Button(top, text ="Hello", command = helloCallBack)

B.pack()
B.place(bordermode=OUTSIDE, height=100, width=100)
top.mainloop()