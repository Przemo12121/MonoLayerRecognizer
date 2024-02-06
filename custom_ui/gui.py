from tkinter import *
from tkinter import ttk
from custom_ui.camera_controls import CameraControls
from custom_ui.camera_view import CameraView
from custom_ui.info_display import InfoDisplay
from custom_ui.auto_controls import AutoControls, ProcessConfig
from custom_ui.constants import MAIN_WINDOW_BG

class ProgramConfig:
    def __init__(self, img_height, img_width, start_x, start_y, end_x, end_y, exposure_ms, step_x, step_y, step_z, motor_x, motor_z, motor_y, camera, ai_model, output_dir, treshold):
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
        self.output_dir = output_dir
        self.treshold = treshold

class GUI:
    def __init__(self, title, on_start, on_stop, motor_mngr):
        self.__on_start = on_start
        self.__on_stop = on_stop
        self.__root = Tk(className=title)
        self.__root.resizable(False, False)
        self.__motor_mngr = motor_mngr
        self.info_display = None

    def build(self, config: ProgramConfig, init_img):    
        (height, width) = (config.img_height, config.img_width)
        
        frmStyle = ttk.Style()
        frmStyle.configure('My.TFrame', background=MAIN_WINDOW_BG)
        frm = ttk.Frame(self.__root, padding=10, style='My.TFrame')
        frm.grid()
        
        process_config = ProcessConfig(
            start=(config.start_x, config.start_y), 
            end=(config.end_x, config.end_y), 
            steps=(config.step_x, config.step_y, config.step_z), 
            exposure_time_ms=config.exposure_ms,
            treshold=config.treshold,
            output_dir_path=config.output_dir
        )

        self.info_display = InfoDisplay(frm, self.__root).build()
        
        camera_controls_panel = CameraControls(frm, self.__root, self.__motor_mngr)
        camera_controls_panel.build()
        
        def start(config: ProcessConfig):
            camera_controls_panel.switch_buttons(False)
            self.__on_start(config)
        
        def end():
            camera_controls_panel.switch_buttons(True)
            self.__on_stop()
        
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