import threading
import time
from tkinter import *
from tkinter import ttk
import numpy
from custom_ui.camera_controls import CameraControls, CameraControlsListener
from custom_ui.camera_view import CameraView
from custom_ui.info_display import infoDisplay
from custom_ui.auto_controls import AutoControls, ProcessConfig
from custom_ui.constants import MAIN_WINDOW_BG

# TODO: devices integration
(height, width) = (860, 1240)
allRed = numpy.zeros((width*height), dtype="uint8")
allRed = [[255, 0, 0, 255] for _ in allRed]
allRed = numpy.reshape(allRed, (height,width,4)).astype("uint8")

root = Tk(className="Auto Mono Layer")
frmStyle = ttk.Style()
frmStyle.configure('My.TFrame', background=MAIN_WINDOW_BG)
frm = ttk.Frame(root, padding=10, style='My.TFrame')
frm.grid()

process_config = ProcessConfig((0, 0), (1000, 1000), 100, 500)

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

camera_controls_panel = CameraControls(frm, root, cameraListener)
camera_controls_panel.build()

def start():
    camera_controls_panel.switch_buttons(False)
    print("Process started")

def end():
    camera_controls_panel.switch_buttons(True)
    print("Process ended")

auto_controls_panel = AutoControls(
    frm, root, 
    motor_position_provider=lambda : (120, 130), 
    on_start=start, 
    on_stop=end
)
auto_controls_panel.build(process_config)

camera_view_panel = CameraView(frm, root, height, width)
camera_view_panel.build(allRed)

root.mainloop()