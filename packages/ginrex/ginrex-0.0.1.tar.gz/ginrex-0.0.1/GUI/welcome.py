from tkinter import Tk, Label, Button, Canvas, Entry
from rootmethod import rootMethod
import sys

sys.path.insert(1, "larch_app")
from larch_app import Sum


# create and edit the app
root = Tk()
root.title("ginRex")
# root.iconbitmap("./Path/file")
root.configure(bg="#E9CCA4")
root.geometry("500x500")

# welcome message
labl = Label(root, text="Welcome to ginRex", bg="#E9CCA4", fg="#000000", pady=10)
labl.pack()

# create root button
rootBtn = Button(root, text="back home", fg="#000000", command=rootMethod)
rootBtn.pack()

# create readData button
readDataBtn = Button(root, text="read Data", fg="#000000")
readDataBtn.pack(pady=5)


# create UI entry box
canvas1 = Canvas(root, width=400, height=300, relief="raised")
canvas1.pack()

entryLabel1 = Label(root, text="Enter variable one:")
entryLabel1.config(font=("helvetica", 10))
canvas1.create_window(200, 100, window=entryLabel1)
entry1 = Entry(root)
test = Sum.Sum(entry1.get())
canvas1.create_window(200, 140, window=entry1)

# canvas2 = Canvas(root, width=400, height=300, relief="raised")
# canvas2.pack()

# entryLabel2 = Label(root, text="Enter variable two:")
# entryLabel2.config(font=("helvetica", 10))
# canvas2.create_window(200, 100, window=entryLabel2)
# entry2 = Entry(root)
# canvas2.create_window(200, 140, window=entry2)

# test Button
testBtn = Button(root, text="foo", command=test)
canvas1.create_window(200, 180, window=testBtn)

root.mainloop()
