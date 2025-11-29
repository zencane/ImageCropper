from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk
import random

root = Tk()
root.title("Image Resizer")

pic = None


def upload():
    global pic
    fileTypes = [("Image files", "*.png")]
    path = filedialog.askopenfilename(filetypes=fileTypes)
    print('Selected:', path)
    img = Image.open(path)
    img = img.resize(resizer(img))
    pic = ImageTk.PhotoImage(img)
    filePath.set(path)
    confirmButton.config(state=NORMAL)

def resizer(image):
    global imageWidth, imageHeight
    width, height = image.size
    maxDimension = max(width, height)
    scale = frameWidth / maxDimension
    imageWidth = int(width * scale)
    imageHeight = int(height * scale)
    print(f"Resized dimensions: {imageWidth}x{imageHeight}")
    return (int(width * scale), int(height * scale))

def confirm():
    print("Setting images on label")
    CropperToolCanvas.create_image(0, 0, image=pic, anchor=NW)
    confirmButton.config(state=DISABLED)
    FileInput.config(state=NORMAL)
    fileName.set(resolvefileName())
    TL = CropperToolCanvas.create_image(0, 0, image=TLarrow, anchor=NW)
    BR = CropperToolCanvas.create_image(304, 304, image=BRarrow, anchor=SE)
    CropperToolCanvas.bind("<B1-Motion>", move)

def resolvefileName():
    path = filePath.get()
    name = path.split('/')[-1]
    randomnums = random.randint(100,999)
    name = name.split('.')[0] + f"_cropped_{randomnums}.png"
    print(name)
    return name

def crop():
    print("Cropping image")
    # get top left x,y of TL corner
    # get bottom right x,y of BR corner
    # perform crop on original image
    # display cropped image
    cropButton.config(state=DISABLED)
    FileInput.config(state=DISABLED)

def move(event):
    global TLarrow, BRarrow, TLarrowX, TLarrowY, BRarrowX, BRarrowY
    if event.x < 10:
        event.x = 10
    if event.y < 10:
        event.y = 10
    if event.x > imageWidth:
        event.x = imageWidth
    if event.y > imageHeight:
        event.y = imageHeight
    if abs(event.x - TLarrowX) < abs(event.x - BRarrowX):
        TLarrowX = event.x-10
        TLarrowY = event.y-10
        cropperToolTLXY.set(f"({TLarrowX}, {TLarrowY})")
    else:
        BRarrowX = event.x
        BRarrowY = event.y
        cropperToolBRXY.set(f"({BRarrowX}, {BRarrowY})")
    cropperToolXY.set(f"{cropperToolTLXY.get()} | {cropperToolBRXY.get()}")
    refreshImages()
    cropButton.config(state=NORMAL)
    
def refreshImages():
    global TLarrow, BRarrow, TLarrowX, TLarrowY, BRarrowX, BRarrowY
    CropperToolCanvas.delete("all")
    CropperToolCanvas.create_image(0, 0, image=pic, anchor=NW)
    CropperToolCanvas.create_image(TLarrowX, TLarrowY, image=TLarrow, anchor=NW)
    CropperToolCanvas.create_image(BRarrowX, BRarrowY, image=BRarrow, anchor=SE)

windowWidth = 640
frameWidth = 320


mainframe = ttk.Frame(root, padding=(20, 5, 20, 0))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

uploadframe = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=320, height=320)
uploadframe.grid(column=0, row=2, sticky=(N, W, E, S), columnspan=2)

imageframe = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=640, height=640)
imageframe.grid(column=0, row=5, sticky=(N, W, E, S), columnspan=2)
imageframe.config(cursor="crosshair")

tempImage = ImageTk.PhotoImage(Image.open('upload.png').resize((320, 320)))
imageWidth, imageHeight = 320, 320
TLarrow = ImageTk.PhotoImage(Image.open('TLarrow.png').resize((16, 16)))
BRarrow = ImageTk.PhotoImage(Image.open('BRarrow.png').resize((16, 16)))
TLarrowX = 0
TLarrowY = 0
BRarrowX = 320
BRarrowY = 320

fileName = StringVar()
filePath = StringVar()

fileName.set("")
filePath.set("")

cropperToolTLXY = StringVar()
cropperToolBRXY = StringVar()
cropperToolXY = StringVar()

titleLabel = ttk.Label(mainframe, text="Image Resizer", font=("Helvetica", 16))
fileLabel = ttk.Label(uploadframe, textvariable=filePath, wraplength=320, font=("Helvetica", 8))
uploadButton = ttk.Button(mainframe, text="Upload", command=lambda:upload())
confirmButton = ttk.Button(mainframe, text="Confirm", state=DISABLED, command=lambda:confirm())
CropperToolCanvas = Canvas(imageframe, width=320, height=320)
imageInCanvas = CropperToolCanvas.create_image(0, 0, image=tempImage, anchor=NW)
cropperToolTLXYLabel = ttk.Label(mainframe, textvariable=cropperToolTLXY, foreground="red", font=("Helvetica", 8))
cropperToolBRXYLabel = ttk.Label(mainframe, textvariable=cropperToolBRXY, foreground="blue", font=("Helvetica", 8))
FileInput = ttk.Entry(mainframe, textvariable=fileName, width=40, state=DISABLED)
cropButton = ttk.Button(mainframe, text="Crop", state=DISABLED, command=lambda:crop())


titleLabel.grid(column=0, row=1, sticky=N, columnspan=2)
fileLabel.grid(column=0, row=0, sticky=N)
uploadButton.grid(column=0, row=3, sticky=E)
confirmButton.grid(column=1, row=3, sticky=W)
CropperToolCanvas.grid(column=0, row=0, sticky=(N, W, E, S))
cropperToolTLXYLabel.grid(column=0, row=6, sticky=E)
cropperToolBRXYLabel.grid(column=1, row=6, sticky=W)
FileInput.grid(column=0, row=7, sticky=N, columnspan=2)
cropButton.grid(column=0, row=8, sticky=N, columnspan=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)	
mainframe.columnconfigure(2, weight=1)
imageframe.columnconfigure(3, weight=1)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=5)

root.mainloop()
