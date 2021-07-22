import tkinter
from tkinter import *
from tkinter import filedialog as fd
from PIL import Image, ImageTk
from PIL import ImageGrab

#   GLOBAL Variable
root_file = ''


# Function to save watermark image as .png
def getter():
    x = root.winfo_rootx() + canvas.winfo_x()
    y = root.winfo_rooty() + canvas.winfo_y()
    x1 = x + canvas.winfo_width()
    y1 = y + canvas.winfo_height()
    print(root_file)
    filename = str.split(root_file, '.')[0]+'_WM.png'
    print(filename)
    ImageGrab.grab().crop((x, y, x1, y1)).save(filename)


# Function to resize watermark image
def resize(image, width):
    base_width = width
    w_percent = (base_width / float(image.size[0]))
    h_size = int((float(image.size[1]) * float(w_percent)))
    img = image.resize((base_width, h_size), Image.ANTIALIAS)
    return img


# function to load image to received watermark
def get_filename():
    global root_file

    root_file = fd.askopenfilename()
    original = Image.open(root_file)
    if original.size[0] > 800 or original.size[1] > 800:
        ratio = original.size[0] / original.size[1]
        if original.size[0] >= original.size[1]:  # Picture is wider that high
            original = resize(original, 800)
        else:
            original = resize(original, int(800 * ratio))

    original = ImageTk.PhotoImage(original)
    label1.configure(image=original)
    label1.image = original
    place_watermark('avatar.png')


# function to load in a new watermark
def get_watermark():
    filename = fd.askopenfilename()
    place_watermark(filename)


# function to place watermark in the lower right corner of image
def place_watermark(image):
    width = label1.image.width()
    height = label1.image.height()
    watermark = Image.open(image)
    watermark = watermark.convert("RGBA")
    watermark = resize(watermark, int(width * .25))
    watermark.putalpha(100)

    water_mark = ImageTk.PhotoImage(watermark)
    label2.configure(image=water_mark)
    label2.image = water_mark
    label2.place(x=width - watermark.size[0], y=height - watermark.size[1])


root = Tk()
root.title("Watermark Photos")

canvas = Canvas(root, width=999, height=800)
label1 = tkinter.Label(canvas, image='')
label2 = tkinter.Label(canvas, image='')

button1 = Button(text="add File", command=get_filename)
button2 = Button(text="change watermark", command=get_watermark)
button3 = Button(text="Save", command=getter)
button4 = Button(text="quit")

canvas.grid(row=1, column=0, columnspan=4)
label1.pack()
label2.pack()
button1.grid(row=0, column=0)
button2.grid(row=0, column=1)
button3.grid(row=0, column=2)
button4.grid(row=0, column=3)

root.mainloop()
