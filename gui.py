import tkinter
import tkinter.font
from settings import SafeLightSettings
from PIL import ImageTk
from typing import Callable

class SafeLightGui:
    settings: SafeLightSettings
    
    tkWindow: tkinter.Tk
    
    font: tkinter.font.Font
    
    btnMain: tkinter.Button
    btnMask: tkinter.Button
    btnFinal: tkinter.Button
    
    sliderExposure: tkinter.Scale
    sliderThreshold: tkinter.Scale
    sliderBlur: tkinter.Scale
    sliderStrength: tkinter.Scale
    def __init__(self, imageWidth: float, settings: SafeLightSettings):
        self.settings = settings
        
        self.tkWindow = tkinter.Tk()
        self.tkWindow.title("SafeLight")
        
        self.font = tkinter.font.Font(family="Default", size = 48)
        
        self.btnMain = tkinter.Button(self.tkWindow)
        self.btnMain.grid(row=0, column=0)

        self.btnMask = tkinter.Button(self.tkWindow)
        self.btnMask.grid(row=0, column=1)

        self.btnFinal = tkinter.Button(self.tkWindow)
        self.btnFinal.grid(row=0, column=2)
        
        self.sliderExposure = self.addSlider(0, 2, 0.01, settings.exposure, "Exposure", 1, 3 * imageWidth)
        self.sliderThreshold = self.addSlider(0, 1, 0.01, settings.threshold, "Threshold", 2, 3 * imageWidth)
        self.sliderBlur = self.addSlider(0, 100, 0.1, settings.blurRadius, "Blur", 3, 3 * imageWidth)
        self.sliderStrength = self.addSlider(0, 10, 0.1, settings.strength, "Strength", 4, 3 * imageWidth)
        
    def addSlider(self, start: float, end: float, step: float, value: float, label: str, row: int, width: float):
        slider = tkinter.Scale(self.tkWindow, 
                                from_= start,
                                to = end,
                                resolution=step,
                                length=width,
                                font = self.font, 
                                label=label, 
                                orient=tkinter.HORIZONTAL,)
        slider.set(value)
        slider.grid(row = row, column=0, columnspan=3)
        return slider
        
    def SetCallback(self, callableFunc: Callable[[any], None]):
        self.sliderExposure.configure(command = callableFunc)
        self.sliderExposure.command = callableFunc
        self.sliderThreshold.configure(command = callableFunc)
        self.sliderThreshold.command = callableFunc
        self.sliderBlur.configure(command = callableFunc)
        self.sliderBlur.command = callableFunc
        self.sliderStrength.configure(command = callableFunc)
        self.sliderStrength.command = callableFunc

    def UpdateMain(self, image: ImageTk.PhotoImage):
        self.btnMain.configure(image=image)
        self.btnMain.image = image
    
    def UpdateMask(self, image: ImageTk.PhotoImage):
        self.btnMask.configure(image=image)
        self.btnMask.image = image
    
    def UpdateFinal(self, image: ImageTk.PhotoImage):
        self.btnFinal.configure(image=image)
        self.btnFinal.image = image