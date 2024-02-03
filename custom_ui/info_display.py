from tkinter import *
from custom_ui.constants import DISPLAY_LABELS_BG
from custom_ui.constants import MAIN_WINDOW_BG

class InfoDisplay:
    def __init__(self, frame: Frame, win: Tk):
        self.__frame = frame
        self.__win = win
        
    def build(self):    
        label_width = 18
        
        Label(self.__frame, text="Current motor positions", background=MAIN_WINDOW_BG).grid(column=0, row=4, columnspan=5, pady=20)
        
        Label(self.__frame, text="X", background=MAIN_WINDOW_BG).grid(column=0, row=5)
        self.__x_label = Label(self.__frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
        self.__x_label.grid(column=1, row=5, columnspan=10)
        
        Label(self.__frame, text="Y", background=MAIN_WINDOW_BG).grid(column=0, row=6)
        self.__y_label = Label(self.__frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
        self.__y_label.grid(column=1, row=6, columnspan=10)
        
        Label(self.__frame, text="Z", background=MAIN_WINDOW_BG).grid(column=0, row=7)
        self.__z_label = Label(self.__frame, text=str(100), background=DISPLAY_LABELS_BG, width=label_width, anchor="e", justify="right")
        self.__z_label.grid(column=1, row=7, columnspan=10)
        
        return self
    
    def update_position(self, pos: tuple[int, int, int]):
        self.__x_label.config(text=str(pos[0]))
        self.__y_label.config(text=str(pos[1]))
        self.__z_label.config(text=str(pos[2]))