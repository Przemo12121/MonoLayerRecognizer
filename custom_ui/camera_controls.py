from tkinter import *

def cameraControls(frame: Frame, win: Tk):
    buttons_clr = "lightgray"
    Label(frame, border=10).grid(column=4, row=0)
    Label(frame, text="Move camera").grid(column=0, row=0)

    btn_up = Button(frame, text="Y+", background=buttons_clr)
    btn_up.grid(column=2, row=1)

    btn_down = Button(frame, text="Y-", background=buttons_clr)
    btn_down.grid(column=2, row=2)

    btn_left = Button(frame, text="X-", background=buttons_clr)
    btn_left.grid(column=1, row=2)

    btn_right = Button(frame, text="X+", background=buttons_clr)
    btn_right.grid(column=3, row=2)

    btn_zplus = Button(frame, text="H", background=buttons_clr)
    btn_zplus.grid(column=5, row=1)

    btn_zminus = Button(frame, text="L", background=buttons_clr)
    btn_zminus.grid(column=5, row=2)

    btn_up.bind('<ButtonPress-1>', lambda _ : print("Holding..."))
    btn_up.bind('<ButtonRelease-1>',lambda _ : print("Released!"))
    
    btn_down.bind('<ButtonPress-1>', lambda _ : print("Holding..."))
    btn_down.bind('<ButtonRelease-1>',lambda _ : print("Released!"))
    
    btn_right.bind('<ButtonPress-1>', lambda _ : print("Holding..."))
    btn_right.bind('<ButtonRelease-1>',lambda _ : print("Released!"))
    
    btn_left.bind('<ButtonPress-1>', lambda _ : print("Holding left..."))
    btn_left.bind('<ButtonRelease-1>',lambda _ : print("Released left!"))

    btn_zplus.bind('<ButtonPress-1>', lambda _ : print("Holding left..."))
    btn_zplus.bind('<ButtonRelease-1>',lambda _ : print("Released left!"))

    btn_zminus.bind('<ButtonPress-1>', lambda _ : print("Holding left..."))
    btn_zminus.bind('<ButtonRelease-1>',lambda _ : print("Released left!"))

    def handle_keyboard_press(e):
        btn_pressed = None
        if e.keysym == "Up":
            btn_pressed = btn_up
        elif e.keysym == "Down":
            btn_pressed = btn_down
        elif e.keysym == "Left":
            btn_pressed = btn_left
        elif e.keysym == "Right":
            btn_pressed = btn_right
        elif e.keysym == "h":
            btn_pressed = btn_zplus
        elif e.keysym == "l":
            btn_pressed = btn_zminus
        else:
            return
        
        btn_pressed.config(bg="blue")

    def handle_keyboard_release(e):
        btn_pressed = None
        if e.keysym == "Up":
            btn_pressed = btn_up
        elif e.keysym == "Down":
            btn_pressed = btn_down
        elif e.keysym == "Left":
            btn_pressed = btn_left
        elif e.keysym == "Right":
            btn_pressed = btn_right
        elif e.keysym == "h":
            btn_pressed = btn_zplus
        elif e.keysym == "l":
            btn_pressed = btn_zminus
        else:
            return
        
        btn_pressed.config(bg=buttons_clr)

    win.bind('<KeyPress>', handle_keyboard_press)
    win.bind('<KeyRelease>', handle_keyboard_release)