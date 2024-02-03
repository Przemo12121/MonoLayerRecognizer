from tkinter import *
from PIL import ImageTk, Image

class CameraView:
    def __init__(self, frame: Frame, win: Tk, img_height: int, img_width: int):
        self.__frame = frame
        self.__win = win
        self.__img_height = img_height
        self.__img_width = img_width
        self.__img = None
        
    def build(self, init_img: tuple[tuple[tuple[int,int,int,int]]]):
        self.__img = Image.fromarray(init_img).convert("RGB")

        self.__img=ImageTk.PhotoImage(self.__img)

        self.__canvas = Canvas(self.__frame, width=self.__img_width/2, height=self.__img_height/2)
        self.__canvas.config(bg="white")
        self.__canvas.grid(column=60, row=2, rowspan=1000, columnspan=2, padx=20)

        self.__img_container = self.__canvas.create_image(self.__img_width/4, self.__img_height/4, image=self.__img)
        self.__canvas.scale("all", 0, 0, 0.5, 0.5)

    def update_image(self, img: tuple[tuple[tuple[int,int,int]]]):
        img = Image.fromarray(img, mode="RGB")
        img = ImageTk.PhotoImage(img)
        self.__img = img    
        self.__canvas.itemconfig(self.__img_container, image=self.__img)