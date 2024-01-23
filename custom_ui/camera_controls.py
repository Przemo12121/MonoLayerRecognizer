from tkinter import *
from custom_ui.constants import BUTTONS_BG_PRESSED, BUTTONS_BG, MAIN_WINDOW_BG

class CameraControlsListener:
    def __init__(self,
                 on_x_up_pressed, on_x_up_released,
                 on_x_down_pressed, on_x_down_released,
                 on_y_up_pressed, on_y_up_released,
                 on_y_down_pressed, on_y_down_released,
                 on_z_up_pressed, on_z_up_released,
                 on_z_down_pressed, on_z_down_released,
                ) -> None:
        self.on_x_up_pressed = on_x_up_pressed
        self.on_x_up_released = on_x_up_released
        
        self.on_x_down_pressed = on_x_down_pressed
        self.on_x_down_released = on_x_down_released
        
        self.on_y_up_pressed = on_y_up_pressed
        self.on_y_up_released = on_y_up_released
        
        self.on_y_down_pressed = on_y_down_pressed
        self.on_y_down_released = on_y_down_released

        self.on_z_up_pressed = on_z_up_pressed
        self.on_z_up_released = on_z_up_released
        
        self.on_z_down_pressed = on_z_down_pressed
        self.on_z_down_released = on_z_down_released


def cameraControls(frame: Frame, win: Tk, listener: CameraControlsListener):
    buttons_width = 1
    buttons_height = 1

    Label(frame, text="Move camera", background=MAIN_WINDOW_BG).grid(column=0, row=0, columnspan=5)

    btn_up = Button(frame, text="Y+", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_up.grid(column=1, row=1)

    btn_down = Button(frame, text="Y-", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_down.grid(column=1, row=2)

    btn_left = Button(frame, text="X-", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_left.grid(column=0, row=2)

    btn_right = Button(frame, text="X+", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_right.grid(column=2, row=2)

    btn_zplus = Button(frame, text="H", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_zplus.grid(column=5, row=1)

    btn_zminus = Button(frame, text="L", background=BUTTONS_BG, width=buttons_width, height=buttons_height, activebackground=BUTTONS_BG_PRESSED)
    btn_zminus.grid(column=5, row=2)

    btn_up.bind('<ButtonPress-1>', listener.on_y_up_pressed)
    btn_up.bind('<ButtonRelease-1>', listener.on_y_up_released)
    
    btn_down.bind('<ButtonPress-1>', listener.on_y_down_pressed)
    btn_down.bind('<ButtonRelease-1>', listener.on_y_down_released)
    
    btn_right.bind('<ButtonPress-1>', listener.on_x_up_pressed)
    btn_right.bind('<ButtonRelease-1>', listener.on_x_up_released)
    
    btn_left.bind('<ButtonPress-1>', listener.on_x_down_pressed)
    btn_left.bind('<ButtonRelease-1>', listener.on_x_down_released)

    btn_zplus.bind('<ButtonPress-1>', listener.on_z_up_pressed)
    btn_zplus.bind('<ButtonRelease-1>',listener.on_z_up_released)

    btn_zminus.bind('<ButtonPress-1>', listener.on_z_down_pressed)
    btn_zminus.bind('<ButtonRelease-1>',listener.on_z_down_released)

    def handle_keyboard_press(e):
        btn_pressed = None
        if e.keysym == "Up":
            btn_pressed = btn_up
            listener.on_y_up_pressed(None)
        elif e.keysym == "Down":
            btn_pressed = btn_down
            listener.on_y_down_pressed(None)
        elif e.keysym == "Left":
            btn_pressed = btn_left
            listener.on_x_down_pressed(None)
        elif e.keysym == "Right":
            btn_pressed = btn_right
            listener.on_x_up_pressed(None)
        elif e.keysym == "h":
            btn_pressed = btn_zplus
            listener.on_z_up_pressed(None)
        elif e.keysym == "l":
            btn_pressed = btn_zminus
            listener.on_z_down_pressed(None)
        else:
            return
        
        btn_pressed.config(bg=BUTTONS_BG_PRESSED)

    def handle_keyboard_release(e):
        btn_pressed = None
        if e.keysym == "Up":
            btn_pressed = btn_up
            listener.on_y_up_released(None)
        elif e.keysym == "Down":
            btn_pressed = btn_down
            listener.on_y_down_released(None)
        elif e.keysym == "Left":
            btn_pressed = btn_left
            listener.on_x_down_released(None)
        elif e.keysym == "Right":
            btn_pressed = btn_right
            listener.on_x_up_released(None)
        elif e.keysym == "h":
            btn_pressed = btn_zplus
            listener.on_z_up_released(None)
        elif e.keysym == "l":
            btn_pressed = btn_zminus
            listener.on_z_down_released(None)
        else:
            return
        
        btn_pressed.config(bg=BUTTONS_BG)

    win.bind('<KeyPress>', handle_keyboard_press)
    win.bind('<KeyRelease>', handle_keyboard_release)