from tkinter import *
from custom_ui.constants import BUTTONS_BG, BUTTONS_BG_PRESSED, DISPLAY_LABELS_BG

def autoControls(frame: Frame, win: Tk, onSetStartPosPressed, onSetEndPosPressed):
    label_width = 18
    buttons_width = 7
    buttons_height = 3

    xStartVariable = StringVar()
    xEndVariable = StringVar()
    yStartVariable = StringVar()
    yEndVariable = StringVar()
    stepVariable = StringVar()

    Label(frame, text="Autonomic process controls").grid(column=0, row=16, columnspan=8, pady=2)

    Label(frame, text="Start position").grid(column=0, row=17, columnspan=8, pady=2)
    Label(frame, text="X").grid(column=0, row=18)
    xStartEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=xStartVariable, validate="focusout", validatecommand=lambda : print(xStartVariable.get()))
    xStartEntry.grid(column=1, row=18, columnspan=10)
    Label(frame, text="Y").grid(column=0, row=19)
    yStartEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=xEndVariable, validate="focusout", validatecommand=lambda : print(xEndVariable.get()))
    yStartEntry.grid(column=1, row=19, columnspan=10)

    Label(frame, text="End position").grid(column=0, row=20, columnspan=8, pady=2)
    Label(frame, text="X").grid(column=0, row=21)
    xEndEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=yStartVariable, validate="focusout", validatecommand=lambda : print(yStartVariable.get()))
    xEndEntry.grid(column=1, row=21, columnspan=10)
    Label(frame, text="Y").grid(column=0, row=22)
    yEndEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=yEndVariable, validate="focusout", validatecommand=lambda : print(yEndVariable.get()))
    yEndEntry.grid(column=1, row=22, columnspan=10)

    Label(frame, text="",).grid(column=0, row=23, columnspan=6, pady=1)
    Label(frame, text="Step").grid(column=0, row=24)
    stepEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=stepVariable, validate="focusout", validatecommand=lambda : print(stepVariable.get()))
    stepEntry.grid(column=1, row=24, columnspan=10)

    # TODO
    def onSetStartClicked():
        xStartVariable.set("1000")
        onSetStartPosPressed()

    Label(frame, text="",).grid(column=0, row=8, columnspan=6, pady=1)
    
    startBtn = Button(frame, text="Set\nstart\npostion", command=onSetStartClicked, background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    startBtn.grid(column=0, row=9, columnspan=3)
    
    endBtn = Button(frame, text="Set\nend\npostion", command=onSetEndPosPressed, background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    endBtn.grid(column=4, row=9, columnspan=3)

    

    # endPosLabel = Label(frame, text="End position")
    # endPosLabel.grid(column=0, row=18, columnspan=8, pady=2)
