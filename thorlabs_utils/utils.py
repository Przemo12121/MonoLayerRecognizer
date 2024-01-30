from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
import matplotlib.pyplot as mlp
from time import sleep
import cv2 as cv
import tensorflow as tf
import numpy as np
import json


cameraRgbRescale = 0.3 # camera does not stick to rgb format

def replace_picture(old, camera, target_width, target_height):
    img = camera.snap()
    print(img.shape)
    img = tf.image.resize(img, (target_width, target_height))
    img = np.array(img).astype("float32") * cameraRgbRescale
    
    shape = old.shape
    for i in range(0, shape[0]):
        for j in range(0, shape[1]):
            old[i][j][0] = img[i][j][0]
            old[i][j][1] = img[i][j][1]
            old[i][j][2] = img[i][j][2]


# TODO remove
if (False):
    deviceToIdMapping = { 
        "Yglass": "27600759",
        "Xglass": "27600799",
        "Y": config.motor_x,
        "X": config.motor_y,
        "Z": config.motor_z,
        "Camera": config.camera
    }
    
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
    
    def move(motor: KinesisMotor, position):
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