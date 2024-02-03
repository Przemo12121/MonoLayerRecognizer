import threading
import time
from tkinter import *
from tkinter import ttk
import numpy
from custom_ui.camera_controls import CameraControls
from custom_ui.camera_view import CameraView
from custom_ui.info_display import InfoDisplay
from custom_ui.auto_controls import AutoControls, ProcessConfig
from custom_ui.constants import MAIN_WINDOW_BG

class ProgramConfig:
    def __init__(self, img_height, img_width, start_x, start_y, end_x, end_y, exposure_ms, step_x, step_y, step_z, motor_x, motor_z, motor_y, camera, ai_model):
        self.img_height = img_height
        self.img_width = img_width
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.exposure_ms = exposure_ms
        self.step_x = step_x
        self.step_y = step_y
        self.step_z = step_z
        self.motor_x = motor_x
        self.motor_y = motor_y
        self.motor_z = motor_z
        self.camera = camera
        self.ai_model = ai_model

class GUI:
    def __init__(self, title, on_save_config, motor_mngr):
        self.__on_save_config = on_save_config
        self.__root = Tk(className="Auto Mono Layer")
        self.__root.resizable(False, False)
        self.__motor_mngr = motor_mngr
        self.info_display = None

    def build(self, config: ProgramConfig, init_img):    
        (height, width) = (config.img_height, config.img_width)
        
        frmStyle = ttk.Style()
        frmStyle.configure('My.TFrame', background=MAIN_WINDOW_BG)
        frm = ttk.Frame(self.__root, padding=10, style='My.TFrame')
        frm.grid()
        
        process_config = ProcessConfig((config.start_x, config.start_y), (config.end_x, config.end_y), config.step_x, config.exposure_ms)
        
        self.info_display = InfoDisplay(frm, self.__root).build()
        
        camera_controls_panel = CameraControls(frm, self.__root, self.__motor_mngr)
        camera_controls_panel.build()
        
        def start():
            camera_controls_panel.switch_buttons(False)
            print("Process started")
        
        def end():
            camera_controls_panel.switch_buttons(True)
            print("Process ended")
        
        auto_controls_panel = AutoControls(
            frm, self.__root, 
            motor_position_provider=lambda : self.__motor_mngr.current_position, 
            on_start=start, 
            on_stop=end
        )
        auto_controls_panel.build(process_config)
        
        self.camera_view_panel = CameraView(frm, self.__root, height, width)
        self.camera_view_panel.build(init_img)
        
        return self
        
    def run(self):
        self.__root.mainloop()