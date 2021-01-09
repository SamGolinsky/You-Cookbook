import tkinter as tk
import enter_recipe as er
from center_window import *


class ReviewRecipe:
    def __init__(self, master, family, recipe_name):
        self.master = master
        self.master.geometry('235x65')
        center(self.master)
        self.family = family
        self.recipe_name = recipe_name

        self.fam_file = open(f"{self.family}", "r+")
        self.fam_data = self.fam_file.readlines()
        self.fam_file.close()

        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1, 2], minsize=20)
        self.frame.grid_columnconfigure([0, 1, 2], minsize=80)

        self.name_index = None
        for i in range(len(self.fam_data)):
            if self.fam_data[i] == f"{self.recipe_name}\n":
                self.name_index = i

        self.reviewLbl = tk.Label(self.frame, text='Rate it Baby').grid(row=0, column=0, sticky='we', columnspan=3)
        self.goodBtn = tk.Button(self.frame, text='Good', command=self.__good).grid(row=1, column=0)
        self.mehBtn = tk.Button(self.frame, text='Meh', command=self.__meh).grid(row=1, column=1)
        self.badBtn = tk.Button(self.frame, text='Bad', command=self.__bad).grid(row=1, column=2)

    def __good(self):
        self.fam_file = open(f"{self.family}", "w+")
        self.fam_data[self.name_index] = self.fam_data[self.name_index][:-1] + ' :)\n'
        self.fam_file.writelines(self.fam_data)
        self.fam_file.close()
        self.frame.destroy()
        er.RecipeSelect(self.master, self.family)

    def __meh(self):
        self.fam_file = open(f"{self.family}", "w+")
        self.fam_data[self.name_index] = self.fam_data[self.name_index][:-1] + ' :|\n'
        self.fam_file.writelines(self.fam_data)
        self.fam_file.close()
        self.frame.destroy()
        er.RecipeSelect(self.master, self.family)

    def __bad(self):
        self.fam_file = open(f"{self.family}", "w+")
        self.fam_data[self.name_index] = self.fam_data[self.name_index][:-1] + ' :(\n'
        self.fam_file.writelines(self.fam_data)
        self.fam_file.close()
        self.frame.destroy()
        er.RecipeSelect(self.master, self.family)

