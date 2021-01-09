import tkinter as tk
from tkinter import ttk
import os.path
import reg_family as rf
import enter_recipe as er
from center_window import *


class ChoseFamily:
    def __init__(self, master):
        if os.path.isfile("families"):
            families_file = open("families", "r")
            saved_families = families_file.readlines()
            for i in range(len(saved_families)):
                saved_families[i] = saved_families[i][:-1]
            families_file.close()
        else:
            families_file = open("families", 'w+')
            saved_families = []

        self.master = master
        self.master.geometry('270x170')
        center(self.master)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1, 2, 3], minsize=40)
        self.frame.grid_columnconfigure([0, 1, 2], minsize=65)

        self.selectLbl = tk.Label(self.frame, text="Select a Family")
        self.enterBtn = tk.Button(self.frame, text="Enter", command=self.enter_recipe)
        self.RegisterBtn = tk.Button(master=self.frame, text="Register", command=self.reg_family)
        self.family = tk.StringVar()
        self.family_select = ttk.Combobox(self.frame, textvariable=self.family)
        self.family_select['values'] = saved_families
        self.family_select.current()

        self.selectLbl.grid(row=0, column=1)
        self.enterBtn.grid(row=2, column=1)
        self.RegisterBtn.grid(row=3, column=1)
        self.family_select.grid(row=1, column=1)

    def reg_family(self):
        self.frame.destroy()
        rf.RegisterFamily(self.master)

    def enter_recipe(self):
        if self.family.get() != "":
            self.frame.destroy()
            er.RecipeSelect(self.master, self.family.get())

