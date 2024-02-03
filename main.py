from custom_ui.gui import GUI, ProgramConfig
from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
from thorlabs_utils.utils import MotorManager
from threading import Thread
from time import sleep
import numpy

camera_rgb_rescale = 0.25 # camera does not stick to rgb format

config = ProgramConfig(
    img_height = 1080,
    img_width = 1440,
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

device_id_mapping = { 
    "Yglass": "27600759",
    "Xglass": "27600799",
    "Y": config.motor_x,
    "X": config.motor_y,
    "Z": config.motor_z,
    "Camera": config.camera
}

init_img = numpy.zeros((config.img_width*config.img_height), dtype="uint8")
init_img = [[0, 0, 0] for _ in init_img]
init_img = numpy.reshape(init_img, (config.img_height,config.img_width,3)).astype("uint8")

with (
        KinesisMotor(device_id_mapping["Yglass"]) as y_motor,
        KinesisMotor(device_id_mapping["Xglass"]) as x_motor,
        KinesisMotor(device_id_mapping["Z"]) as z_motor,
        TLCamera.ThorlabsTLCamera(device_id_mapping["Camera"]) as camera
):
    motor_mngr = MotorManager(x_motor, y_motor, z_motor, 500)
    gui = GUI("Auto Mono Layer", lambda : print(""), motor_mngr).build(config, init_img)
    
    run_thread = True
    
    def update_img():
        sleep(5)
        
        while(run_thread):
            sleep(0.01)
            img = numpy.array(camera.snap() * camera_rgb_rescale).astype("uint8") # ThorLabs 'RGB' -> actual RGB
            gui.camera_view_panel.update_image(img)

    update_img_th = Thread(target=update_img, args=())
    
    motor_mngr.begin(lambda : gui.info_display.update_position(motor_mngr.current_position))
    update_img_th.start()
    gui.run()
    
    motor_mngr.finish()
    stop_thread = False

print("Finished")    