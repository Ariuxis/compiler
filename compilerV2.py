                                                #===============================================================================#
                                                #                   Pontificia Universidad Javeriana, Cali                      #
                                                #                           Facultad de Ingeniería                              #
                                                #                    Ingeniería de Sistemas y Computación                       #
                                                #                       Arquitectura del Computador II                          #
                                                #                               Antonio Yu Chen                                 #
                                                #===============================================================================#

import re
from tkinter import *

# R0 will be the base address. It will point to the start of the data memory. It starts at the position 0.
# The memory address which points to the arrays will be 100. Each array has a size of 100.

# Initialization of window with widgets #
root = Tk()
root.title("Compilador a Von Neumann")
root.geometry("800x700")
inputText = Text(width = 35)
inputText.place(x = 35, y = 80)
outputText = Text(width = 35)
outputText.place(x = 485, y = 80)
inputLabel = Label(text = "Algoritmo en alto nivel", font = ("Inconsolata", 12))
inputLabel.place(x = 90, y = 50)
outputLabel = Label(text = "Algoritmo en Von Neumann", font = ("Inconsolata", 12))
outputLabel.place(x = 530, y = 50)
periodText = Text(height = 1, width = 10)
periodText.place(x = 35, y = 525)
periodLabel = Label(text = "Periodo de reloj", font = ("Inconsolata", 12))
periodLabel.place(x = 32, y = 500)
frequencyText = Text(height = 1, width = 10)
frequencyText.place(x = 35, y = 580)
frequencyLabel = Label(text = "Frecuencia de reloj", font = ("Inconsolata", 12))
frequencyLabel.place(x = 32, y = 555)
execText = Text(height = 1, width = 25)
execText.place(x = 483, y = 525)
execLabel = Label(text = "Tiempo de ejecucion", font = ("Inconsolata", 12))
execLabel.place(x = 480, y = 500)
outputText.config(state = DISABLED)
periodText.config(state = DISABLED)
frequencyText.config(state = DISABLED)
execText.config(state = DISABLED)
# Initialization of variables #
registerList = []
counterList = [0, 0, 0] # First position corresponds to if, second to for, third to while
frequency = 0
period = 0

def validAlgorithm():
	algorithm = (inputText.get("1.0", "end-1c")).split("\n")
	assign = "^([A-z]+[0-9]*)\s*=\s*([A-z]+[0-9]*|[0-9]+)$"
	init = "^(int)\s*([A-z]+[0-9]*)$"
	ifWhile = "^(if|while)[(]\s*([A-z]+[0-9]*|[0-9]+)\s*(<|>|!=|==)\s*([A-z]+[0-9]*|[0-9]+)\s*[)]\s*{$"


def compiler(cycles):
    algorithm = (inputText.get("1.0", "end-1c")).split("\n") # Splits the algorithm that was written into the input text box and stores it in an array.
    for line in algorithm:
        if(re.match("^(int)\s*([A-z]+[0-9]*)$", line)):
            instruction = re.match("^(int)\s*([A-z]+[0-9]*)$", line)
            register = instruction.group(2)
            if(register not in registerList):
                registerList.append(register)
    outputText.config(state = NORMAL)
    outputText.insert(END, "MOV R0, 0")
    outputText.config(state = DISABLED)


def translate():
    cycles = 1
    outputText.config(state = NORMAL)
    outputText.delete("1.0", END)
    outputText.config(state = DISABLED)
    counterList = [0, 0, 0]
    if(inputText.get("1.0", END) != "\n"):
        cycles = compiler(cycles)
    outputFile = open("output.txt", "w")
    outputFile.write(outputText.get("1.0", "end-1c"))
    outputFile.close()
    #print(cycles)

def clear():
    """Procedure that clears all the text boxes."""
    inputText.delete("1.0", END)
    outputText.config(state = NORMAL)
    outputText.delete("1.0", END)
    outputText.config(state = DISABLED)
    periodText.config(state = NORMAL)
    periodText.delete("1.0", END)
    periodText.config(state = DISABLED)
    frequencyText.config(state = NORMAL)
    frequencyText.delete("1.0", END)
    frequencyText.config(state = DISABLED)
    execText.config(state = NORMAL)
    execText.delete("1.0", END)
    execText.config(state = DISABLED)
    registerList = []
    counterList = [0, 0, 0]
    
def period():
    """Procedure that enables the periodText text box and clears the frequencyText text box."""
    frequencyText.config(state = NORMAL)
    frequencyText.delete("1.0", END)
    frequencyText.config(state = DISABLED)
    periodText.config(state = NORMAL)

def frequency():
    """Procedure that enables the frequencyText text box and clears the frequencyText text box."""
    periodText.config(state = NORMAL)
    periodText.delete("1.0", END)
    periodText.config(state = DISABLED)
    frequencyText.config(state = NORMAL)
    
translateButton = Button(text = "Traducir", font = ("Inconsolata", 12), command = translate)
translateButton.place(x = 365, y = 250)
clearButton = Button(text = "Limpiar", font = ("Inconsolata", 12), command = clear)
clearButton.place(x = 365, y = 300)
periodButton = Button(text = "Periodo de reloj", font = ("Inconsolata", 9), command = period)
periodButton.place(x = 165, y = 500)
frequencyButton = Button(text = "Frecuencia de reloj", font = ("Inconsolata", 9), command = frequency)
frequencyButton.place(x = 180, y = 555)
