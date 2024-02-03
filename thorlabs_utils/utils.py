from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
import matplotlib.pyplot as mlp
from time import sleep
import cv2 as cv
import tensorflow as tf
import numpy as np
import json
from threading import Thread

class MotorManager:
    def __init__(self, x_motor: KinesisMotor, y_motor: KinesisMotor, z_motor: KinesisMotor, step: int):
        self.__motors = (x_motor, y_motor, z_motor)
        self.__step = step
        self.__mv_vector = (0, 0, 0) # (x, y, z)
        self.__running = False
        self.__th = Thread(target=self.__manage_motors, args=())
        self.current_position = (x_motor.get_position(), y_motor.get_position(), z_motor.get_position())
        self.__callback = None
        
    def start_x_up(self, e: None):
        self.__mv_vector = (1, 0, 0)
        
    def start_x_down(self, e: None):
        self.__mv_vector = (-1, 0, 0)
        
    def start_y_up(self, e: None):
        self.__mv_vector = (0, 1, 0)
        
    def start_y_down(self, e: None):
        self.__mv_vector = (0, -1, 0)
    
    def start_z_up(self, e: None):
        self.__mv_vector = (0, 0, 1)
        
    def start_z_down(self, e: None):
        self.__mv_vector = (0, 0, -1)
        
    def stop_all(self, e: None):
        self.__mv_vector = (0, 0, 0)
     
    def __manage_motors(self):
        self.__update_pos()
        
        while self.__running:
            for i in range(0, 3):
                if self.__mv_vector[i] == 0:
                    continue
                
                self.__motors[i].move_by(self.__mv_vector[i] * self.__step)
                self.__motors[i].wait_move()
                
            self.__update_pos()
        
            if self.__callback is not None:
                self.__callback()
                
            sleep(0.01)
            
    def __update_pos(self):
        self.current_position = (self.__motors[0].get_position(), self.__motors[1].get_position(), self.__motors[2].get_position())

    def begin(self, callback):
        self.__running = True
        self.__callback = callback
        self.__th.start()
        
    def finish(self):
        self.__running = False
        self.__mv_vector = (0, 0, 0)
        

# TODO remove
if (False):
    def move(motor: KinesisMotor, position):
        motor.move_to(position)
        motor.wait_move()

    config = None # TODO
    
    modelPath = config.ai_model
    model = tf.keras.models.load_model(modelPath)
    
    # must be adjusted before each start
    stepX = config.step_x # adjust motor step, about 3455 equals for 0.1mm
    stepY = config.step_y
    stepZ = config.step_z
    cameraExposureTime = config.exposure_ms / 1000 # seconds to wait for camrea to catch exposure
    startPoint = { "x": config.start_x, "y": config.start_y }
    endPoint = { "x": config.end_x, "y": config.end_y }
    
    def takeFocusedPicture(camera: TLCamera, zMotor: KinesisMotor):
        global stepZ
        
        # try to adjust focus by going up
        image, focus = tryAdjustFocus(camera, zMotor, stepZ)
        
        # try to adjust focus by going down
        newImage, newFocus = tryAdjustFocus(camera, zMotor, -1 * stepZ)
        
        # return initials
        return (image, focus) if focus > newFocus else (newImage, newFocus)
        
    def tryAdjustFocus(
        camera: TLCamera.ThorlabsTLCamera, 
        zMotor: KinesisMotor, 
        step: int
    ):
        global cameraExposureTime
        sleep(cameraExposureTime)
        
        # reference values
        previousPosition = zMotor.get_position()
        referenceImage = camera.snap()
        referenceFocus = cv.Laplacian(referenceImage, cv.CV_64F).var()
    
        while (True):
            sleep(cameraExposureTime)
            
            # update position
            move(zMotor, zMotor.get_position() + step)
            newPosition = zMotor.get_position()
            
            # break when motor cannot move
            if (newPosition == previousPosition):
                break
            
            # update new values
            newImage = camera.snap() 
            newFocus = cv.Laplacian(newImage, cv.CV_64F).var()
            
            # break when adjustment did not improve focus
            if (newFocus <= referenceFocus):
                move(zMotor, previousPosition)
                break
            
            # update reference values
            previousPosition = newPosition
            referenceImage = newImage
            referenceFocus = newFocus
            
            
        return referenceImage, referenceFocus
        
    def analysePicture(image):
        pass # tensorflow   
    
    def move_rm(motor: KinesisMotor, position):
        motor.move_to(position)
        motor.wait_move()
    #TLCamera.ThorlabsTLCamera("").set_exposure(800)
    #ThorlabsTLCamera("").set_color_format("rgb")
    with (
            KinesisMotor(deviceToIdMapping["Yglass"]) as yGlassMotor,
            KinesisMotor(deviceToIdMapping["Xglass"]) as xGlassMotor,
            KinesisMotor(deviceToIdMapping["Z"]) as zMotor,
            TLCamera.ThorlabsTLCamera(deviceToIdMapping["Camera"]) as camera
    ):
        #model.summary()
        #camera.set_exposure(0.8)
        #camera.set_color_format(color_output="rgb", color_space="srgb")
        
        ##print(camera.get_white_balance_matrix())
        
        img = camera.snap()
        img = tf.image.resize(img, (256, 256))
        img = np.array(img).astype("float32") * cameraRgbRescale
        #img /= img.max()
        #print(img.max())
        #img = np.array(img * 0.30).astype("uint8")
        
        
        #tf.keras.utils.save_img("123123.jpg", mlpImg)
        #f = tf.io.read_file("./123123.jpg")
        #img = tf.image.decode_image(f, 3)
        #img = tf.image.resize(img, (256, 256))
        #print(np.array(img).max())
        #cvImg = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        #cv.imwrite('bbb.png', cvImg)
        
        mlpImg = img / 255
        mlp.imshow(mlpImg) 
        mlp.show()
        
        img = tf.expand_dims(img, 0)
        result = model(img)
        print(result)
            
        # X-axis
        for posX in range(startPoint["x"], endPoint["x"], stepX):
            pass    
            # Y-axis
            for posY in range(startPoint["y"], endPoint["y"], stepY): 
                # image, focus = takeFocusedPicture(camera, zMotor)
                pass
                # move(yGlassMotor, posY)
                #print(f"{str(posX)},{str(posY)}")
                #sleep(0.5)
                #img = takeFocusedPicture()
                #analysePicture(img)
                # handle result - save image with positions            
                
            #move(xGlassMotor, posX)
    
    print("Finished.")