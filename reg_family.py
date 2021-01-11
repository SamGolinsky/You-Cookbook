import tkinter as tk
from functools import partial
import family
import os
from center_window import *


class RegisterFamily:
    def __init__(self, master):
        self.master = master
        self.master.geometry('250x215')
        center(self.master)
        self.frame = tk.Frame(self.master)
        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1, 2], minsize=40)
        self.frame.grid_columnconfigure([0, 1, 2], minsize=65)

        self.famName = tk.StringVar()
        self.famNum = tk.StringVar()
        self.famNameLbl = tk.Label(self.frame, text="Family Name: ").grid(row=0, column=0)
        self.famNameNtr = tk.Entry(self.frame, textvariable=self.famName).grid(row=0, column=1)
        self.numPplLbl = tk.Label(self.frame, text="Number of People: ").grid(row=1, column=0)
        self.numPplNtr = tk.Entry(self.frame, textvariable=self.famNum).grid(row=1, column=1)

        self.enterNames = tk.Button(self.frame, text="Enter Names: ", command=self.__name_frame).grid(row=2, column=1)

    def __name_frame(self):
        for i in self.famNum.get():
            if not(48 <= ord(i) <= 57):
                self.alertLbl = tk.Label(self.frame, text="Number of People must be an Integer Value").grid(row=5, column=0, columnspan=3)
                return
        if os.path.isfile(f"{self.famName.get()}"):
            self.alertLbl = tk.Label(self.frame, text="Family Already Registered").grid(row=5, column=0, columnspan=3)
            return
        try:
            int(self.famNum.get())
        except ValueError:
            return
        self.family_file = open(self.famName.get(), "w+")
        self.family_file.write(self.famName.get() + '\n')
        families_file = open("families", "a+")
        families_file.write(self.famName.get() + '\n')
        families_file.close()

        self.nameFrame = tk.Frame(self.master)
        self.nameFrame.grid(row=1, column=0)
        self.nameFrame.grid_rowconfigure([0, 1], minsize=40)
        self.nameFrame.grid_columnconfigure([0, 1, 2], minsize=65)

        self.i = 1

        self.personLbl = tk.Label(self.nameFrame, text=f"Person #{self.i}").grid(row=0, column=0)
        self.personName = tk.StringVar()
        self.personNtr = tk.Entry(self.nameFrame, textvariable=self.personName)
        self.personNtr.grid(row=0, column=1)

        if int(self.famNum.get()) == 1:
            self.ctnuBtn = tk.Button(self.nameFrame, text="Continue", command=self.__continue_reg).grid(row=1, column=1)
        else:
            self.nxtPersonBtn = tk.Button(self.nameFrame, text="Next", command=self.__next_person).grid(row=1, column=1)

    def __next_person(self):
        if self.i == int(self.famNum.get())-1:
            self.ctnuBtn = tk.Button(self.nameFrame, text="Continue", command=self.__continue_reg).grid(row=1, column=1)
        if self.i < int(self.famNum.get()):
            self.family_file.write(self.personName.get() + '\n')
            self.i += 1
            self.personLbl = tk.Label(self.nameFrame, text=f"Person #{self.i}").grid(row=0, column=0)
            self.personNtr.delete(0, 'end')

    def __continue_reg(self):
        self.family_file.write(self.personName.get() + '\n')
        self.family_file.close()

        self.newFrame = tk.Frame(self.master)
        self.nameFrame.destroy()
        self.frame.destroy()
        IndividualPerson(self.master, self.newFrame, int(self.famNum.get()), self.famName)


class IndividualPerson:
    def __init__(self, master, frame, num, name):
        self.frame = frame
        self.master = master
        self.master.geometry('505x710')
        center(self.master)
        self.famNum = num
        self.famName = name

        self.frame.grid(row=0, column=0)
        self.frame.grid_rowconfigure([0, 1, 2, 3, 4, 5], minsize=40)
        self.frame.grid_columnconfigure([0, 1, 2, 3, 4], minsize=65)

        with open(self.famName.get(), "r") as self.fam_file:
            self.fam_data = self.fam_file.readlines()
        self.__each_person_info(1)

    def __each_person_info(self, i):
        self.i = i
        self.personLbl = tk.Label(self.frame, text=f"{self.fam_data[self.i][:-1]}'s Personal Information")
        self.personLbl.grid(row=0, column=0, sticky="we", columnspan=5)
        self.portionLbl = tk.Label(self.frame, text="Select Portion Size:").grid(row=1, column=0)
        self.portionViewBtn = tk.Button(self.frame, text="View Portion", command=self.__portion_graph).grid(row=2, column=0)
        self.portionSld = tk.Scale(self.frame, tickinterval=25, showvalue=0, orient=tk.HORIZONTAL)
        self.portionSld.grid(row=1, column=1, columnspan=4, stick="we")
        self.portionsLbl = tk.Label(self.frame, text="petite\t\tNormal\t\tBig Boi\t\tULTRA").grid(row=2, column=1, sticky="we", columnspan=4)
        self.portionGraph = tk.Canvas(self.frame, bg="darkgoldenrod3", height=500, width=500)
        self.portionGraph.grid(row=3, column=0, columnspan=5, sticky="we")
        self.portionPlate = self.portionGraph.create_oval(10, 490, 490, 10, fill="lemon chiffon")

        self.allergyLbl = tk.Label(self.frame, text="Allergies: ").grid(row=4, column=0)
        self.allergyVar = tk.StringVar()
        self.allergyNtr = tk.Entry(self.frame, textvariable=self.allergyVar)
        self.allergyNtr.grid(row=4, column=1)
        self.allergyLbl2 = tk.Label(self.frame, text="(if many separate w/ ',')").grid(row=4, column=2)

        self.nextBtn = tk.Button(self.frame, text="Next", command=partial(self.__next_person_info, self.i)).grid(row=5, column=4)
        if self.famNum == 1:
            self.finishBtn = tk.Button(self.frame, text="Finish", command=partial(self.__add_personal, self.i)).grid(row=5, column=4)

    def __portion_graph(self):
        self.portionDepiction = self.portionGraph.create_oval(10, 490, 490, 10, fill="lemon chiffon")
        if 0 <= self.portionSld.get() < 25:
            self.portionDepiction = self.portionGraph.create_oval(200, 300, 300, 200, fill="salmon1")
        elif 25 <= self.portionSld.get() < 50:
            self.portionDepiction = self.portionGraph.create_oval(150, 350, 350, 150, fill="salmon1")
        elif 50 <= self.portionSld.get() < 75:
            self.portionDepiction = self.portionGraph.create_oval(100, 400, 400, 100, fill="salmon1")
        elif 75 <= self.portionSld.get() < 100:
            self.portionDepiction = self.portionGraph.create_oval(50, 450, 450, 50, fill="salmon1")

    def __next_person_info(self, i):
        self.i = i
        self.__add_personal(self.i)
        self.i += 1
        if self.i == self.famNum:
            self.__each_person_info(self.i)
            self.finishBtn = tk.Button(self.frame, text="Finish", command=partial(self.__add_personal, self.i)).grid(row=5, column=4)
        else:
            self.__each_person_info(self.i)

    def __add_personal(self, i):
        if 0 <= self.portionSld.get() < 25:
            self.portionSize = 1
        elif 25 <= self.portionSld.get() < 50:
            self.portionSize = 2
        elif 50 <= self.portionSld.get() < 75:
            self.portionSize = 3
        elif 75 <= self.portionSld.get() < 100:
            self.portionSize = 4

        self.fam_data[i] = self.fam_data[i][:-1] + f"; {self.portionSize}; {self.allergyVar.get()}" + "\n"
        self.family_file = open(self.famName.get(), "w+")

        if self.i == self.famNum:
            self.family_file.writelines(self.fam_data + ['|\n'])
            self.family_file.close()
            self.frame.destroy()
            family.ChoseFamily(self.master)

