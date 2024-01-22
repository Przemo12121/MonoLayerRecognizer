from tkinter import *
from custom_ui.constants import DISPLAY_LABELS_BG

def infoDisplay(frame: Frame, win: Tk):
    label_width = 18
    
    Label(frame, text="Current motor positions").grid(column=0, row=4, columnspan=5, pady=20)
    
    Label(frame, text="X").grid(column=0, row=5)
    xLabel = Label(frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
    xLabel.grid(column=1, row=5, columnspan=10)
    
    Label(frame, text="Y").grid(column=0, row=6)
    yLabel = Label(frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
    yLabel.grid(column=1, row=6, columnspan=10)
    
    Label(frame, text="Z").grid(column=0, row=7)
    zLabel = Label(frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
    zLabel.grid(column=1, row=7, columnspan=10)

    def xPosListener(pos: int):
        xLabel.config(text=str(pos))

    def yPosListener(pos: int):
        yLabel.config(text=str(pos))
        
    def zPosListener(pos: int):
        zLabel.config(text=str(pos))

    return (xPosListener, yPosListener, zPosListener)