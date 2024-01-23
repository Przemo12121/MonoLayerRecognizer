from tkinter import *
import tkinter.messagebox
from custom_ui.constants import BUTTONS_BG, BUTTONS_BG_PRESSED, DISPLAY_LABELS_BG, MAIN_WINDOW_BG

def showErrors(fields: list[str]):
     errList = [f"- {field}." for field in fields]
     errList = '\n'.join(errList)
     tkinter.messagebox.showerror("Invalid input data", f"Below fields have invalid input data:\n\n{errList}\n\nThey must be natural number.")

def autoControls(frame: Frame, win: Tk, motorPositionProvider, onStart, onStop):
    label_width = 18
    buttons_width = 7
    buttons_height = 3

    xStartVariable = StringVar()
    xEndVariable = StringVar()
    yStartVariable = StringVar()
    yEndVariable = StringVar()
    stepVariable = StringVar()
    exposureVariable = StringVar()

    Label(frame, text="Autonomic process controls", background=MAIN_WINDOW_BG).grid(column=0, row=16, columnspan=8, pady=2)

    Label(frame, text="Start position", background=MAIN_WINDOW_BG).grid(column=0, row=17, columnspan=8, pady=2)
    Label(frame, text="X", background=MAIN_WINDOW_BG).grid(column=0, row=18)
    xStartEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=xStartVariable)
    xStartEntry.grid(column=1, row=18, columnspan=10)
    Label(frame, text="Y", background=MAIN_WINDOW_BG).grid(column=0, row=19)
    yStartEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=yStartVariable)
    yStartEntry.grid(column=1, row=19, columnspan=10)

    Label(frame, text="End position", background=MAIN_WINDOW_BG).grid(column=0, row=20, columnspan=8, pady=2)
    Label(frame, text="X", background=MAIN_WINDOW_BG).grid(column=0, row=21)
    xEndEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=xEndVariable)
    xEndEntry.grid(column=1, row=21, columnspan=10)
    Label(frame, text="Y", background=MAIN_WINDOW_BG).grid(column=0, row=22)
    yEndEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=yEndVariable)
    yEndEntry.grid(column=1, row=22, columnspan=10)

    Label(frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=23, columnspan=6, pady=1)
    Label(frame, text="Step", background=MAIN_WINDOW_BG).grid(column=0, row=24)
    stepEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=label_width, justify="right", textvariable=stepVariable)
    stepEntry.grid(column=1, row=24, columnspan=10)
    Label(frame, text="Exposure [ms]", background=MAIN_WINDOW_BG).grid(column=0, row=25, columnspan=2)
    exposureEntry = Entry(frame, background=DISPLAY_LABELS_BG, width=int(label_width/2), justify="right", textvariable=exposureVariable)
    exposureEntry.grid(column=2, row=25, columnspan=7)

    def onSetStartClicked():
        (x, y) = motorPositionProvider()
        xStartVariable.set(str(x))
        yStartVariable.set(str(y))

    def onSetEndClicked():
        (x, y) = motorPositionProvider()
        xEndVariable.set(str(x))
        yEndVariable.set(str(y))

    Label(frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=8, columnspan=6, pady=1)
    
    setStartBtn = Button(frame, text="Set\nstart\npostion", command=onSetStartClicked, background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    setStartBtn.grid(column=0, row=9, columnspan=3)
    
    setEndBtn = Button(frame, text="Set\nend\npostion", command=onSetEndClicked, background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    setEndBtn.grid(column=4, row=9, columnspan=3)
    
    Label(frame, text="", background=MAIN_WINDOW_BG).grid(column=0, row=26, columnspan=6, pady=4)
    buttons_height = 1
    buttons_width = 3
    startBtn = Button(frame, text="Start", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    startBtn.grid(column=1, row=27, columnspan=1)
    stopBtn = Button(frame, text="Stop", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    stopBtn.grid(column=4, row=27, columnspan=1)
    stopBtn.config(state="disabled")
    
    def startBtnCommand():
        err = []
        if not xStartVariable.get().isdigit():
            err.append("X coordinate of start position")
        if not yStartVariable.get().isdigit():
            err.append("Y coordinate of start position")
        if not xEndVariable.get().isdigit():
            err.append("X coordinate of start position")
        if not yEndVariable.get().isdigit():
            err.append("Y coordinate of end position")
        if not stepVariable.get().isdigit():
            err.append("Camera step")
        if not exposureVariable.get().isdigit():
            err.append("Camera exposure time")

        if len(err) > 0:
            showErrors(err)
            return

        startBtn.config(state="disabled")
        stopBtn.config(state="normal")
        onStart()

    def stopBtnCommand():
            startBtn.config(state="normal")
            stopBtn.config(state="disabled")
            onStop()

    startBtn.config(command=startBtnCommand)
    stopBtn.config(command=stopBtnCommand)