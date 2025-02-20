import tkinter.font
import rawpy
import imageio
from PIL import Image, ImageTk, ImageEnhance, ImageOps, ImageChops, ImageFilter
import tkinter
from gui import SafeLightGui
from settings import SafeLightSettings

IMG_WIDTH = 512
IMG_HEIGHT = 512

path = 'test.RAF'
raw = rawpy.imread(path)
rgb = raw.postprocess()
print(raw.raw_image)

# Create pillow image from npy array
image = Image.fromarray(rgb.astype('uint8'), 'RGB')
image = image.resize((IMG_WIDTH, IMG_HEIGHT))

def TransformMainImage(inputImage: Image, settings: SafeLightSettings) -> Image:
    localImage = ImageEnhance.Brightness(inputImage).enhance(settings.exposure)
    return localImage

def TransformMaskImage(inputImage: Image, settings: SafeLightSettings) -> Image:
    lutBase = [i if i > settings.threshold * 255 else 0 for i in range(256) ]
    grayscale = inputImage.convert('L')
    localImage = grayscale.point(lutBase)
    blurred = localImage.filter(ImageFilter.GaussianBlur(settings.blurRadius))
    localImage = ImageOps.colorize(blurred, (0,0,0), (255,0,0))
    return localImage

def TransformFinalImage(baseImage: Image, maskImage: Image, settings: SafeLightSettings) -> Image:
    offsetMask = ImageEnhance.Brightness(maskImage).enhance(settings.strength)
    localImage = ImageChops.screen(baseImage, offsetMask)
    return localImage

# Create settings object
settings: SafeLightSettings = SafeLightSettings()

gui: SafeLightGui = SafeLightGui(IMG_WIDTH, settings)

def UpdateUi():
    newImage = TransformMainImage(image, settings)
    newMask = TransformMaskImage(newImage, settings)
    newFinal = TransformFinalImage(newImage, newMask, settings)
    gui.UpdateMain(ImageTk.PhotoImage(newImage))
    gui.UpdateMask(ImageTk.PhotoImage(newMask))
    gui.UpdateFinal(ImageTk.PhotoImage(newFinal))

def Callback_SliderUpdate(e: tkinter.Event):
    # Debounce the input events
    numUpdates: int = 0
    if (gui.sliderExposure.get() != settings.exposure):
        settings.exposure = gui.sliderExposure.get()
        numUpdates += 1
    
    if (gui.sliderThreshold.get() != settings.threshold):
        settings.threshold = gui.sliderThreshold.get()
        numUpdates += 1
        
    if (gui.sliderBlur.get() != settings.blurRadius):
        settings.blurRadius = gui.sliderBlur.get()
        numUpdates += 1
        
    if (gui.sliderStrength.get() != settings.strength):
        settings.strength = gui.sliderStrength.get()
        numUpdates += 1
        
    if (numUpdates == 0):
        return
    
    UpdateUi()
  

gui.SetCallback(Callback_SliderUpdate)
UpdateUi()

gui.tkWindow.mainloop()

#imageio.imsave('test.tiff', rgb)