#!/usr/bin/env python3

import larch
from larch.xafs import autobk
import sys
from tkinter import Label, Canvas

sys.path.insert(2, "./GUI/welcome.py")
from welcome import root


class Sum:
    def __init__(self, var_a, var_b, var_ui):
        self.var_a = var_a
        self.var_b = var_b
        self.var_ui = var_ui

    def sum(self, entry):
        self.var_ui = entry

        canvas1 = Canvas(root, width=400, height=300, relief="raised")
        canvas1.pack()

        label3 = Label(
            root, text="The sum is" + self.var_ui + " is:", font=("helvetica", 10)
        )
        canvas1.create_window(200, 210, window=label3)

        label4 = Label(
            root, text=float(self.var_ui) ** 0.5, font=("helvetica", 10, "bold")
        )
        canvas1.create_window(200, 230, window=label4)

        return self.var_a + self.var_b


# ui_sum = Sum(float(input("Variable one")), float(input("Variable two")))
# print("Your sum is:", ui_sum.sum())
