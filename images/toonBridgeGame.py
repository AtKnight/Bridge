import sys

from tkinter import *
#from tkinter import ttk
from PIL import Image, ImageTk

def get_suit_image(suit_str):
    if suit_str == 'spades':
        file_name = 'spade.jpg'
    elif suit_str == 'hearts':
        file_name = 'heart.jpg'
    elif suit_str == 'diamonds':
        file_name = 'diamond.jpg'
    elif suit_str == 'clubs':
        file_name = 'club.jpg'
    else:
        print(f'Suit {suit_str} does not exists.')
        sys.exit(1)

    image = Image.open(file_name)
    breedte, hoogte = image.size

    prefered_size = 128

    # Resize the image using resize() method
    factor = 0.2
    breedte = int(factor *  prefered_size)
    hoogte = int(factor * prefered_size)

    resize_image = image.resize((breedte, hoogte))

    return ImageTk.PhotoImage(resize_image)


 
# Create Tkinter Object
root = Tk()
root.configure(background='yellow')

lab_root1 = Label(root, text="Hello World!")
lab_root1.grid(row=0, column=0)

but_root1 = Button(root, text="Quit", command=root.destroy)
but_root1.grid(row=0, column=1)

game_frame = Frame(root, bg='blue', width=200, height = 600)
game_frame.grid(row=1, column=0, padx=10, pady=20)

#Row 1
Frame(game_frame, bg='red', width=200, height = 200).grid(row=1, column=0, padx=10, pady=20)

#empty_frame00 = Frame(game_frame, bg='red', width=200, height = 200)
#empty_frame00.grid(row=1, column=0, padx=10, pady=20)

#empty_label = Label(empty_frame00, bg='grey', text="Hier zeer brede tekst")
#empty_label.grid(row=1, column=1, padx=10, pady=20)

north_frame = Frame(game_frame, bg='white', width=200, height = 200)
north_frame.grid(row=1, column=1, padx=10, pady=20)

Frame(game_frame, bg='purple', width=200, height = 200).grid(row=1, column=2, padx=10, pady=20)

#Row 2

Frame(game_frame, bg='magenta', width=200, height = 200).grid(row=2, column=1, padx=10, pady=20)

#Row 3
Frame(game_frame, bg='green', width=200, height = 200).grid(row=3, column=0, padx=10, pady=20)

Frame(game_frame, bg='pink', width=200, height = 200).grid(row=3, column=2, padx=10, pady=20)

values= ['A', 'K', 'Q', 'J']
values.extend(list(range(10, 1, -1)))

row = 0
suit_labels = {}
value_labels = {}
for suit in ('spades', 'hearts', 'diamonds', 'clubs'):
    img = get_suit_image(suit)

    suit_labels[suit] = Label(north_frame, bg='white', image=img)
    suit_labels[suit].img = img
    suit_labels[suit].grid(column=0, row=row)

    column = 1
    for value in values:
        value_labels[suit + str(value)] = Label(north_frame, text=str(value),
                                                font=("Arial", 20), bg='white')
        value_labels[suit + str(value)].grid(row=row, column=column)

        column += 1
        
    row += 1

#"""

# Execute Tkinter
root.mainloop()
