from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from PIL import Image, ImageTk

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
    filename.set(path)
    confirmButton.config(state=NORMAL)
    #root.geometry("640x640")

def resizer(image):
    width, height = image.size
    maxDimension = max(width, height)
    scale = frameWidth / maxDimension
    print(width*scale, height*scale)
    return (int(width * scale), int(height * scale))

def confirm():
    print("Setting image on label")
    imageLabel.config(image=pic)
    imageLabel.image = pic
    confirmButton.config(state=DISABLED)

def crop():
    print("Cropping image")
    #imagelabel.configure(image=upload_image)
    cropButton.config(state=DISABLED)

def selectVertices():
    print("Selecting vertices")
    cropButton.config(state=NORMAL)

windowWidth = 640
frameWidth = 320


mainframe = ttk.Frame(root, padding=(20, 5, 20, 0))
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))

uploadframe = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=320, height=320)
uploadframe.grid(column=0, row=2, sticky=(N, W, E, S), columnspan=2)

imageframe = ttk.Frame(mainframe, borderwidth=2, relief="sunken", width=640, height=640)
imageframe.grid(column=0, row=5, sticky=(N, W, E, S), columnspan=2)

tempImage = ImageTk.PhotoImage(Image.open('upload.png').resize((320, 320)))
filename = StringVar()
filename.set("No file selected")


titleLabel = ttk.Label(mainframe, text="Image Resizer", font=("Helvetica", 16))
fileLabel = ttk.Label(uploadframe, textvariable=filename, wraplength=320, font=("Helvetica", 8))
uploadButton = ttk.Button(mainframe, text="Upload", command=lambda:upload())
confirmButton = ttk.Button(mainframe, text="Confirm", state=DISABLED, command=lambda:confirm())
imageLabel = ttk.Label(imageframe, image=tempImage, anchor=SE)
cropButton = ttk.Button(mainframe, text="Crop", state=DISABLED, command=lambda:crop())


titleLabel.grid(column=0, row=1, sticky=N, columnspan=2)
fileLabel.grid(column=0, row=0, sticky=N)
uploadButton.grid(column=0, row=3, sticky=E)
confirmButton.grid(column=1, row=3, sticky=W)
imageLabel.grid(column=0, row=0, sticky=(N, W, E, S))
cropButton.grid(column=0, row=6, sticky=N, columnspan=2)

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)	
mainframe.columnconfigure(2, weight=1)
imageframe.columnconfigure(3, weight=1)

for child in mainframe.winfo_children(): 
    child.grid_configure(padx=10, pady=5)

root.mainloop()
