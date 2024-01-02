from tkinter import *
from tkinter import ttk
import numpy
from custom_ui.camera_controls import cameraControls
from custom_ui.camera_view import cameraView

root = Tk()
frm = ttk.Frame(root, padding=10)
frm.grid()

# print(allRed)
cameraControls(frm, root)
cameraView(frm, root)

root.mainloop()
# from tkinter import *
# from random import choice
# colors = ['red', 'green', 'blue']
# root = Tk()
# root.geometry("100x100")
# button = Button(root, text="Button1", command=lambda: root.configure(bg=choice(colors)))
# button.pack()
# root.mainloop()