from tkinter import *
from custom_ui.constants import BUTTONS_BG_PRESSED, BUTTONS_BG, MAIN_WINDOW_BG

class CameraControls:
    def __init__(self, frame: Frame, win: Tk, listener):
        self.__frame = frame
        self.__win = win
        self.__listener = listener
        self.__buttons_enabled = True

    def build(self):
        buttons_width = 3
        buttons_height = 1

        Label(self.__frame, text="Move camera", background=MAIN_WINDOW_BG).grid(column=0, row=0, columnspan=5)

        self.__btn_up = Button(self.__frame, text="Y+", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_up.grid(column=1, row=1)

        self.__btn_down = Button(self.__frame, text="Y-", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_down.grid(column=1, row=2)

        self.__btn_left = Button(self.__frame, text="X-", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_left.grid(column=0, row=2)

        self.__btn_right = Button(self.__frame, text="X+", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_right.grid(column=2, row=2)

        self.__btn_zplus = Button(self.__frame, text="H", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_zplus.grid(column=5, row=1)

        self.__btn_zminus = Button(self.__frame, text="L", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
        self.__btn_zminus.grid(column=5, row=2)

        # self.__btn_up.bind('<ButtonPress-1>', self.__listener.start_y_up)
        # self.__btn_up.bind('<ButtonRelease-1>', self.__listener.stop_all)
        
        # self.__btn_down.bind('<ButtonPress-1>', self.__listener.start_y_down)
        # self.__btn_down.bind('<ButtonRelease-1>', self.__listener.stop_all)
        
        # self.__btn_right.bind('<ButtonPress-1>', self.__listener.start_x_up)
        # self.__btn_right.bind('<ButtonRelease-1>', self.__listener.stop_all)
        
        # self.__btn_left.bind('<ButtonPress-1>', self.__listener.start_x_down)
        # self.__btn_left.bind('<ButtonRelease-1>', self.__listener.stop_all)

        # self.__btn_zplus.bind('<ButtonPress-1>', self.__listener.start_z_up)
        # self.__btn_zplus.bind('<ButtonRelease-1>',self.__listener.stop_all)

        # self.__btn_zminus.bind('<ButtonPress-1>', self.__listener.start_z_down)
        # self.__btn_zminus.bind('<ButtonRelease-1>',self.__listener.stop_all)

        def handle_keyboard_press(e):
            if not self.__buttons_enabled:
                return

            self.__btn_pressed = None
            # if e.keysym == "Up":
            #     self.__btn_pressed = self.__btn_up
            #     self.__listener.start_y_up(None)
            # elif e.keysym == "Down":
            #     self.__btn_pressed = self.__btn_down
            #     self.__listener.start_y_down(None)
            # elif e.keysym == "Left":
            #     self.__btn_pressed = self.__btn_left
            #     self.__listener.start_x_down(None)
            # elif e.keysym == "Right":
            #     self.__btn_pressed = self.__btn_right
            #     self.__listener.start_x_up(None)
            # elif e.keysym == "h":
            #     self.__btn_pressed = self.__btn_zplus
            #     self.__listener.start_z_up(None)
            # elif e.keysym == "l":
            #     self.__btn_pressed = self.__btn_zminus
            #     self.__listener.start_z_down(None)
            # else:
            #     return
            
            # self.__btn_pressed.config(state="active")

        def handle_keyboard_release(e):
            if not self.__buttons_enabled:
                return
            
            self.__btn_pressed = None
            if e.keysym == "Up":
                self.__btn_pressed = self.__btn_up
            elif e.keysym == "Down":
                self.__btn_pressed = self.__btn_down
            elif e.keysym == "Left":
                self.__btn_pressed = self.__btn_left
            elif e.keysym == "Right":
                self.__btn_pressed = self.__btn_right
            elif e.keysym == "h":
                self.__btn_pressed = self.__btn_zplus
            elif e.keysym == "l":
                self.__btn_pressed = self.__btn_zminus
            else:
                return
            
            # self.__listener.stop_all(None)
            self.__btn_pressed.config(state="normal")

        self.__win.bind('<KeyPress>', handle_keyboard_press)
        self.__win.bind('<KeyRelease>', handle_keyboard_release)

    def switch_buttons(self, enabled: bool):
        self.__buttons_enabled = enabled

        state = "normal" if enabled else "disabled"
        self.__btn_up.config(state=state)
        self.__btn_down.config(state=state)
        self.__btn_left.config(state=state)
        self.__btn_right.config(state=state)
        self.__btn_zminus.config(state=state)
        self.__btn_zplus.config(state=state)

