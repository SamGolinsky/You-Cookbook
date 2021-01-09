import tkinter as tk
from tkinter import ttk
import view_recipe as vr
import io
from center_window import *


class RecipeSelect:
    def __init__(self, master, family):
        self.family = family
        self.fam_file = open(f"{self.family}", 'r+')
        self.fam_data = self.fam_file.readlines()
        self.fam_file.close()
        self.saved_recipes = []
        for i in range(len(self.fam_data)):
            if self.fam_data[i][:2] == ">>":
                self.saved_recipes.append(self.fam_data[i+1][:-1])

        self.master = master
        self.master.geometry('340x90')
        center(self.master)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1], minsize=40)
        self.frame.grid_columnconfigure([0, 1, 2], minsize=80)

        self.selectLbl = tk.Label(self.frame, text="Select Recipe: ").grid(row=0, column=0, columnspan=2)
        self.continueBtn = tk.Button(self.frame, text="Continue", command=self.__continue)
        self.enterNewBtn = tk.Button(self.frame, text="Enter New Recipe", command=self.__new_recipe)
        self.recipeName = tk.StringVar()
        self.recipe_select = ttk.Combobox(self.frame, textvariable=self.recipeName)
        self.recipe_select['values'] = self.saved_recipes
        self.recipe_select.current()

        self.continueBtn.grid(row=1, column=2)
        self.enterNewBtn.grid(row=1, column=0, columnspan=2)
        self.recipe_select.grid(row=0, column=2)

    def __new_recipe(self):
        self.frame.destroy()
        NewRecipe(self.master, self.family)

    def __continue(self):
        self.frame.destroy()
        vr.ViewRecipe(self.master, self.family, self.recipeName.get())


class NewRecipe:
    def __init__(self, master, family):
        self.master = master
        self.master.geometry('260x245')
        center(self.master)
        self.family = family
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1, 2, 3, 4, 5], minsize=40)
        self.frame.grid_columnconfigure([0, 1, 2, 3], minsize=80)

        self.ingredientList = []
        self.processList = []

        self.recipeLbl = tk.Label(self.frame, text="Recipe Name: ").grid(row=0, column=0)
        self.ingredientLbl = tk.Label(self.frame, text="Ingredients: ").grid(row=1, column=0)
        self.processLbl = tk.Label(self.frame, text="Process: ").grid(row=2, column=0)
        self.cookTimeLbl = tk.Label(self.frame, text="Cook Time: ").grid(row=3, column=0)
        self.portionsLbl = tk.Label(self.frame, text="Yields: ").grid(row=4, column=0)

        self.recipeName = tk.StringVar()
        self.recipeNtr = tk.Entry(self.frame, textvariable=self.recipeName).grid(row=0, column=1, columnspan=2, sticky='we')
        self.ingredient_idv = tk.StringVar()
        self.ingredientNtr = tk.Entry(self.frame, textvariable=self.ingredient_idv)
        self.ingredientNtr.grid(row=1, column=1, columnspan=2, sticky='we')
        self.process_idv = tk.StringVar()
        self.processNtr = tk.Entry(self.frame, textvariable=self.process_idv)
        self.processNtr.grid(row=2, column=1, columnspan=2, sticky='we')
        self.cookTime_idv = tk.StringVar()
        self.cookTimeNtr = tk.Entry(self.frame, textvariable=self.cookTime_idv).grid(row=3, column=1, columnspan=2, sticky='we')
        self.portions_idv = tk.StringVar()
        self.portionsNtr = tk.Entry(self.frame, textvariable=self.portions_idv).grid(row=4, column=1, columnspan=2, sticky='we')

        self.continueBtn = tk.Button(self.frame, text="Continue", command=self.__continue).grid(row=5, column=1, columnspan=2)

    def __continue(self):
        self.fam_file = io.open(f"{self.family}", "a+", encoding="utf-8")
        self.fam_file.write(f">>\n{self.recipeName.get()}\n")
        self.fam_file.write("INGREDIENTS\n")
        self.fam_file.write(self.ingredient_idv.get()+'\n')
        self.fam_file.write("PROCESS\n")
        self.fam_file.write(self.process_idv.get()+'\n')
        self.fam_file.write(f"COOK TIME\n{self.cookTime_idv.get()}\nYIELD\n{self.portions_idv.get()}\n<<\n")
        self.fam_file.close()
        self.frame.destroy()
        vr.ViewRecipe(self.master, self.family, self.recipeName.get())

