from tkinter import *
from tkinter import ttk
from custom_ui.camera_controls import cameraControls, CameraControlsListener
from custom_ui.camera_view import cameraView
from custom_ui.info_display import infoDisplay
from custom_ui.auto_controls import autoControls
from custom_ui.constants import MAIN_WINDOW_BG

root = Tk(className="Auto Mono Layer")
frmStyle = ttk.Style()
frmStyle.configure('My.TFrame', background=MAIN_WINDOW_BG)
frm = ttk.Frame(root, padding=10, style='My.TFrame')
frm.grid()

# TODO device
xV = 100
yV = 100
zV = 100
def xUpListener(_):
    global xV
    xV += 10
    x(xV)    
def xDownListener(_):
    global xV
    xV -= 10
    x(xV)    
def yUpListener(_):
    global yV
    yV += 10
    y(yV)    
def yDownListener(_):
    global yV
    yV -= 10
    y(yV)    
def zUpListener(_):
    global zV
    zV += 10
    z(zV)    
def zDownListener(_):
    global zV
    zV -= 10
    z(zV)    

def nil(_):
    pass

x, y, z = infoDisplay(frm, root)

cameraListener = CameraControlsListener(
    on_x_up_pressed=xUpListener,
    on_x_down_pressed=xDownListener,
    on_y_up_pressed=yUpListener,
    on_y_down_pressed=yDownListener,
    on_z_up_pressed=zUpListener,
    on_z_down_pressed=zDownListener,
    on_x_up_released=nil,
    on_y_up_released=nil,
    on_z_up_released=nil,
    on_x_down_released=nil,
    on_y_down_released=nil,
    on_z_down_released=nil,
)

cameraControls(frm, root, cameraListener)
autoControls(
    frm, root, 
    motorPositionProvider=lambda : (120, 130), 
    onStart=lambda : print("Process started"), 
    onStop=lambda : print("Process ended")
)
cameraView(frm, root)

root.mainloop()