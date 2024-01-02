from tkinter import *
import numpy
from PIL import ImageTk, Image
import time
import asyncio
import threading

(height, width) = (270, 480)

allRed = numpy.zeros((width*height), dtype="uint8")
allRed = [[255, 0, 0, 255] for _ in allRed]
allRed = numpy.reshape(allRed, (height,width,4)).astype("uint8")
allRed = Image.fromarray(allRed).convert("RGB")

allBlue = numpy.zeros((width*height), dtype="uint8")
allBlue = [[0, 0, 255, 255] for _ in allBlue]
allBlue = numpy.reshape(allBlue, (height,width,4)).astype("uint8")
allBlue = Image.fromarray(allBlue).convert("RGB")

currentImg = True

def cameraView(frame: Frame, win: Tk):
    img = allRed

    img=ImageTk.PhotoImage(img)

    canvas = Canvas(frame, width=width, height=height)
    canvas.config(bg="white")
    canvas.grid(column=10, row=3)

    win.img = img
    img_container = canvas.create_image(width/2, height/2, image=img)

    def update_image():
        time.sleep(2)
        global currentImg, allRed, allBlue
        nextImg = allRed if not currentImg else allBlue
        nextImg = ImageTk.PhotoImage(nextImg)
        win.img = nextImg
        canvas.itemconfig(img_container, image=win.img)
        currentImg = not currentImg

    def update_image_background_thread():
        th = threading.Thread(target=update_image, args=())
        th.start()

    Button(text="swap img", command=update_image_background_thread).grid(column=10, row=10)