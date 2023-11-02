from pylablib.devices.Thorlabs import kinesis, KinesisMotor, TLCamera
import matplotlib.pyplot as mlp
from time import sleep
import cv2 as cv


deviceToIdMapping = { 
    "Yglass": "27600759",
    "Xglass": "27600799",
    "Y": "27600801",
    "X": "27261134",
    "Z": "27600749",
    "Camera": "20806"
}

# must be adjusted before each start
stepX = 1000 # adjust motor step, about 3455 equals for 0.1mm
stepY = 1000
stepZ = 1000
cameraExposureTime = 0.180 # seconds to wait for camrea to catch exposure
startPoint = { "x": 0, "y": 0 }
endPoint = { "x": 5000, "y": 5000 }

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

with (
        KinesisMotor(deviceToIdMapping["Yglass"]) as yGlassMotor,
        KinesisMotor(deviceToIdMapping["Xglass"]) as xGlassMotor,
        KinesisMotor(deviceToIdMapping["Z"]) as zMotor,
        TLCamera.ThorlabsTLCamera(deviceToIdMapping["Camera"]) as camera
):
    #print(focus)
    
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