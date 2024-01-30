from custom_ui.gui import GUI, ProgramConfig
from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
from thorlabs_utils.utils import replace_picture
from threading import Thread
from time import sleep
import numpy

config = ProgramConfig(
    img_height = 860,
    img_width = 1260,
    start_x = 0,
    start_y = 0,
    end_x = 5000,
    end_y = 5000,
    exposure_ms = 180,
    step_x = 1000,
    step_y = 1000,
    step_z = 1000,
    motor_x = "27261134",
    motor_y = "27600801",
    motor_z = "27600749",
    camera = "20806",
    ai_model = "./models/monoLayerRecognizer_new"
)

deviceToIdMapping = { 
    "Yglass": "27600759",
    "Xglass": "27600799",
    "Y": config.motor_x,
    "X": config.motor_y,
    "Z": config.motor_z,
    "Camera": config.camera
}

init_img = numpy.zeros((config.img_width*config.img_height), dtype="uint8")
init_img = [[0, 0, 0, 255] for _ in init_img]
init_img = numpy.reshape(init_img, (config.img_height,config.img_width,4)).astype("uint8")

with (
        KinesisMotor(deviceToIdMapping["Yglass"]) as yGlassMotor,
        KinesisMotor(deviceToIdMapping["Xglass"]) as xGlassMotor,
        KinesisMotor(deviceToIdMapping["Z"]) as zMotor,
        TLCamera.ThorlabsTLCamera(deviceToIdMapping["Camera"]) as camera
):
    gui = GUI("Auto Mono Layer", lambda : print("")).build(config, init_img)
    
    def update_img():
        global init_img
        delay = config.exposure_ms / 1000
        
        while(True):
            sleep(delay)
            print("next")
            replace_picture(init_img, camera, config.img_width, config.img_width)
            gui.camera_view_panel.update_image(init_img)
    
    update_img_th = Thread(target=update_img, args=())
    
    update_img_th.start()
    gui.run()
    print("XD")
    