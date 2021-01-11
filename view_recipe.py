import tkinter as tk
from tkinter import ttk
import string_scale as ss
import review_recipe as rr
from center_window import *

scale_values = [0.25, 0.5, 0.75, 1, 1.25, 1.5, 1.75, 2, 2.5, 3, 3.5, 4, 4.5, 5,
                6, 7, 8, 9, 10, 15, 20, 25, 30, 40, 50]
measurement_units = ['teaspoon', 'teaspoons', 't', 'tsp', 'tablespoon', 'tablespoons', 'tbs', 'tbsp', 'fluid ounce',
                     'fluid ounces', 'fl oz', 'gill', 'gills', 'cup', 'cups', 'pint', 'pints', 'pt', 'quart', 'quarts',
                     'qt', 'gallon', 'gallons', 'gal', 'ml', 'l', 'dl', 'pound', 'pounds', 'lb', 'lbs', 'ounce',
                     'ounces', 'oz', 'mg', 'g', 'kg', 'mm', 'cm', 'm', 'inch', 'in', '"']


class ViewRecipe:
    def __init__(self, master, family, recipe_name):
        self.master = master
        self.family = family
        self.recipe_name = recipe_name

        self.fam_file = open(f"{self.family}", "r+")
        self.fam_data = self.fam_file.readlines()
        self.fam_file.close()
        self.recipe_index, self.ingredient_index, self.process_index, self.cooktime_index, self.yield_index = 0, 0, 0, 0, 0
        for j in range(len(self.fam_data)):
            if self.fam_data[j] == f"{self.recipe_name}\n":
                self.recipe_index = j
                count = 0
                for i in range(j, len(self.fam_data)):
                    if self.fam_data[i] == "INGREDIENTS\n":
                        self.ingredient_index = i
                        count += 1
                    if self.fam_data[i] == "PROCESS\n":
                        self.process_index = i
                        count += 1
                    if self.fam_data[i] == "COOK TIME\n":
                        self.cooktime_index = i
                        count += 1
                    if self.fam_data[i] == "YIELD\n":
                        self.yield_index = i
                        count += 1
                    if count == 4:
                        break
        row_num = []
        count = 0
        for i in range(1 + self.process_index, self.cooktime_index):
            for word in self.fam_data[i].split():
                for char in word:
                    if char == '.' and not(48 <= ord(word[0]) <= 57):
                        row_num.append(count)
                        count += 1
            if self.fam_data[i].split():
                row_num.append(count)
                count += 1
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure((row_num + [len(row_num) + 1]), minsize=20)
        self.frame.grid_columnconfigure([0, 1, 2, 3], minsize=80)
        self.master.geometry('')
        # self.master.geometry(f'{self.master.winfo_screenwidth()}x{self.master.winfo_screenheight()-40}')
        # center(self.master)

        self.processFrame = tk.Frame(self.frame)
        self.processFrame.grid(row=2, column=4, rowspan=(len(row_num)))
        self.processFrame.grid_rowconfigure((row_num + [len(row_num) + 1]), minsize=20)
        self.processFrame.grid_columnconfigure([0, 1, 2], minsize=80)

        self.titleLbl = tk.Label(self.frame, text=f"Family: {self.family}\tRecipe: {self.recipe_name}"). \
            grid(row=0, column=0, columnspan=6)
        self.scaleVar = tk.StringVar()
        self.scale_select = ttk.Combobox(self.frame, textvariable=self.scaleVar)
        self.scale_select['values'] = scale_values
        self.scale_select.current(3)
        self.scale_select.grid(row=2, column=1, sticky='e')

        self.scaleBtn = tk.Button(self.frame, text='Scale!', command=self.__scale).grid(row=2, column=2, sticky='w')

        self.reviewBtn = tk.Button(self.frame, text="Continue", command=self.__review).grid(row=len(row_num) + 2, column=0
                                                                                          , columnspan=6)
        self.grow_pageLbl = tk.Label(self.frame, text='').grid(row=len(row_num) + 3, column=0)

        self.ingredientLbl = tk.Label(self.frame, text="Ingredients").grid(row=1, column=0, columnspan=3)
        self.nums = []
        self.units = []
        for i in range(self.ingredient_index + 1, self.process_index):
            num_str = ''
            unit_str = ''
            ingredient_str = ''
            parentheses_str = ''

            start = self.fam_data[i].find('(')
            end = self.fam_data[i].find(')')
            if start != -1 and end != -1:
                parentheses_str = self.fam_data[i][start + 1:end]

            if len(parentheses_str) > 0:
                self.fam_data[i] = self.fam_data[i].replace(f"({parentheses_str})", '')

            for word in self.fam_data[i].split():
                count = 0
                for char in word:
                    if 47 <= ord(char) <= 57:
                        count += 1
                    if count == len(word):
                        num_str += word + ' '
                if word in measurement_units:
                    if word not in unit_str:
                        unit_str += word
                if word not in measurement_units:
                    count = 0
                    for char in word:
                        if 47 <= ord(char) <= 57:
                            count += 1
                    if count != len(word):
                        ingredient_str += word + ' '

            if len(unit_str) != 0 and unit_str[-1] == 's':
                unit_str = unit_str[:-1]
            self.nums.append(num_str[:-1])
            self.units.append(unit_str)
            self.__scale()
            self.ingredient_viewLbl = tk.Label(self.frame, text=f"{ingredient_str}").grid(
                row=(2 + i - self.ingredient_index),
                column=2, sticky='w')

        self.processLbl = tk.Label(self.frame, text="Process").grid(row=1, column=3, columnspan=3)
        count = 1
        row_index = 0
        endwordindex = None
        for i in range(1 + self.process_index, self.cooktime_index):
            endwordindexlist = []
            process_data = self.fam_data[i].split()
            for word in process_data:
                for char in word:
                    endwordindex = 0
                    if char == '.':
                        endword = word
                        endwordindex = process_data.index(endword)
                endwordindexlist.append(endwordindex)
            indexlist = [0]

            for index in endwordindexlist:
                if index != 0:
                    indexlist.append(index + 1)
            if (len(endwordindexlist) - 1) not in indexlist:
                indexlist.append(len(endwordindexlist))

            for j in range(0, len(indexlist) - 1):
                if len(process_data) != 0 and len(process_data[indexlist[j - 1]:indexlist[j]]) == 0:
                    self.processesLbl = tk.Label(self.processFrame, text=f"({count})"). \
                        grid(row=row_index, column=0, columnspan=3, sticky='w')
                    row_index += 1
                if len(process_data) != 0 and len(process_data[indexlist[j]:indexlist[j + 1]]) != 0:
                    if 48 <= ord(process_data[indexlist[j]][0]) <= 57:
                        self.processesLbl = tk.Label(self.processFrame,
                                                     text=f"{' '.join(process_data[indexlist[j]:indexlist[j + 1]][1:])}"
                                                          f"").grid(row=row_index, column=0, columnspan=3, sticky='w')
                    else:
                        self.processesLbl = tk.Label(self.processFrame,
                                                     text=f"{' '.join(process_data[indexlist[j]:indexlist[j + 1]])}").\
                            grid(row=row_index, column=0, columnspan=3, sticky='w')
                    row_index += 1
            if len(process_data) != 0:
                count += 1

    def __scale(self):
        multiplier = self.scaleVar.get()
        if multiplier != '':
            multiplier = float(multiplier)
            multiplier = multiplier * ss.fam_scale(self.fam_data)
            i = self.ingredient_index + 1
            j = 0
            for num in self.nums:
                scaled_num, scaled_unit = ss.scale(num, multiplier, self.units[j])
                self.numLbl = tk.Label(self.frame, text=f"{scaled_num}", bg='SystemButtonFace').grid(
                    row=(2 + i - self.ingredient_index), column=0, sticky='we')
                self.unitLbl = tk.Label(self.frame, text="", bg='SystemButtonFace').grid(
                    row=(2 + i - self.ingredient_index), column=1, sticky='we')
                self.unitLbl = tk.Label(self.frame, text=f"{scaled_unit}", bg='SystemButtonFace').grid(
                    row=(2 + i - self.ingredient_index), column=1, sticky='w')
                i += 1
                j += 1

    def __review(self):
        self.frame.destroy()
        self.processFrame.destroy()
        rr.ReviewRecipe(self.master, self.family, self.recipe_name)
        return
