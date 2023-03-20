from tkinter import *

ws = Tk()
ws.title('PythonGuides')


img = PhotoImage(file='PNG-cards-1.3/king_of_diamonds2.png')
Label(
    ws,
    image=img
).pack()

ws.mainloop()
