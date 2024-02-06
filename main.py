from custom_ui.gui import GUI, ProgramConfig
#from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
#from thorlabs_utils.utils import MotorManager
from threading import Thread
from time import sleep
import numpy
from json import dump, load
from custom_ui.auto_controls import ProcessConfig
# from thorlabs_utils.process import process
from os import mkdir, path

camera_rgb_scale = 0.25 # camera does not stick to rgb format
config_file_path = ".config.json"

config = None
with open(config_file_path, "r") as config_file:
    deserialized = load(config_file)

    config = ProgramConfig(
        img_height = deserialized["img_height"],
        img_width = deserialized["img_width"],
        start_x = deserialized["start_x"],
        start_y = deserialized["start_y"],
        end_x = deserialized["end_x"],
        end_y = deserialized["end_y"],
        exposure_ms = deserialized["exposure_ms"],
        step_x = deserialized["step_x"],
        step_y = deserialized["step_y"],
        step_z = deserialized["step_z"],
        motor_x = deserialized["motor_x"],
        motor_y = deserialized["motor_y"],
        motor_z = deserialized["motor_z"],
        camera = deserialized["camera"],
        ai_model = deserialized["ai_model"],
        output_dir = deserialized["output_dir"],
        treshold = deserialized["treshold"],
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

# with (
#         KinesisMotor(device_id_mapping["Yglass"]) as y_motor,
#         KinesisMotor(device_id_mapping["Xglass"]) as x_motor,
#         KinesisMotor(device_id_mapping["Z"]) as z_motor,
#         TLCamera.ThorlabsTLCamera(device_id_mapping["Camera"]) as camera
# ):
#     motor_mngr = MotorManager(x_motor, y_motor, z_motor, 500)
#     gui = GUI("Auto Mono Layer", lambda : print(""), motor_mngr).build(config, init_img)
    
#     run_thread = True
    
#     def update_img():
#         sleep(5)
        
#         while(run_thread):
#             sleep(0.01)
#             img = numpy.array(camera.snap() * camera_rgb_rescale).astype("uint8") # ThorLabs 'RGB' -> actual RGB
#             gui.camera_view_panel.update_image(img)

#     update_img_th = Thread(target=update_img, args=())
    
#     motor_mngr.begin(lambda : gui.info_display.update_position(motor_mngr.current_position))
#     update_img_th.start()
#     gui.run()
    
#     motor_mngr.finish()
#     stop_thread = False

# print("Finished")    

def on_start(process_config: ProcessConfig):
    global config, camera_rgb_scale

    with open(config_file_path, "w+") as config_file:
        config.start_x = process_config.start[0]    
        config.start_y = process_config.start[1]    
        config.end_x = process_config.end[0]    
        config.end_y = process_config.end[1]    
        config.exposure_ms = process_config.exposure_time_ms    
        config.step_x = process_config.steps[0]    
        config.step_y = process_config.steps[1]
        config.step_z = process_config.steps[2]
        config.output_dir = process_config.output_dir_path

        dump(config.__dict__, config_file, indent=4)
    
    if not path.exists(config.output_dir):
        mkdir(config.output_dir)

    # process(config, None, None, None, None, camera_rgb_scale, config.output_dir, lambda err : print(err))

def on_stop():
    pass

gui = GUI(
    "Auto Mono Layer",
    on_start=on_start, 
    on_stop=on_stop,
    motor_mngr=None
).build(config, init_img)
gui.run()