import os
from threading import Thread

from custom_ui.auto_controls import ProcessConfig
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
from tensorflow import _logging
_logging.disable()

from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
from time import sleep
import cv2 as cv
import tensorflow as tf
import numpy as np

class AutoProcess:
    def __init__(self, on_error, camera_rgb_scale):
        self.__on_error = on_error
        self.__camera_rgb_scale = camera_rgb_scale
        self.__requested_break = False
        self.is_running = False

    def stop(self):
        self.__requested_break = True

    def begin(
            self,
            config: ProcessConfig, 
            camera: TLCamera.ThorlabsTLCamera, 
            motor_x: KinesisMotor, 
            motor_y: KinesisMotor, 
            motor_z: KinesisMotor,
            output_dir_path: str
        ):
        
        self.__requested_break = False

        def run_in_background_thread():
            self.is_running = True

            try:
                model = tf.keras.models.load_model(config.ai_model)
                camera_exposure_time = config.exposure_ms / 1000
                
                # X-axis
                for pos_x in range(config.start[0], config.end[0], config.step_x):
                    if self.__requested_break: return
                    
                    # Y-axis
                    self.__move(motor_x, pos_x)

                    for pos_y in range(config.start[1], config.end[1], config.step_y): 
                        if self.__requested_break: return
                        
                        self.__move(motor_y, pos_y)
                        image, _ = self.__take_focused_picture(camera, motor_z, camera_exposure_time, config.step_z)

                        if (self.__contains_mono_layer(model, image, self.__camera_rgb_scale, config.treshold)):
                            AutoProcess.__save_image(image, os.path.join(output_dir_path, f"{pos_x}_{pos_y}.png"))

            except Exception as err:
                if self.__requested_break:
                    self.__on_error(err)
            
            self.is_running = False

        th = Thread(target=run_in_background_thread, args=())
        th.start()

    def __take_focused_picture(self, camera: TLCamera, zMotor: KinesisMotor, camera_exposure_time: float, step_z: int):
        # try to adjust focus by going up
        image, focus = self.__try_adjust_focus(camera, zMotor, camera_exposure_time, step_z)
        
        # try to adjust focus by going down
        newImage, newFocus = self.__try_adjust_focus(camera, zMotor, camera_exposure_time, -1 * step_z)
        
        # return initials
        return (image, focus) if focus > newFocus else (newImage, newFocus)
        
    def __try_adjust_focus(
        self,
        camera: TLCamera.ThorlabsTLCamera, 
        motor_z: KinesisMotor,
        camera_exposure_time: float,
        step_z: int
    ):
        sleep(camera_exposure_time)
        
        # reference values
        previousPosition = motor_z.get_position()
        referenceImage = camera.snap()
        referenceFocus = cv.Laplacian(referenceImage, cv.CV_64F).var()

        while (not self.__requested_break):
            sleep(camera_exposure_time)
            
            # update position
            AutoProcess.__move(motor_z, motor_z.get_position() + step_z)
            newPosition = motor_z.get_position()
            
            # break when motor cannot move
            if (newPosition == previousPosition):
                break
            
            # update new values
            newImage = camera.snap() 
            newFocus = cv.Laplacian(newImage, cv.CV_64F).var()
            
            # break when adjustment did not improve focus
            if (newFocus <= referenceFocus):
                AutoProcess.__move(motor_z, previousPosition)
                break
            
            # update reference values
            previousPosition = newPosition
            referenceImage = newImage
            referenceFocus = newFocus
            
            
        return referenceImage, referenceFocus

    @staticmethod
    def __save_image(image, path):
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        cv.imwrite(path, image)

    @staticmethod  
    def __contains_mono_layer(model, image, camera_rgb_scale: int, treshold: float) -> bool:
        image = tf.image.resize(image, (256, 256))
        image = np.array(image * camera_rgb_scale).astype("float32")
        image = tf.expand_dims(image, 0)
        result = model(image)

        return result[1] >= treshold

    @staticmethod  
    def __move(motor: KinesisMotor, position):
        motor.move_to(position)
        motor.wait_move()