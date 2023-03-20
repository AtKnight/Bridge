from tkinter import *
#from tkinter import ttk
from PIL import Image, ImageTk
 
# Create Tkinter Object
root = Tk()

frm = Frame(root)
frm.grid()

Label(frm, text="Hello World!").grid(column=0, row=0)
Button(frm, text="Quit", command=root.destroy).grid(column=1, row=0)

values = list(range(2, 11))
values.extend(['jack', 'queen', 'king', 'ace'])

firstIndex = 2
step = 3
lastIndex = firstIndex + step

fileName = f'club.png'
image = Image.open(fileName)
breedte, hoogte = image.size

# Resize the image using resize() method
factor = 0.2
breedte = int(factor * breedte)
hoogte = int(factor * hoogte)

resize_image = image.resize((breedte, hoogte))

img = ImageTk.PhotoImage(resize_image)

# create label and add resize image
label1 = Label(frm, text="Hier zeer brede tekst", image=img)
label1.image = img  # Het is mij onbekend waarom img twee keer moet worden toegekend.
                    # https://python-course.eu/tkinter/labels-in-tkinter.php
                    # wekt de indruk dat gif zonder problemen kan worden getoond

label1.grid(column=0, row=1)

# Execute Tkinter
root.mainloop()
